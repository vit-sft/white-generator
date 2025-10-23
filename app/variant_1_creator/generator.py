import os
import asyncio
import hashlib
import base64
from app.core.config import (
    DIST_DIR,
    STATIC_DIR,
    IMG_DIR,
    CSS_DIR,
    JS_DIR,
    FONTS_DIR,
    COOKIE_DIR,
)
import random
from .styles import get_random_style, get_font_face
from app.utils import copy_all_files, build_directories, copy_file_async
from .helpers import (
    identify_store,
    write_file,
    write_bytes_file,
    read_file,
    load_files,
    download_image,
    choose_random_template,
    PRESETS_IMG_DIR,
)


async def build_site_from_parser(data: dict) -> str:
    """
    Builds a site from a parser data into a DIST_DIR folder
    """

    build_directories()

    # For random template dir
    template_dir = choose_random_template()
    # template_dir = 'C:\\Users\\u1-1824\\Desktop\\Projects\\app\\variant_1_creator\\templates\\4'

    # Download screenshots and icon to /static/img
    screenshot_tasks = [download_image(url) for url in data["screenshot_urls"]]
    icon_task = download_image(data["icon_url"], filename="icon.webp")

    # Gathering async tasks to await
    results = await asyncio.gather(*screenshot_tasks, icon_task)

    screenshot_files = results[:-1]
    icon_path = results[-1]

    # Reading template files
    index_content, css_content, cookie_css_content = await load_files(template_dir)

    # Build HTML
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i + 1}"></div>'
        for i, p in enumerate(screenshot_files)
    )
    components_path = os.path.join(template_dir, "components")
    cookie_html_src = os.path.join(COOKIE_DIR, "cookie.html")

    component_files = os.listdir(components_path)
    random.shuffle(component_files)

    results = await asyncio.gather(
        *[
            read_file(os.path.join(components_path, component_file))
            for component_file in component_files
        ],
        read_file(cookie_html_src),
    )
    *components, cookie_component = results

    # Preparing data to parse
    title = data["title"]
    description = data["description"]
    logo_path = ""

    if icon_path:
        logo_path = f"static/img/{os.path.basename(icon_path)}"

    app_url = data["app_url"]

    styles = get_random_style()
    root_element = styles["root_element"]
    chosen_font, font_dir = styles["font"]

    font_face = get_font_face(chosen_font, font_dir)

    index_path = os.path.join(DIST_DIR, "index.html")
    css_path = os.path.join(CSS_DIR, "style.css")
    fonts_path = os.path.join(FONTS_DIR, chosen_font)

    store = identify_store(app_url)

    if store == "play_store":
        badge = "badge-google-market.png"
    elif store == "app_store":
        badge = "badge-apple-store.png"
    else:
        badge = "badge-download.png"

    preview_img = os.path.basename(screenshot_files[0])

    # Join all components into one HTML string
    components_html = "".join(components)
    index_content = index_content.format(
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html,
        cookie_html=cookie_component,
        badge=badge,
        preview_img=preview_img,
    )
    index_content = index_content.format(
        description_html=description,
        screenshots_html=screenshots_html,
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html,
        cookie_html=cookie_component,
        badge=badge,
        preview_img=preview_img,
    )

    css_content = "\n".join([root_element, font_face, css_content, cookie_css_content])

    cookie_js_src = os.path.join(COOKIE_DIR, "cookie.js")

    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        copy_file_async(cookie_js_src, JS_DIR),
        copy_all_files(font_dir, fonts_path),
        copy_all_files(PRESETS_IMG_DIR, IMG_DIR),
    )

    return os.path.abspath(DIST_DIR)


async def build_site_from_data(data: dict) -> str:
    """
    Builds a site from a pre-existing application data into a DIST_DIR folder
    """
    build_directories()

    # For random template dir
    template_dir = choose_random_template()

    # Gathering async tasks to await
    screenshot_tasks = []

    for screenshot_data in data["screenshots_data"]:
        filename = hashlib.md5(screenshot_data.encode()).hexdigest() + ".webp"
        screenshot_data = base64.b64decode(screenshot_data)
        dst = os.path.join(IMG_DIR, filename)
        screenshot_tasks.append(write_bytes_file(dst, screenshot_data))

    icon_data = data["icon_data"]
    icon_data = base64.b64decode(icon_data)
    filename = "icon.webp"
    icon_dst = os.path.join(IMG_DIR, filename)

    icon_task = write_bytes_file(icon_dst, icon_data)

    results = await asyncio.gather(*screenshot_tasks, icon_task)

    screenshot_files = results[:-1]
    icon_path = results[-1]

    index_content, css_content, cookie_css_content = await load_files(template_dir)

    # Build HTML
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i + 1}"></div>'
        for i, p in enumerate(screenshot_files)
    )
    components_path = os.path.join(template_dir, "components")
    cookie_html_src = os.path.join(COOKIE_DIR, "cookie.html")

    component_files = os.listdir(components_path)
    random.shuffle(component_files)

    results = await asyncio.gather(
        *[
            read_file(os.path.join(components_path, component_file))
            for component_file in component_files
        ],
        read_file(cookie_html_src),
    )
    *components, cookie_component = results

    # Preparing data to parse
    title = data["title"]
    description = data["description"]
    logo_path = ""

    if icon_path:
        logo_path = f"static/img/{os.path.basename(icon_path)}"

    app_url = data["app_url"]

    styles = get_random_style()
    root_element = styles["root_element"]
    chosen_font, font_dir = styles["font"]

    font_face = get_font_face(chosen_font, font_dir)

    index_path = os.path.join(DIST_DIR, "index.html")
    css_path = os.path.join(CSS_DIR, "style.css")
    fonts_path = os.path.join(FONTS_DIR, chosen_font)

    badge = "badge-download.png"

    preview_img = os.path.basename(screenshot_files[0])

    # Join all components into one HTML string
    components_html = "".join(components)
    index_content = index_content.format(
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html,
        cookie_html=cookie_component,
        badge=badge,
        preview_img=preview_img,
    )
    index_content = index_content.format(
        description_html=description,
        screenshots_html=screenshots_html,
        title=title,
        app_url=app_url,
        logo_path=logo_path,
        components_html=components_html,
        cookie_html=cookie_component,
        badge=badge,
        preview_img=preview_img,
    )

    css_content = "\n".join([root_element, font_face, css_content, cookie_css_content])

    cookie_js_src = os.path.join(COOKIE_DIR, "cookie.js")

    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        copy_file_async(cookie_js_src, JS_DIR),
        copy_all_files(font_dir, fonts_path),
        copy_all_files(PRESETS_IMG_DIR, IMG_DIR),
    )

    return os.path.abspath(DIST_DIR)
