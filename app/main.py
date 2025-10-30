import json
import asyncio
import hashlib
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import Optional, Literal
from .variant_1_creator.parser import get_parser
from .variant_1_creator.builder import build_site_from_parser, build_site_from_data
from .variant_1_creator.requests import fetch_html
from .variant_1_creator.generator import AppDataGenerator
from .variant_1_creator.schemas import AppData
from .bucket import AsyncS3Client
from app.core.config import config


async def build_from_app_data(app_data: dict) -> str:
    """
    Build a site using pre-existing application data.
    """
    if isinstance(app_data, dict):
        app_data = AppData(**app_data)

    return await build_site_from_data(app_data)


async def build_from_generated_data(
    generation_query: str, img_cx: str, img_api_token: str, llm_api_key: str
) -> str:
    """
    Generate new data and build a site from it.
    """
    async with AppDataGenerator(
        img_cx=img_cx, img_api_token=img_api_token, llm_api_key=llm_api_key
    ) as data_generator:
        data = await data_generator.generate_data(generation_query=generation_query)
    return await build_site_from_parser(data)


async def build_from_url(url: str) -> str:
    """
    Fetch HTML content from a URL and build a site from the parsed information.
    """
    async with ClientSession() as session:
        html = await fetch_html(session, url)
        parser = get_parser(url)
        soup = BeautifulSoup(html, "html.parser")
        data = parser(soup, url)

        return await build_site_from_parser(data)


async def build_app_site(
    target_directory: str,
    campaign_id: str,
    mode: Literal["app_data", "to_generate_data", "url"],
    generation_query: Optional[str] = None,
    app_data: Optional[dict] = None,
    url: Optional[str] = None,
    img_cx: str = None,
    img_api_token: str = None,
    llm_api_key: str = None,
    access_key: str = None,
    access_secret: str = None,
) -> str:
    """
    Build app site based on the given mode and install from/upload it to S3.
    Returns destination.
    """
    if not target_directory:
        target_directory = str(config.APP_DIR.parent / "dist")
    
    if not os.path.isabs(target_directory):
        raise ValueError("target_directory has to be absolute path")
    
    if not campaign_id:
        raise ValueError("campaign_id cannot be None or empty")
    
    # Setting directories.
    config.set_dist_dir(target_directory)
    
    full_string = f"{mode or ''}{generation_query or ''}{app_data or ''}{url or ''}"
    hashed_string = hashlib.md5(full_string.encode()).hexdigest()

    # Using Bucket client to make bucket operations
    async with AsyncS3Client(
        region_name=config.AWS_REGION,
        aws_access_key_id=access_key,
        aws_secret_access_key=access_secret,
        bucket_name=config.BUCKET_NAME,
        basic_folder=config.BASIC_FOLDER,
    ) as bucket_client:
        bucket_cache, bucket_url = await bucket_client.check_bucket_cache(
            destination=target_directory, campaign_id=campaign_id, hashed_string=hashed_string
        )
        if bucket_cache and bucket_url:
            return bucket_cache, bucket_url

        match mode:
            case "app_data":
                if not app_data:
                    raise ValueError("In Data mode you need to put data")
                directory = await build_from_app_data(app_data)
            case "to_generate_data":
                if not generation_query:
                    raise ValueError("In Generation mode you need to put generation query")
                directory = await build_from_generated_data(generation_query, img_cx, img_api_token, llm_api_key)
            case "url":
                if not url:
                    raise ValueError("In URL mode you need to put url")
                directory = await build_from_url(url)
            case _:
                raise ValueError(f"Invalid build mode: {mode}")

        # Upload to S3

        bucket_url = await bucket_client.upload_directory(
            origin=target_directory, prefix=f"{campaign_id}_{hashed_string}"
        )
        return directory, bucket_url


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    with open("app/core/test.json", "r") as f:
        conf_data = json.load(f)
    # Abs path where to save DIR.
    target_directory = ""
    
    abs_path, bucket_url = asyncio.run(
        build_app_site(
            target_directory=target_directory,
            **conf_data,
            img_cx=os.getenv("IMG_CX"),
            img_api_token=os.getenv("IMG_API_TOKEN"),
            llm_api_key=os.getenv("LLM_API_KEY"),
            access_key=os.getenv("ACCESS_KEY"),
            access_secret=os.getenv("ACCESS_SECRET"),
        )
    )
    print(abs_path, bucket_url)
