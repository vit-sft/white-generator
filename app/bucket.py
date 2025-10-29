from aiobotocore.session import get_session
from app.core.config import (
    ACCESS_KEY,
    ACCESS_SECRET,
    BUCKET_NAME,
    AWS_REGION,
    DIST_DIR,
    BASIC_FOLDER,
)
import aiofiles
import os
import asyncio
from .utils import build_directories


session = get_session()


async def get_s3_client():
    """Return a client."""
    return session.create_client(
        "s3",
        region_name=AWS_REGION,
        aws_secret_access_key=ACCESS_SECRET,
        aws_access_key_id=ACCESS_KEY,
    )


async def list_directories(client, prefix: str = "") -> list[str]:
    """List only directories in the bucket."""
    resp = await client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=BASIC_FOLDER + prefix,
        Delimiter="/",
    )

    directories = [p["Prefix"] for p in resp.get("CommonPrefixes", [])]
    return directories


async def list_files_in_directory(client, prefix: str = "") -> list[str]:
    """List of files in directory in the bucket."""

    resp = await client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=BASIC_FOLDER + prefix,
    )
    object_keys = [obj["Key"] for obj in resp.get("Contents", [])]
    return object_keys


async def upload_directory(client, prefix: str):
    """Recursively upload all files in a directory to Bucket"""
    for root, _, files in os.walk(DIST_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, start=DIST_DIR)
            key = f"{BASIC_FOLDER}{prefix}/{relative_path}".replace("\\", "/")

            async with aiofiles.open(local_path, "rb") as f:
                body = await f.read()
                await client.put_object(Bucket=BUCKET_NAME, Key=key, Body=body)


async def delete_directory(client, prefix: str) -> None:
    """Delete all S3 objects under directory."""
    if not prefix:
        return

    objects_to_delete = await list_files_in_directory(client, prefix)

    if not objects_to_delete:
        return

    delete_params = {
        "Bucket": BUCKET_NAME,
        "Delete": {"Objects": [{"Key": obj} for obj in objects_to_delete]},
    }

    await client.delete_objects(**delete_params)


async def download_file(client, key: str, local_path: str) -> None:
    """Download S3 object file and save it locally."""

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    resp = await client.get_object(Bucket=BUCKET_NAME, Key=key)
    async with aiofiles.open(local_path, "wb") as f:
        body = await resp["Body"].read()
        await f.write(body)


async def download_directory(client, prefix: str) -> None:
    """Download all files from prefix to DIST_DIR"""

    objects_to_install = await list_files_in_directory(client, prefix)

    if not objects_to_install:
        return

    build_directories()

    tasks = []
    for obj in objects_to_install:
        key = obj
        if key.endswith("/"):
            continue

        relative_path = key.removeprefix(BASIC_FOLDER + prefix).lstrip("/\\")
        local_path = os.path.join(DIST_DIR, relative_path)

        # Create download task
        tasks.append(download_file(client, key, local_path))

    await asyncio.gather(*tasks)
    return os.path.abspath(DIST_DIR)


async def check_bucket_cache(campaign_id: str, hashed_string: str):
    """
    Looking for White page by campaign_id in a Bucket. If exists: downloading it.
    If exists but with old data - delete it.
    """

    async with await get_s3_client() as client:
        prefix = f"{campaign_id}_{hashed_string}/"
        white_name = BASIC_FOLDER + f"{prefix}"
        white_list = await list_directories(client=client)
        # Checking if there's already white with those params
        if white_name in white_list:
            return await download_directory(client=client, prefix=prefix)

        # Checking if there's already white with same campaign_id
        for key in white_list:
            if key.startswith(f"{BASIC_FOLDER}{campaign_id}_"):
                key = key.removeprefix(BASIC_FOLDER)
                await delete_directory(client=client, prefix=key)
                break
    return None
