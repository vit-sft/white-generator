import asyncio
import shutil
import os

async def copy_file_async(src, dst):
    await asyncio.to_thread(shutil.copy2, src, dst)

async def copy_all_fonts(font_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    tasks = []

    for filename in os.listdir(font_dir):
        if filename.lower().endswith(('.ttf', '.otf', '.woff', '.woff2')):
            src = os.path.join(font_dir, filename)
            dst = os.path.join(dest_dir, filename)
            tasks.append(copy_file_async(src, dst))

    await asyncio.gather(*tasks)
