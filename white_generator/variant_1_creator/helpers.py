import os
from urllib.parse import urlparse
import aiofiles
from aiohttp import ClientSession
from white_generator.core.config import config
from white_generator.variant_1_creator.styles import generate_slot_reels, spin_wheel_colors
import asyncio
import hashlib
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
PRESETS_IMG_DIR = os.path.join(BASE_DIR, "presets/images")


def identify_store(url: str) -> str | None:
    """
    Identify if the URL belongs to Google Play or Apple App Store.
    """
    play_store_domains = ["play.google.com", "market.android.com", "market://"]
    app_store_domains = ["apps.apple.com", "itunes.apple.com", "itms-apps://"]

    if any(domain in url for domain in play_store_domains):
        return "play_store"
    elif any(domain in url for domain in app_store_domains):
        return "app_store"
    return None


async def read_file(path: str) -> str:
    """
    Function for reading a file by it's path. Returns str with content
    """
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        return await f.read()


async def write_file(path: str, content: str) -> str:
    """
    Function for writing a file by it's path and content for file. Returns abs path to a file
    """
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(content)
        return f.name


async def write_bytes_file(path: str, content: bytes) -> str:
    """
    Function for writing a file by it's path and bytes content for file. Returns abs path to a file
    """
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)
        return f.name


async def load_files(template_dir: str, fidget_dir: str) -> tuple[str, str, str, str, str]:
    """
    Function for readings files in async from random template's folder
    """
    index_path = os.path.join(template_dir, "index.html")
    css_path = os.path.join(template_dir, "style.css")
    js_path = os.path.join(template_dir, "main.js")
    cookie_css_src = os.path.join(config.COOKIE_DIR, "cookie.css")
    fidget_css_src = os.path.join(fidget_dir, "fidget.css")
    
    index_content, css_content, js_content, cookie_css, fidget_css = await asyncio.gather(
        read_file(index_path),
        read_file(css_path),
        read_file(js_path),
        read_file(cookie_css_src),
        read_file(fidget_css_src)
    )

    return index_content, css_content, js_content, cookie_css, fidget_css


async def download_image(session: ClientSession, url: str, filename=None) -> str:
    """
    Downloads an image from url into IMG_DIR and hashes its name.
    """
    if not url:
        return ""

    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1] or ".webp"
    if ext.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg"}:
        ext = ".webp"

    url_hash = hashlib.md5(url.encode()).hexdigest()
    if not filename:
        filename = f"{url_hash}{ext}"
    else:
        filename = filename + ext

    os.makedirs(config.IMG_DIR, exist_ok=True)
    dst = os.path.join(config.IMG_DIR, filename)
    try:
        async with session.get(url) as resp:
            if resp.status == 200 and "image" in resp.headers.get("Content-Type", ""):
                async with aiofiles.open(dst, "wb") as f:
                    await f.write(await resp.read())
            else:
                return ""

    except Exception:
        return ""
    return dst


def choose_random_template() -> str:
    """
    Choose random template folder from templates. Get path
    """
    chosen_template = random.choice(os.listdir(TEMPLATES_DIR))
    template_dir = os.path.join(TEMPLATES_DIR, chosen_template)

    return template_dir


def choose_random_fidget_with_params():
    """
    Select a random fidget folder and generate the corresponding parameters.

    Returns:
        fidget_dir (str): Path to the chosen fidget folder.
        params (dict): Dictionary of parameters required for the fidget.
                       - Slot machines: {'num_reels': int, 'slot_symbols': list}
                       - Spin wheel: {'wheel_colors': list}
    """
    
    chosen_fidget = random.choice(os.listdir(config.FIDGETS_DIR))
    fidget_dir = os.path.join(config.FIDGETS_DIR, chosen_fidget)
    
    # Determine parameters based on fidget type
    params = {}
    if "slotmachine" in chosen_fidget.lower():  # for slot machines
        num_reels, slot_symbols = generate_slot_reels()
        params = {
            "num_reels": num_reels,
            "slot_symbols": slot_symbols
        }
    elif "spinwheel" in chosen_fidget.lower():  # for spin wheel
        wheel_colors = spin_wheel_colors()
        params = {
            "wheel_colors": wheel_colors
        }
    
    return fidget_dir, params


def format_error_message(status: int, store: str | None) -> str:
    """
    Return a message based on HTTP status and store type.
    """
    if status == 400:
        return "Bad Request - the store couldn't process your request properly."
    elif status == 404:
        if store == "play_store":
            return (
                "App not found - it may have been removed from the Google Play Store."
            )
        elif store == "app_store":
            return "App not found - it may have been removed from the Apple App Store."
        return "Page not found - the requested URL doesn't exist."
    elif status == 408:
        return (
            "Request Timeout - the store took too long to respond. Try again shortly."
        )
    elif status == 429:
        if store:
            return "Too Many Requests - you've hit the store's rate limit. Please wait a few minutes."
        return "Too Many Requests - the server is rate-limiting you. Please slow down and retry."
    elif 500 <= status < 600:
        if store == "play_store":
            return f"Google Play Store seems to be having issues (HTTP {status}). Try again later."
        elif store == "app_store":
            return f"Apple App Store appears to be down or under maintenance (HTTP {status}). Try again later."
        return f"Server Error (HTTP {status}) - the store returned an internal error. Try again later."
    else:
        return f"Unexpected response - received HTTP {status} from the store."
