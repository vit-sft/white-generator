import json
import asyncio
import hashlib
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import Optional, Literal
from .variant_1_creator.parser import get_parser, generate_data
from .variant_1_creator.generator import build_site_from_parser, build_site_from_data
from .variant_1_creator.requests import fetch_html
from .variant_1_creator.schemas import AppData
from .bucket import AsyncS3Client
from app.core.config import (
    ACCESS_KEY,
    ACCESS_SECRET,
    BUCKET_NAME,
    AWS_REGION,
    DIST_DIR,
    BASIC_FOLDER,
)


async def build_from_app_data(app_data: dict) -> str:
    """
    Build a site using pre-existing application data.
    """
    if isinstance(app_data, dict):
        app_data = AppData(**app_data)

    return await build_site_from_data(app_data)


async def build_from_generated_data(generation_query: str) -> str:
    """
    Generate new data and build a site from it.
    """
    data = await generate_data(generation_query)
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
    campaign_id: str,
    mode: Literal["app_data", "to_generate_data", "url"],
    generation_query: Optional[str] = None,
    app_data: Optional[dict] = None,
    url: Optional[str] = None,
) -> str:
    """
    Build app site based on the given mode and install from/upload it to S3.
    Returns destination.
    """
    if not campaign_id:
        raise ValueError("campaign_id cannot be None or empty")

    full_string = f"{mode or ''}{generation_query or ''}{app_data or ''}{url or ''}"
    hashed_string = hashlib.md5(full_string.encode()).hexdigest()

    # Using Bucket client to make bucket operations
    async with AsyncS3Client(
        region_name=AWS_REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=ACCESS_SECRET,
        bucket_name=BUCKET_NAME,
        basic_folder=BASIC_FOLDER,
    ) as bucket_client:
        bucket_cache = await bucket_client.check_bucket_cache(
            destination=DIST_DIR, campaign_id=campaign_id, hashed_string=hashed_string
        )
        if bucket_cache:
            return bucket_cache

        handlers = {
            "app_data": (
                app_data,
                build_from_app_data,
                "In Data mode you need to put data",
            ),
            "to_generate_data": (
                generation_query,
                build_from_generated_data,
                "In Generation mode you need to put generation query",
            ),
            "url": (url, build_from_url, "In URL mode you need to put url"),
        }

        if mode not in handlers:
            raise ValueError(f"Invalid build mode: {mode}")

        data, handler, error_message = handlers[mode]
        if not data:
            raise ValueError(error_message)

        # Build the directory locally
        directory = await handler(data)

        # Upload to S3

        await bucket_client.upload_directory(
            origin=DIST_DIR, prefix=f"{campaign_id}_{hashed_string}"
        )
        return directory


if __name__ == "__main__":
    with open("app/core/test copy.json", "r") as f:
        conf_data = json.load(f)

    abs_path = asyncio.run(build_app_site(**conf_data))
    print(abs_path)
