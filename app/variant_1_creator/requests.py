from aiohttp import ClientSession, client_exceptions
from .helpers import identify_store, format_error_message
from app.core.config import IMG_API_TOKEN, IMG_CX, LLM_API_KEY, LLM_MODEL
from urllib.parse import urlencode
from google import genai
from google.genai import types
from google.api_core import exceptions as google_exceptions
from aiohttp import ClientError
import asyncio


async def fetch_html(session: ClientSession, url: str) -> str:
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


async def get_images_query(session: ClientSession, query: str, quantity: int):
    """
    Fetches image URLs from Google Search.
    """

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    all_images = []

    params = {
        "q": query,
        "cx": IMG_CX,
        "key": IMG_API_TOKEN,
        "searchType": "image",
        "safe": "off",
        "num": quantity,
        "start": 1,
    }

    url = f"https://www.googleapis.com/customsearch/v1?{urlencode(params)}"
    try:
        async with session.get(url, headers=headers) as resp:
            
            data = await resp.json()
            if "error" in data:
                error_info = data["error"]
                message = error_info.get("message", "Unknown Google API error")
                code = error_info.get("code", "N/A")
                raise RuntimeError(f"Google API error {code}: {message}")
            
            results = data.get("items", [])
            for item in results:
                link = item.get("link")
                if link:
                    all_images.append(link)

        return all_images

    except client_exceptions.InvalidURL:
        raise ValueError(
            f"The provided URL seems invalid: '{url}'. "
        )

    except client_exceptions.ClientConnectorError:
        raise ConnectionError(
            f"Could not connect to '{url}'. Check your internet connection or verify that the API is reachable."
        )

    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred while fetching '{url}': {str(e)}"
        )


async def generate_app_desc(app_name):
    client = genai.Client(
        api_key=LLM_API_KEY,
    )

    model = LLM_MODEL
    promt = (
        f"Write a short, engaging app store description for an app called '{app_name}'."
    )
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=promt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(
                text="""Role / Purpose:
You are an assistant that writes creative, engaging, and family-friendly descriptions for entertainment apps themed around “slots”, “spinning reels”.

Tone & Style
Use vivid, energetic, and engaging language.
Keep it concise and upbeat — think app-store friendly (≈150–200 words).
Prohibited Language
Avoid words like \"win big”, “earn”, or “gamble.”
Don’t reference risk, odds, or financial gain.
Safety & Policy
All outputs must comply with Google and app store content policies.
Avoid mature, suggestive, or real-world gambling contexts.

Format
Do not use Markdown. Write a html with html tags. Do not use ```html```.
"""
            ),
        ],
    )
    try:
        chunks = []
        async for chunk in await client.aio.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if getattr(chunk, "text", None):
                chunks.append(chunk.text)

        if not chunks:
            raise ValueError("Empty response from LLM — no content generated.")

        result = "".join(chunks)
        description = result.replace("{", "{{").replace("}", "}}")
        return description

    except ClientError as e:
        raise ConnectionError(
            f"Network or HTTP error while calling the GenAI API: {e}"
        ) from e

    except asyncio.TimeoutError:
        raise TimeoutError("The GenAI request timed out. Try again later.")

    except ValueError as e:
        raise ValueError(f"Invalid response from LLM: {e}") from e

    except google_exceptions.ResourceExhausted as e:
        raise google_exceptions.ResourceExhausted(f"Rate limit hit: {e}")
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e
