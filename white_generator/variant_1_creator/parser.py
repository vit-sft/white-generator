from bs4 import BeautifulSoup
from white_generator.variant_1_creator.helpers import identify_store
from white_generator.variant_1_creator.schemas import AppUrlData


def get_parser(url: str):
    """
    Returns the appropriate parser function based on URL.
    """
    store = identify_store(url)

    if store == "play_store":
        return parse_google_play
    elif store == "app_store":
        return parse_app_store


def parse_google_play(soup: BeautifulSoup, app_url: str) -> AppUrlData:
    """
    Parser for google play links
    """
    # Title
    title_tag = soup.select_one('span[itemprop="name"]')
    title = None

    if title_tag:
        # Filter out tags, keeping only the text parts
        title_parts = [part for part in title_tag.contents if isinstance(part, str)]
        title = "".join(title_parts).strip()
        title = title.replace("{", "{{").replace("}", "}}")

    # Description
    desc_tag = soup.select_one("div[data-g-id='description']")
    if desc_tag:
        description = desc_tag.get_text(separator="<br>").strip()
        description = description.replace("{", "{{").replace("}", "}}")
    else:
        description = None

    # Icon URL
    images = soup.select("img[itemprop='image']")
    icon_img = images[1]
    if icon_img:
        icon_url = None
        if icon_img.get("srcset"):
            icon_url = icon_img["srcset"].split()[-2]
        elif icon_img.get("src"):
            icon_url = icon_img["src"]
    else:
        icon_url = None

    # Screenshot images
    screenshot_imgs = images[3:] if len(images) > 3 else []
    screenshot_urls = []
    for img in screenshot_imgs:
        if img.get("srcset"):
            # Use the high-res (2x) image
            screenshot_urls.append(img["srcset"].split()[-2])
        elif img.get("src"):
            screenshot_urls.append(img["src"])

    return AppUrlData(
        title=title,
        description=description,
        icon_url=icon_url,
        screenshot_urls=screenshot_urls,
        app_url=app_url,
    )


def parse_app_store(soup: BeautifulSoup, app_url: str) -> AppUrlData:
    """
    Parser for app store links
    """
    # Title
    title_tag = soup.select_one("h1")
    title = None

    if title_tag:
        # Filter out tags, keeping only the text parts
        title_parts = [part for part in title_tag.contents if isinstance(part, str)]
        title = "".join(title_parts).strip()
        title = title.replace("{", "{{").replace("}", "}}")

    # Description
    description = None

    desc_tag = soup.select_one("section article p")

    if desc_tag:
        description = desc_tag.get_text(separator="<br>").strip()
        description = description.replace("{", "{{").replace("}", "}}")

    # # Icon
    # picture = soup.select_one('[role="presentation"]')

    # # Find the source with PNG type
    # source_png = None
    # if picture:
    #     source_png = picture.find("source", attrs={"type": "image/png"})

    icon_img = soup.select_one('[type="image/webp"][srcset]')
    # Parse the srcset and get the largest URL
    icon_url = None

    if icon_img:
        srcset = icon_img.get("srcset")
        urls = [url.strip().split(" ")[0] for url in srcset.split(",")]
        icon_url = urls[-1]  # Get the largest (last) image

    # # Screenshots
    ul = soup.select('section div ul')[1]

    screenshot_urls = []

    if ul:
        for li in ul.select("li"):
            source = li.select_one("source")
            if source and source.has_attr("srcset"):
                srcset = source["srcset"]
                urls = [url.strip().split(" ")[0] for url in srcset.split(",")]
                if urls:
                    last_url = urls[-1]
                    screenshot_urls.append(last_url)

    return AppUrlData(
        title=title,
        description=description,
        icon_url=icon_url,
        screenshot_urls=screenshot_urls,
        app_url=app_url,
    )
