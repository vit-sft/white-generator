from aiobotocore.session import get_session
import aiofiles
import os
import asyncio
import mimetypes
from white_generator.utils import build_directories


class AsyncS3Client:
    """
    Async client for AWS S3 bucket operations.
    
    Provides async methods to interact with an S3 bucket — such as listing, uploading,
    downloading, and deleting files or directories.

    Usage:
        async with AsyncS3Client(bucket_name="my-bucket", basic_folder="data/") as s3:
            dirs = await s3.list_directories()
    """
    def __init__(
        self,
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
        region_name="eu-north-1",
        basic_folder="",
    ):
        """
        Initialize the AsyncS3Client.

        Args:
            aws_access_key_id (str): AWS access key ID.
            aws_secret_access_key (str): AWS secret access key.
            bucket_name (str): Name of the S3 bucket.
            region_name (str, optional): AWS region name. Defaults to "eu-north-1".
            basic_folder (str, optional): Base folder path within the bucket.
        """
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.basic_folder = basic_folder
        self._session = get_session()
        self._client = None

    async def __aenter__(self):
        """Enter the async context and create the S3 client."""
        self._client = await self._create_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context and close the S3 client connection."""
        await self._client.close()

    async def _create_client(self):
        """Create and return an aiobotocore S3 client."""
        return await self._session.create_client(
            "s3",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ).__aenter__()

    async def list_directories(self, prefix: str = "") -> list[str]:
        """List only directories in the bucket."""
        resp = await self._client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=self.basic_folder + prefix,
            Delimiter="/",
        )

        directories = [p["Prefix"] for p in resp.get("CommonPrefixes", [])]
        return directories

    async def list_files_in_directory(self, prefix: str = "") -> list[str]:
        """List of files in directory in the bucket."""

        resp = await self._client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=self.basic_folder + prefix,
        )
        object_keys = [obj["Key"] for obj in resp.get("Contents", [])]
        return object_keys


    async def upload_file(self, local_path: str, key: str, content_type):
        """Upload file in a from relative path ot key directory in Bucket"""
        
        async with aiofiles.open(local_path, "rb") as f:
            body = await f.read()
            await self._client.put_object(
                Bucket=self.bucket_name, Key=key, Body=body, ContentType=content_type
            )
            
    async def upload_directory(self, origin: str, prefix: str):
        """Recursively upload all files in a origin directory to Bucket"""
        
        # Define the key prefix and cloud base URL
        key_prefix = f"{self.basic_folder}{prefix}".rstrip("/")
        base_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{key_prefix}/source_target.html"
        
        tasks = []
        
        for root, _, files in os.walk(origin):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, start=origin)
                key = f"{self.basic_folder}{prefix}/{relative_path}".replace("\\", "/")
                content_type, _ = mimetypes.guess_type(local_path)
                tasks.append(self.upload_file(local_path=local_path, key=key, content_type=content_type))
                
        await asyncio.gather(*tasks)
        return base_url

    async def delete_directory(self, prefix: str) -> None:
        """Delete all S3 objects under prefix."""
        if not prefix:
            return

        objects_to_delete = await self.list_files_in_directory(prefix)
        if not objects_to_delete:
            return

        delete_params = {
            "Bucket": self.bucket_name,
            "Delete": {"Objects": [{"Key": obj} for obj in objects_to_delete]},
        }

        await self._client.delete_objects(**delete_params)

    async def download_file(self, key: str, local_path: str) -> None:
        """Download S3 object file and save it locally."""

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        resp = await self._client.get_object(Bucket=self.bucket_name, Key=key)
        async with aiofiles.open(local_path, "wb") as f:
            body = await resp["Body"].read()
            await f.write(body)

    async def download_directory(self, destination: str, prefix: str) -> None:
        """Download all files from Bucket prefix to a destination directory"""

        objects_to_install = await self.list_files_in_directory(prefix)

        if not objects_to_install:
            return

        build_directories()
        # Define the key prefix and cloud base URL
        key_prefix = f"{self.basic_folder}{prefix}".rstrip("/")
        base_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{key_prefix}/source_target.html"
        
        tasks = []
        for obj in objects_to_install:
            key = obj
            if key.endswith("/"):
                continue

            relative_path = key.removeprefix(self.basic_folder + prefix).lstrip("/\\")
            local_path = os.path.join(destination, relative_path)

            # Create download task
            tasks.append(self.download_file(key, local_path))

        await asyncio.gather(*tasks)
        return os.path.abspath(destination), base_url

    async def check_bucket_cache(self, destination: str, campaign_id: str, hashed_string: str):
        """
        Looking for White page by campaign_id in a Bucket. If exists: downloading it into destination.
        If exists but with old data - delete it.
        """

        prefix = f"{campaign_id}_{hashed_string}/"
        white_name = self.basic_folder + f"{prefix}"
        white_list = await self.list_directories()
        # Checking if there's already white with those params
        if white_name in white_list:
            return await self.download_directory(destination=destination, prefix=prefix)

        # Checking if there's already white with same campaign_id
        for key in white_list:
            if key.startswith(f"{self.basic_folder}{campaign_id}_"):
                key = key.removeprefix(self.basic_folder)
                await self.delete_directory(prefix=key)
                break
        return None, None
