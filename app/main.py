from aiohttp import ClientSession, client_exceptions, ClientError
from bs4 import BeautifulSoup
import asyncio
from variant_1_creator.parser import get_parser
from variant_1_creator.generator import build_site

async def fetch_html(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    try:
        async with session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.text()
    except client_exceptions.InvalidURL as e:
        raise client_exceptions.InvalidURL(f"Invalid URL: {url} - {e}")
    except ClientError as e:
        raise ClientError(f"An aiohttp client error occurred for {url}: {e}")


async def build_app_site(url: str):
    
    if url:
        async with ClientSession() as session:
            html = await fetch_html(session, url)
            if html is None:
                # If fetching failed, fallback to parser with empty HTML
                parser = get_parser(url)
                soup = BeautifulSoup("", 'html.parser')
                data = parser(soup, url)
                abs_path = await build_site(data)
                return abs_path

            parser = get_parser(url)
            soup = BeautifulSoup(html, 'html.parser')
            data = parser(soup, url)
            abs_path = await build_site(data)
            return abs_path
        
    # Handler for an empty or invalid link: use parser directly with empty HTML       
    parser = get_parser(url)
    soup = BeautifulSoup("", 'html.parser')
    data = parser(soup, url)
    abs_path = await build_site(data)
    return abs_path

if __name__ == "__main__":
    app_url = "https://apps.apple.com/ua/app/chatgpt/id6448311069"
    # app_url = "fdsfsdfsdfsd"
    # app_url = 'https://play.google.com/store/apps/details?id=com.miHoYo.GenshinImpact&pcampaignid=merch_published_cluster_promotion_battlestar_featured_games'
    # app_url = "https://play.google.com/store/apps/details?id=ua.slando"
    abs_path = asyncio.run(build_app_site(app_url))
    print(abs_path)
