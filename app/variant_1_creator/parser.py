from bs4 import BeautifulSoup
from .helpers import identify_store

def get_parser(url: str):
    """
    Returns the appropriate parser function based on URL.
    """
    store = identify_store(url)

    if store == "play_store":
        return parse_google_play
    elif store == "app_store":
        return parse_app_store

def parse_google_play(soup: BeautifulSoup, app_url) -> dict:
    """
    Parser for google play links
    """
    # Title
    title_tag = soup.select_one('span[itemprop="name"]')
    title = None
    
    if title_tag:
        # Filter out tags, keeping only the text parts
        title_parts = [part for part in title_tag.contents if isinstance(part, str)]
        title = ''.join(title_parts).strip()
        title = title.replace('{', '{{').replace('}', '}}')


    # Description
    desc_tag = soup.select_one("div[data-g-id='description']")
    if desc_tag:
        description = desc_tag.get_text(separator='<br>').strip()
        description = description.replace('{', '{{').replace('}', '}}')
    else:
        description = None

    # Icon URL
    icon_img = soup.select_one("img[alt='Icon image']")
    icon_url = icon_img['src'] if icon_img and icon_img.get('src') else None

    # Screenshot images
    screenshot_imgs = soup.select("img[alt='Screenshot image']")
    screenshot_urls = [img['src'] for img in screenshot_imgs if img.get('src')]
    
    return {
        'title': title,
        'description': description,
        'icon_url': icon_url,
        'screenshot_urls': screenshot_urls,
        'app_url': app_url
    }

def parse_app_store(soup: BeautifulSoup, app_url) -> dict:
    """
    Parser for app store links
    """
    # Title
    title_tag = soup.select_one('h1.product-header__title')
    title = None
    
    if title_tag:
        # Filter out tags, keeping only the text parts
        title_parts = [part for part in title_tag.contents if isinstance(part, str)]
        title = ''.join(title_parts).strip()
        title = title.replace('{', '{{').replace('}', '}}')

    # Description
    description = None
    
    desc_tag = soup.select_one('div.section__description p')
    
    if desc_tag:
        description = desc_tag.get_text(separator='<br>').strip()
        description = description.replace('{', '{{').replace('}', '}}')

    # Icon
    picture = soup.select_one("picture.we-artwork--ios-app-icon")

    # Find the source with PNG type
    source_png = None
    if picture:
        source_png = picture.find("source", attrs={"type": "image/png"})

    # Parse the srcset and get the largest URL
    icon_url = None
    if source_png:
        srcset = source_png.get("srcset")
        urls = [url.strip().split(" ")[0] for url in srcset.split(",")]
        icon_url = urls[-1]  # Get the largest (last) image

    # Screenshots
    ul = soup.select_one("ul.we-screenshot-viewer__screenshots-list")
    screenshot_urls = []

    if ul:
        for li in ul.select('li'):
            source = li.select_one('source')
            if source and source.has_attr('srcset'):
                srcset = source['srcset']
                urls = [url.strip().split(' ')[0] for url in srcset.split(',')]
                if urls:
                    last_url = urls[-1]
                    screenshot_urls.append(last_url)

    return {
        'title': title, 
        'description': description,
        'icon_url': icon_url,
        'screenshot_urls': screenshot_urls,
        'app_url': app_url
    }


def generate_data():
    """
    Generating example data from a...
    """
    #TODO Generation for same return as parsers
    pass