import asyncio
import hashlib
import json
import os
from pathlib import Path
from typing import Literal

from white_generator.bucket import AsyncS3Client
from white_generator.core import settings
from white_generator.core.config import Variant1BuildContext, Variant2BuildContext
from white_generator.variant_1_creator.builder import AppBuilder
from white_generator.variant_2_creator.builder import MiniAppBuilder


async def build_app_site(
    target_directory: str,
    campaign_id: str,
    mode: Literal["app_data", "to_generate_data", "url", "mini_app"],
    generation_query: str | None = None,
    app_data: dict | None = None,
    url: str | None = None,
    img_cx: str | None = None,
    img_api_token: str | None = None,
    llm_api_key: str | None = None,
    access_key: str | None = None,
    access_secret: str | None = None,
    template_number: int | None = None,
) -> dict:
    """
    Build app site based on the given mode and install from/upload it to S3.
    Returns destination.

    Modes:
    - app_data: Build from existing app data
    - to_generate_data: Generate data and build
    - url: Parse URL and build
    - mini_app: Build mini app (tower game) with optional game_config
    """

    if not target_directory:
        # Use the parent directory of this main Python file.
        target_directory = str(Path(__file__).resolve().parent.parent / "dist")

    if not os.path.isabs(target_directory):
        raise ValueError("target_directory has to be absolute path")

    if not campaign_id:
        raise ValueError("campaign_id cannot be None or empty")

    if template_number and template_number not in range(1, 6):
        raise ValueError("template_number has to be inside 1 to 5 range")

    full_string = (
        f"{mode or ''}"
        f"{generation_query or ''}"
        f"{str(app_data) or ''}"
        f"{url or ''}"
    )
    hashed_string = hashlib.md5(full_string.encode()).hexdigest()
    # Using Bucket client to make bucket operations
    async with AsyncS3Client(
        region_name=settings.AWS_REGION,
        aws_access_key_id=access_key,
        aws_secret_access_key=access_secret,
        bucket_name=settings.BUCKET_NAME,
        basic_folder=settings.BASIC_FOLDER,
    ) as bucket_client:

        bucket_cache, bucket_url = await bucket_client.check_bucket_cache(
            destination=target_directory,
            campaign_id=campaign_id,
            hashed_string=hashed_string,
        )

        if bucket_cache and bucket_url:
            return {
                "local_dist": bucket_cache,
                "cloud_url": bucket_url,
            }

        # Create the appropriate build context and builder.
        if mode == "mini_app":
            context = Variant2BuildContext(
                dist_dir=target_directory,
            )

            builder = MiniAppBuilder(context)
            directory = await builder.build()

        else:
            context = Variant1BuildContext(
                dist_dir=target_directory,
            )

            builder = AppBuilder(
                context,
                template_number,
            )

            match mode:
                case "app_data":
                    if not app_data:
                        raise ValueError(
                            "In Data mode you need to put data"
                        )

                    directory = await builder.build_from_app_data(
                        app_data
                    )

                case "to_generate_data":
                    if not generation_query:
                        raise ValueError(
                            "In Generation mode you need to put generation query"
                        )

                    directory = await builder.build_from_generated_data(
                        generation_query,
                        img_cx,
                        img_api_token,
                        llm_api_key,
                    )

                case "url":
                    if not url:
                        raise ValueError(
                            "In URL mode you need to put url"
                        )

                    directory = await builder.build_from_url(url)

                case _:
                    raise ValueError(
                        f"Invalid build mode: {mode}"
                    )

        # Upload to S3
        bucket_url = await bucket_client.upload_directory(
            origin=target_directory,
            prefix=f"{campaign_id}_{hashed_string}",
        )

        return {
            "local_dist": directory,
            "cloud_url": bucket_url,
        }


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    with open("test.json", "r") as f:
        conf_data = json.load(f)

    with open("test copy.json", "r") as f:
        conf_data1 = json.load(f)

    with open("test copy 2.json", "r") as f:
        conf_data2 = json.load(f)

    with open("test copy 3.json", "r") as f:
        conf_data3 = json.load(f)

    # Output directories
    target_directory = ""
    target_directory1 = ""
    target_directory2 = ""

    async def runner():
        result = await build_app_site(
            target_directory=target_directory,
            **conf_data3,
            img_cx=os.getenv("IMG_CX"),
            img_api_token=os.getenv("IMG_API_TOKEN"),
            llm_api_key=os.getenv("LLM_API_KEY"),
            access_key=os.getenv("ACCESS_KEY"),
            access_secret=os.getenv("ACCESS_SECRET"),
            # template_number=4,
        )

        print(result)

    asyncio.run(runner())