import asyncio
import shutil
import os
from white_generator.core.config import config
import time
from functools import wraps


async def copy_file_async(src, dst):
    await asyncio.to_thread(shutil.copy2, src, dst)


async def copy_all_files(file_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    tasks = []

    for filename in os.listdir(file_dir):
        if filename:
            src = os.path.join(file_dir, filename)
            dst = os.path.join(dest_dir, filename)
            tasks.append(copy_file_async(src, dst))

    await asyncio.gather(*tasks)


def remove_dir(path):
    """Removes directory if it exists"""
    if os.path.isdir(path):
        shutil.rmtree(path)


def build_directories():
    """
    Removes old dir and creates new folders for site
    """
    remove_dir(config.DIST_DIR)
    dirs_to_create = [
        config.DIST_DIR,
        config.STATIC_DIR,
        config.IMG_DIR,
        config.CSS_DIR,
        config.JS_DIR,
        config.FONTS_DIR,
    ]

    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)


def timeit(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(
            f"Async function '{func.__name__}' executed in {elapsed_time:.4f} seconds."
        )
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(
            f"Sync function '{func.__name__}' executed in {elapsed_time:.4f} seconds."
        )
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
