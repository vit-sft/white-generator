from aiohttp import ClientSession, client_exceptions
from bs4 import BeautifulSoup
import asyncio
from .variant_1_creator.parser import get_parser, generate_data
from .variant_1_creator.generator import build_site_from_parser, build_site_from_data
from .variant_1_creator.helpers import identify_store, format_error_message
from .variant_1_creator.types import AppData
from typing import Optional, Literal
import json

async def fetch_html(session, url: str) -> str:
    """Fetch and return HTML from an App Store or Play Store URL with friendly error handling."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        async with session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.text()

    except client_exceptions.InvalidURL:
        raise ValueError(
            f"The provided URL seems invalid: '{url}'. "
            f"Please ensure it includes 'https://' and points to an app store page."
        )

    except client_exceptions.ClientConnectorError:
        raise ConnectionError(
            f"Could not connect to '{url}'. Check your internet connection or verify that the store is reachable."
        )

    except client_exceptions.ClientResponseError as e:
        store = identify_store(url)
        msg = format_error_message(e.status, store)
        raise RuntimeError(f"Error fetching '{url}': {msg}")

    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred while fetching '{url}': {str(e)}"
        )


async def build_from_app_data(app_data: AppData) -> str:
    """
    Build a site using pre-existing application data.
    """
    app_data["app_url"] = 'about:blank" target="_blank'
    return await build_site_from_data(app_data)


async def build_from_generated_data(generation_query) -> str:
    """
    Generate new data and build a site from it.
    """
    data = await generate_data()
    return await build_site_from_data(data)


async def build_from_url(url: str) -> str:
    """
    Fetch HTML content from a URL and build a site from the parsed information.
    """
    async with ClientSession() as session:
        html = await fetch_html(session, url)
        parser = get_parser(url)
        soup = BeautifulSoup(html, "html.parser")
        data = parser(soup, url)

        if any(d is None for d in data.values()):
            raise ValueError(
                "Data has None values — parser couldn’t get data from link"
            )

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
