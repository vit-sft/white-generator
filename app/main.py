from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
from variant_1_creator.parser import get_parser
from variant_1_creator.generator import build_site

async def fetch_html(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    async with session.get(url, headers=headers) as resp:
        return await resp.text()


async def build_app_site(url: str):
    async with ClientSession() as session:
        
        html = await fetch_html(session, url)
        parser = get_parser(html)
        soup = BeautifulSoup(html, 'html.parser')
        data = parser(soup, url)
        # print(data)

        await build_site(data)
        print(f"Site generated for: {data['title']}")

if __name__ == "__main__":
    app_url = "https://apps.apple.com/ua/app/chatgpt/id6448311069"
    # app_url = 'https://play.google.com/store/apps/details?id=com.miHoYo.GenshinImpact&pcampaignid=merch_published_cluster_promotion_battlestar_featured_games'
    # app_url = "https://play.google.com/store/apps/details?id=ua.slando"
    asyncio.run(build_app_site(app_url))
