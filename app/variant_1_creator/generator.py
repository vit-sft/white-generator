import os
import aiofiles
from aiohttp import ClientSession
import asyncio
from core.config import DIST_DIR, STATIC_DIR, IMG_DIR, CSS_DIR, JS_DIR
import hashlib
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

async def read_file(path: str) -> str:
    """
    Function for reading a file by it's path. Returns str with content
    """
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        return await f.read()

async def write_file(path: str, content: str):
    """
    Function for writing a file by it's path and content with kwargs for formatting file.
    """
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        # if format_kwargs:
        #     content = content.format(**format_kwargs)
        await f.write(content)
    
async def load_files(template_dir: str) -> list[str]:
    """
    Function for readings files in async from random template's folder
    """
    index_path = os.path.join(template_dir, "index.html")
    css_path = os.path.join(template_dir, "style.css")
    js_path = os.path.join(template_dir, "main.js")

    index_content, css_content, js_content = await asyncio.gather(
        read_file(index_path),
        read_file(css_path),
        read_file(js_path)
    )

    return index_content, css_content, js_content

async def download_image(url: str) -> str:
    """
    Downloads an image from url into img directory and hashes it's name 
    """
    async with ClientSession() as session:
        ext = os.path.splitext(url)[1] or ".webp"
        url_hash = hashlib.md5(url.encode()).hexdigest()
        filename = f"{url_hash}{ext}"
        dst = os.path.join(IMG_DIR, filename)
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(dst, "wb") as f:
                    await f.write(await resp.read())
    return dst

async def build_site(data: dict, styles: dict):
    """
    Builds a sife from a given data into a DIST_DIR folder
    """
    # Ensure directories exist
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(CSS_DIR, exist_ok=True)
    os.makedirs(JS_DIR, exist_ok=True)

    chosen_template = random.choice(os.listdir(TEMPLATES_DIR))
    template_dir = os.path.join(TEMPLATES_DIR, chosen_template)
    
    # Remove old images in IMG_DIR
    for fname in os.listdir(IMG_DIR):
        fpath = os.path.join(IMG_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)

    # Download screenshots to /static/img
    tasks = [download_image(url) for url in data['screenshot_urls']]
    
    screenshot_files = await asyncio.gather(*tasks)

    # Download icon to /static/img/icon.webp
    icon_path = os.path.join(IMG_DIR, "icon.webp")
    async with ClientSession() as session:
        async with session.get(data['icon_url']) as resp:
            if resp.status == 200:
                async with aiofiles.open(icon_path, "wb") as f:
                    await f.write(await resp.read())
            else:
                icon_path = data['icon_url']

    # Read HTML, CSS, JS
    index_content, css_content, js_content = await load_files(template_dir)
    
    # Build HTML
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i+1}"></div>'
        for i, p in enumerate(screenshot_files)
    )
    components_path = os.path.join(template_dir, "components")

    component_files = os.listdir(components_path)
    random.shuffle(component_files)
    components = [await read_file(os.path.join(components_path, component_file)) for component_file in component_files]

    index_path = (os.path.join(DIST_DIR, "index.html"))
    css_path = (os.path.join(CSS_DIR, "style.css"))
    js_path = (os.path.join(JS_DIR, "main.js"))

    title = data['title']
    description = data['description']
    logo_path = f"static/img/{os.path.basename(icon_path)}"
    app_url = data['app_url']
    
    font_url = styles['font_url']
    root_element = styles['root_element']

    # Join all components into one HTML string
    components_html = ''.join(components)
    index_content = index_content.format(
        font_url=font_url,
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html
    )
    index_content = index_content.format(
        description_html=description,
        screenshots_html=screenshots_html,
        font_url=font_url,
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html
    )
    
    css_content = root_element + '\n' + css_content
    
    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        write_file(js_path, js_content)
    )