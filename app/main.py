import json
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import Optional, Literal
from .variant_1_creator.parser import get_parser, generate_data
from .variant_1_creator.generator import build_site_from_parser, build_site_from_data
from .variant_1_creator.requests import fetch_html
from .variant_1_creator.schemas import AppData



async def build_from_app_data(app_data: AppData) -> str:
    """
    Build a site using pre-existing application data.
    """
    if isinstance(app_data, dict):
        app_data = AppData(**app_data)

    return await build_site_from_data(app_data)


async def build_from_generated_data(generation_query: str) -> str:
    """
    Generate new data and build a site from it.
    """
    data = await generate_data(generation_query)
    return await build_site_from_parser(data)


async def build_from_url(url: str) -> str:
    """
    Fetch HTML content from a URL and build a site from the parsed information.
    """
    async with ClientSession() as session:
        html = await fetch_html(session, url)
        parser = get_parser(url)
        soup = BeautifulSoup(html, "html.parser")
        data = parser(soup, url)

        return await build_site_from_parser(data)


async def build_app_site(
    mode: Literal["app_data", "to_generate_data", "url"],
    generation_query: Optional[str] = None,
    app_data: Optional[AppData] = None,
    url: Optional[str] = None,
) -> str:
    match mode:
        case "app_data":
            if app_data:
                return await build_from_app_data(app_data)
            raise ValueError("In Data mode you need to put data")
        case "to_generate_data":
            if generation_query:
                return await build_from_generated_data(generation_query)
            raise ValueError("In Generation mode you need to put generation query")
        case "url":
            if url:
                return await build_from_url(url)
            raise ValueError("In URL mode you need to put url")
        case _:
            raise ValueError(f"Invalid build mode: {mode}")


if __name__ == "__main__":
    with open("app/core/test.json", "r") as f:
        conf_data = json.load(f)

    abs_path = asyncio.run(build_app_site(**conf_data))
    print(abs_path)
