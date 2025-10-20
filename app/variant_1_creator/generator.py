import os
import aiofiles
from aiohttp import ClientSession
import asyncio
from core.config import DIST_DIR, STATIC_DIR, IMG_DIR, CSS_DIR, FONTS_DIR
import hashlib
import random
from .styles import get_random_style, get_font_face
from .utils import copy_all_files
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
PRESETS_IMG_DIR = os.path.join(BASE_DIR, "presets/images")

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
        await f.write(content)
    
async def load_files(template_dir: str) -> list[str]:
    """
    Function for readings files in async from random template's folder
    """
    index_path = os.path.join(template_dir, "index.html")
    css_path = os.path.join(template_dir, "style.css")
    index_content, css_content = await asyncio.gather(
        read_file(index_path),
        read_file(css_path)
    )

    return index_content, css_content

async def download_image(url: str, filename=None) -> str:
    """
    Downloads an image from url into img directory and hashes it's name 
    """
    if not url:
        return None
    
    async with ClientSession() as session:
        ext = os.path.splitext(url)[1] or ".webp"
        url_hash = hashlib.md5(url.encode()).hexdigest()
        if not filename:
            filename = f"{url_hash}{ext}"
        dst = os.path.join(IMG_DIR, filename)
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(dst, "wb") as f:
                    await f.write(await resp.read())
    return dst

async def build_site(data: dict) -> str:
    """
    Builds a sife from a given data into a DIST_DIR folder
    """
    if os.path.isdir(DIST_DIR):
        shutil.rmtree(DIST_DIR)
        
    dirs_to_create = [DIST_DIR, STATIC_DIR, IMG_DIR, CSS_DIR, FONTS_DIR]

    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
    
    #For random dir
    # chosen_template = random.choice(os.listdir(TEMPLATES_DIR))
    # template_dir = os.path.join(TEMPLATES_DIR, chosen_template)

    template_dir = 'C:\\Users\\u1-1824\\Desktop\\Projects\\app\\variant_1_creator\\templates\\1'
    
    # Download screenshots and icon to /static/img
    screenshot_tasks = [download_image(url) for url in data['screenshot_urls']]
    icon_task = download_image(data['icon_url'], filename="icon.webp")
    
    results = await asyncio.gather(*screenshot_tasks, icon_task)
    
    screenshot_files = results[:-1]
    icon_path = results[-1]

    index_content, css_content = await load_files(template_dir)
    
    # Build HTML
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i+1}"></div>'
        for i, p in enumerate(screenshot_files)
    )
    components_path = os.path.join(template_dir, "components")

    component_files = os.listdir(components_path)
    random.shuffle(component_files)
    components = [await read_file(os.path.join(components_path, component_file)) for component_file in component_files]

    
    title = data['title']
    description = data['description']
    logo_path = ""
    
    if icon_path:
        logo_path = f"static/img/{os.path.basename(icon_path)}"
        
    app_url = data['app_url']
    
    styles = get_random_style()
    root_element = styles['root_element']
    chosen_font, font_dir = styles['font']
    
    font_face = get_font_face(chosen_font, font_dir)
    
    index_path = (os.path.join(DIST_DIR, "index.html"))
    css_path = (os.path.join(CSS_DIR, "style.css"))
    fonts_path = (os.path.join(FONTS_DIR, chosen_font))
    
    # Join all components into one HTML string
    components_html = ''.join(components)
    index_content = index_content.format(
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html
    )
    index_content = index_content.format(
        description_html=description,
        screenshots_html=screenshots_html,
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html
    )
    
    css_content = '\n'.join([root_element, font_face, css_content])
    
    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        copy_all_files(font_dir, fonts_path),
        copy_all_files(PRESETS_IMG_DIR, IMG_DIR)
    )
    
    return os.path.abspath(DIST_DIR)