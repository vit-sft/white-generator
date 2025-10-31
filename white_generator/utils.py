import asyncio
import shutil
import os
from white_generator.core.config import config

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
    dirs_to_create = [config.DIST_DIR, config.STATIC_DIR, config.IMG_DIR, config.CSS_DIR, config.JS_DIR, config.FONTS_DIR]

    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
