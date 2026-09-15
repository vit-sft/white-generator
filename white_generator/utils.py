import asyncio
import os
import shutil
import time
from functools import wraps

from white_generator.core.config import BuildContext


async def copy_file_async(src: str, dst: str) -> None:
    """Copy a file asynchronously."""
    await asyncio.to_thread(shutil.copy2, src, dst)


async def copy_all_files(file_dir: str, dest_dir: str) -> None:
    os.makedirs(dest_dir, exist_ok=True)

    tasks = []

    for filename in os.listdir(file_dir):
        if filename:
            src = os.path.join(file_dir, filename)
            dst = os.path.join(dest_dir, filename)
            tasks.append(copy_file_async(src, dst))

    await asyncio.gather(*tasks)


def remove_dir(path: str) -> None:
    """Removes directory if it exists"""
    if os.path.isdir(path):
        shutil.rmtree(path)

def build_directories(context: BuildContext) -> None:
    """
    Removes old dir and creates new folders for site

    Args:
        context: BuildContext instance with DIST_DIR and other paths set
    """
    remove_dir(context.DIST_DIR)
    dirs_to_create = [
        context.DIST_DIR,
        context.STATIC_DIR,
        context.IMG_DIR,
    ]
    # Add other paths if they exist in the specific context
    if hasattr(context, 'CSS_DIR'): dirs_to_create.append(context.CSS_DIR)
    if hasattr(context, 'JS_DIR'): dirs_to_create.append(context.JS_DIR)
    if hasattr(context, 'FONTS_DIR'): dirs_to_create.append(context.FONTS_DIR)
    if hasattr(context, 'ASSETS_DIR'): dirs_to_create.append(context.ASSETS_DIR)

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
