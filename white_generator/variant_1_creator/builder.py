import os
import asyncio
import hashlib
import base64
import random
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from white_generator.core.config import config
from white_generator.utils import copy_all_files, build_directories, copy_file_async
from white_generator.variant_1_creator.styles import get_random_style, get_font_face
from white_generator.variant_1_creator.helpers import (
    identify_store,
    write_file,
    write_bytes_file,
    read_file,
    load_files,
    download_image,
    choose_random_template,
    PRESETS_IMG_DIR,
    TEMPLATES_DIR,
)
from white_generator.variant_1_creator.adresses import get_random_adress
from white_generator.variant_1_creator.footer import (
    get_use_principles,
    get_terms,
    get_faq,
)
from white_generator.variant_1_creator.schemas import (
    AppData,
    AppUrlData,
    AppGeneratedData,
)
from white_generator.variant_1_creator.parser import get_parser
from white_generator.variant_1_creator.requests import fetch_html
from white_generator.variant_1_creator.generator import AppDataGenerator


class AppBuilder:
    """
    Main builder for different app data variants. Has methods for 3 different types of data:
    AppData, AppUrlData, AppGeneratedData.
    All methods return abs path to a destination directory.
    """

    def __init__(self, template_number: int = None) -> None:
        """Initialisation for builder. Has chosen template in it.

        Args:
            template_number (int): Chosen template number. Default is a random one.
        """
        self._template_dir = (
            os.path.join(TEMPLATES_DIR, str(template_number))
            if template_number
            else choose_random_template()
        )

    async def _build_site_from_parser(self, data: AppUrlData) -> str:
        """
        Builds a site from a parser data into a DIST_DIR folder
        """

        build_directories()

        # Download images
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        async with ClientSession(headers=headers) as session:
            screenshot_tasks = [
                download_image(session, url) for url in data.screenshot_urls
            ]
            icon_task = download_image(session, data.icon_url, filename="icon")
            results = await asyncio.gather(*screenshot_tasks, icon_task)

        screenshot_files = results[:-1]
        icon_path = results[-1]

        return await self._build_site(
            data.title, data.description, icon_path, screenshot_files, data.app_url
        )

    async def _build_site_from_data(self, data: AppData) -> str:
        """
        Builds a site from pre-existing application data into the DIST_DIR folder.
        """
        build_directories()

        # Prepare async tasks for screenshots
        screenshot_tasks = []
        for screenshot_data in data.screenshots_data:
            filename = hashlib.md5(screenshot_data).hexdigest() + ".webp"
            dst = os.path.join(config.IMG_DIR, filename)
            screenshot_tasks.append(
                write_bytes_file(dst, base64.b64decode(screenshot_data))
            )

        # Prepare icon task
        icon_data = base64.b64decode(data.icon_data)
        icon_dst = os.path.join(config.IMG_DIR, "icon.webp")
        icon_task = write_bytes_file(icon_dst, icon_data)

        # Await all image writes
        results = await asyncio.gather(*screenshot_tasks, icon_task)
        screenshot_files = results[:-1]
        icon_path = results[-1]

        return await self._build_site(
            data.title, data.description, icon_path, screenshot_files, data.app_url
        )

    async def _build_site_from_generated(self, data: AppGeneratedData) -> str:
        """
        Builds a site from generated application data (icon in bytes + screenshot URLs)
        into the DIST_DIR folder.
        """

        build_directories()

        # Download screenshots
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            ),
        }

        async with ClientSession(headers=headers) as session:
            screenshot_tasks = [
                download_image(session, url) for url in data.screenshot_urls
            ]
            screenshot_results = await asyncio.gather(*screenshot_tasks)

        # Filter out failed downloads
        screenshot_files = [path for path in screenshot_results if path]

        # Save icon bytes
        icon_dst = os.path.join(config.IMG_DIR, "icon.webp")
        icon_path = await write_bytes_file(icon_dst, data.icon_data)

        return await self._build_site(
            data.title, data.description, icon_path, screenshot_files, data.app_url
        )

    async def _build_site(
        self,
        title: str,
        description: str,
        icon_path: str,
        screenshot_files: str,
        app_url: str,
    ):
        """
        Builds site form ready-to-use data from different parsers
        """
        # Remove failed screenshot paths
        screenshot_files = [path for path in screenshot_files if path]

        if not icon_path and screenshot_files:
            icon_path = screenshot_files[0]

        # Load template files
        index_content, css_content, js_content, cookie_css_content = await load_files(
            self._template_dir
        )

        # Build screenshots HTML
        screenshots_html = "\n".join(
            f'<div><img src="source_target_files/img/{os.path.basename(p)}" alt="Screenshot {i + 1}"></div>'
            for i, p in enumerate(screenshot_files)
        )

        # Load components
        components_path = os.path.join(self._template_dir, "components")
        component_files = os.listdir(components_path)
        random.shuffle(component_files)

        cookie_html_src = os.path.join(config.COOKIE_DIR, "cookie.html")
        component_tasks = [
            read_file(os.path.join(components_path, f)) for f in component_files
        ] + [read_file(cookie_html_src)]
        results = await asyncio.gather(*component_tasks)
        *components, cookie_component = results

        components_html = "".join(components)

        # Prepare app data
        logo_path = (
            f"source_target_files/img/{os.path.basename(icon_path)}"
            if icon_path
            else ""
        )
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
            "background_img": random.choices(
                [preview_img, ""],
                weights=[0.75, 0.25],
                k=1,
            )[0],
            "address_html": address_html,
            "principles_html": principles_html,
            "terms_html": terms_html,
            "faq_html": faq_html,
        }

        # Render HTML
        index_content = index_content.format(**context)
        index_content = index_content.format(**context)

        css_content = "\n".join(
            [root_element, font_face, css_content, cookie_css_content]
        )

        cookie_js_src = os.path.join(config.COOKIE_DIR, "cookie.js")

        index_path = os.path.join(config.DIST_DIR, "source_target.html")
        css_path = os.path.join(config.CSS_DIR, "style.css")
        js_path = os.path.join(config.JS_DIR, "main.js")
        fonts_path = os.path.join(config.FONTS_DIR, chosen_font)

        await asyncio.gather(
            write_file(index_path, index_content),
            write_file(css_path, css_content),
            write_file(js_path, js_content),
            copy_file_async(cookie_js_src, config.JS_DIR),
            copy_all_files(font_dir, fonts_path),
            copy_all_files(PRESETS_IMG_DIR, config.IMG_DIR),
        )

        return os.path.abspath(config.DIST_DIR)

    async def build_from_app_data(self, app_data: dict) -> str:
        """
        Build a site using pre-existing application data.
        """
        if isinstance(app_data, dict):
            app_data = AppData(**app_data)

        return await self._build_site_from_data(app_data)

    async def build_from_generated_data(
        self, generation_query: str, img_cx: str, img_api_token: str, llm_api_key: str
    ) -> str:
        """
        Generate new data and build a site from it.
        """
        async with AppDataGenerator(
            img_cx=img_cx, img_api_token=img_api_token, llm_api_key=llm_api_key
        ) as data_generator:
            data = await data_generator.generate_data(generation_query=generation_query)
        return await self._build_site_from_generated(data)

    async def build_from_url(self, url: str) -> str:
        """
        Fetch HTML content from a URL and build a site from the parsed information.
        """
        async with ClientSession() as session:
            html = await fetch_html(session, url)
            parser = get_parser(url)
            soup = BeautifulSoup(html, "html.parser")
            data = parser(soup, url)
            return await self._build_site_from_parser(data)
