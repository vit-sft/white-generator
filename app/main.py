from aiohttp import ClientSession, client_exceptions, ClientError
from bs4 import BeautifulSoup
import asyncio
from .variant_1_creator.parser import get_parser, generate_data
from .variant_1_creator.generator import build_site
from .variant_1_creator.helpers import identify_store, format_error_message

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
        raise RuntimeError(f"An unexpected error occurred while fetching '{url}': {str(e)}")

async def build_app_site(use_auto_generation: bool, url: str = None) -> str:
    
    if url:
        async with ClientSession() as session:
            html = await fetch_html(session, url)
            parser = get_parser(url)
            soup = BeautifulSoup(html, 'html.parser')
            data = parser(soup, url)
            abs_path = await build_site(data)
            return abs_path
    
    # If we want to generate data for site
    if use_auto_generation:       
        generated_data = generate_data()
        abs_path = await build_site(generated_data)
        return abs_path
    
    raise ValueError("You must provide either a URL or enable auto-generation.")

if __name__ == "__main__":
    generate = False
    # app_url = "https://apps.apple.com/ua/app/chatgpt/id6448311069"
    # app_url = "https://itunes.apple.com/ua/app/chatgpt/id6448311069"
    # app_url = "fdsfsdfsdfsd"
    # app_url = "https://play.google.com/store/apps/details?id=cfsdfsd"
    # app_url = 'https://play.google.com/store/apps/details?id=com.miHoYo.GenshinImpact&pcampaignid=merch_published_cluster_promotion_battlestar_featured_games'
    # app_url = "https://play.google.com/store/apps/details?id=ua.slando"
    app_url = "https://market.android.com/details?id=com.google.earth"
    abs_path = asyncio.run(build_app_site(generate, app_url))
    print(abs_path)
