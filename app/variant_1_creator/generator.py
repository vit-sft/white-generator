import os
import aiofiles
from aiohttp import ClientSession
from core.config import CSS_CONTENT, JS_CONTENT, render_html
import pathlib

APP_DIR = pathlib.Path(__file__).parent.parent
DIST_DIR = str(APP_DIR.parent / "dist")
STATIC_DIR = os.path.join(DIST_DIR, "static")
IMG_DIR = os.path.join(STATIC_DIR, "img")
CSS_DIR = os.path.join(STATIC_DIR, "css")
JS_DIR = os.path.join(STATIC_DIR, "js")


async def download_images(urls, dst_folder):
    os.makedirs(dst_folder, exist_ok=True)
    dst_paths = []
    async with ClientSession() as session:
        for i, url in enumerate(urls, start=1):
            ext = os.path.splitext(url)[1] or ".webp"
            filename = f"{i}.webp"
            dst = os.path.join(dst_folder, filename)
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(dst, "wb") as f:
                        await f.write(await resp.read())
                    dst_paths.append(dst)
    return dst_paths

async def build_site(data):
    # Ensure directories exist
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(CSS_DIR, exist_ok=True)
    os.makedirs(JS_DIR, exist_ok=True)

    # Remove old images in IMG_DIR
    for fname in os.listdir(IMG_DIR):
        fpath = os.path.join(IMG_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)

    # Download screenshots to /static/img
    screenshot_files = await download_images(data['screenshot_urls'], IMG_DIR)

    # Download icon to /static/img/icon.webp
    icon_path = os.path.join(IMG_DIR, "icon.webp")
    async with ClientSession() as session:
        async with session.get(data['icon_url']) as resp:
            if resp.status == 200:
                async with aiofiles.open(icon_path, "wb") as f:
                    await f.write(await resp.read())
            else:
                icon_path = data['icon_url']  # fallback to remote

    # Write CSS and JS (always rewrite)
    async with aiofiles.open(os.path.join(CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        await f.write(CSS_CONTENT)
    async with aiofiles.open(os.path.join(JS_DIR, "main.js"), "w", encoding="utf-8") as f:
        await f.write(JS_CONTENT)

    # Build HTML (always rewrite)
    screenshots_html = "\n".join(
        f'<img src="static/img/{os.path.basename(p)}" alt="Screenshot {i+1}">'
        for i, p in enumerate(screenshot_files)
    )
    html = render_html(data=data, screenshots_html=screenshots_html)
    async with aiofiles.open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        await f.write(html)
