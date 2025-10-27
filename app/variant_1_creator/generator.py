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
from .adresses import get_random_adress
from .footer import get_use_principles, get_terms, get_faq

async def build_site_from_parser(data: dict) -> str:
    """
    Builds a site from a parser data into a DIST_DIR folder
    """

    build_directories()

    # For random template dir
    template_dir = choose_random_template()
    # template_dir = 'C:\\Users\\u1-1824\\Desktop\\Projects\\app\\variant_1_creator\\templates\\5'

    # Download images 
    screenshot_tasks = [download_image(url) for url in data["screenshot_urls"]]
    icon_task = download_image(data["icon_url"], filename="icon.webp")
    results = await asyncio.gather(*screenshot_tasks, icon_task)

    screenshot_files = results[:-1]
    icon_path = results[-1]

    # Load template files
    index_content, css_content, js_content, cookie_css_content = await load_files(template_dir)

    # Build screenshots HTML
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i + 1}"></div>'
        for i, p in enumerate(screenshot_files)
    )

    # Load components
    components_path = os.path.join(template_dir, "components")
    component_files = os.listdir(components_path)
    random.shuffle(component_files)

    cookie_html_src = os.path.join(COOKIE_DIR, "cookie.html")
    component_tasks = [
        read_file(os.path.join(components_path, f)) for f in component_files
    ] + [read_file(cookie_html_src)]
    results = await asyncio.gather(*component_tasks)
    *components, cookie_component = results

    components_html = "".join(components)

    # Prepare app data
    logo_path = f"static/img/{os.path.basename(icon_path)}" if icon_path else ""
    app_url = data["app_url"]
    title = data["title"]
    description = data["description"]
    preview_img = os.path.basename(screenshot_files[0])

    store = identify_store(app_url)
    badge_map = {
        "play_store": "badge-google-market.png",
        "app_store": "badge-apple-store.png",
    }
    badge = badge_map.get(store, "badge-download.png")

    # Random elements
    styles = get_random_style()
    chosen_font, font_dir = styles["font"]
    root_element = styles["root_element"]

    font_face = get_font_face(chosen_font, font_dir)

    address_html = get_random_adress()
    principles_html = get_use_principles()
    terms_html = get_terms()
    faq_html = get_faq()

    # Build context dictionary
    context = {
        "title": title,
        "description_html": description,
        "app_url": app_url,
        "logo_path": logo_path,
        "components_html": components_html,
        "screenshots_html": screenshots_html,
        "cookie_html": cookie_component,
        "badge": badge,
        "preview_img": preview_img,
        "address_html": address_html,
        "principles_html": principles_html,
        "terms_html": terms_html,
        "faq_html": faq_html,
    }

    # Render HTML 
    index_content = index_content.format(**context)
    index_content = index_content.format(**context)
    
    css_content = "\n".join([root_element, font_face, css_content, cookie_css_content])

    cookie_js_src = os.path.join(COOKIE_DIR, "cookie.js")

    index_path = os.path.join(DIST_DIR, "source_target.html")
    css_path = os.path.join(CSS_DIR, "style.css")
    js_path = os.path.join(JS_DIR, "main.js")
    fonts_path = os.path.join(FONTS_DIR, chosen_font)
    
    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        write_file(js_path, js_content),
        copy_file_async(cookie_js_src, JS_DIR),
        copy_all_files(font_dir, fonts_path),
        copy_all_files(PRESETS_IMG_DIR, IMG_DIR),
    )

    return os.path.abspath(DIST_DIR)


async def build_site_from_data(data: dict) -> str:
    """
    Builds a site from pre-existing application data into the DIST_DIR folder.
    """
    build_directories()

    # Choose template 
    template_dir = choose_random_template()

    # Prepare async tasks for screenshots 
    screenshot_tasks = []
    for screenshot_data in data["screenshots_data"]:
        filename = hashlib.md5(screenshot_data.encode()).hexdigest() + ".webp"
        decoded_data = base64.b64decode(screenshot_data)
        dst = os.path.join(IMG_DIR, filename)
        screenshot_tasks.append(write_bytes_file(dst, decoded_data))

    # Prepare icon task 
    icon_data = base64.b64decode(data["icon_data"])
    icon_dst = os.path.join(IMG_DIR, "icon.webp")
    icon_task = write_bytes_file(icon_dst, icon_data)

    # Await all image writes 
    results = await asyncio.gather(*screenshot_tasks, icon_task)
    screenshot_files = results[:-1]
    icon_path = results[-1]

    # Load template files 
    index_content, css_content, js_content, cookie_css_content = await load_files(template_dir)

    # Build screenshots HTML 
    screenshots_html = "\n".join(
        f'<div><img src="static/img/{os.path.basename(p)}" alt="Screenshot {i + 1}"></div>'
        for i, p in enumerate(screenshot_files)
    )

    # Load components
    components_path = os.path.join(template_dir, "components")
    component_files = os.listdir(components_path)
    random.shuffle(component_files)
    cookie_html_src = os.path.join(COOKIE_DIR, "cookie.html")

    component_tasks = [
        read_file(os.path.join(components_path, f)) for f in component_files
    ] + [read_file(cookie_html_src)]

    results = await asyncio.gather(*component_tasks)
    *components, cookie_component = results
    components_html = "".join(components)

    address_html = get_random_adress()
    principles_html = get_use_principles()
    terms_html = get_terms()
    faq_html = get_faq()
    
    # Prepare data for template
    context = {
        "title": data["title"],
        "description_html": data["description"],
        "app_url": data["app_url"],
        "logo_path": f"static/img/{os.path.basename(icon_path)}" if icon_path else "",
        "components_html": components_html,
        "cookie_html": cookie_component,
        "badge": "badge-download.png",
        "preview_img": os.path.basename(screenshot_files[0]),
        "screenshots_html": screenshots_html,
        "address_html": address_html,
        "principles_html": principles_html,
        "terms_html": terms_html,
        "faq_html": faq_html,
    }

    index_content = index_content.format(**context)
    index_content = index_content.format(**context)
    # Prepare CSS 
    styles = get_random_style()
    root_element = styles["root_element"]
    chosen_font, font_dir = styles["font"]
    font_face = get_font_face(chosen_font, font_dir)

    css_content = "\n".join([root_element, font_face, css_content, cookie_css_content])

    index_path = os.path.join(DIST_DIR, "source_target.html")
    css_path = os.path.join(CSS_DIR, "style.css")
    js_path = os.path.join(JS_DIR, "main.js")
    fonts_path = os.path.join(FONTS_DIR, chosen_font)
    cookie_js_src = os.path.join(COOKIE_DIR, "cookie.js")

    await asyncio.gather(
        write_file(index_path, index_content),
        write_file(css_path, css_content),
        write_file(js_path, js_content),
        copy_file_async(cookie_js_src, JS_DIR),
        copy_all_files(font_dir, fonts_path),
        copy_all_files(PRESETS_IMG_DIR, IMG_DIR),
    )

    return os.path.abspath(DIST_DIR)
