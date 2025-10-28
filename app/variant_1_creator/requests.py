from aiohttp import ClientSession, client_exceptions
from .helpers import identify_store, format_error_message
from app.core.config import IMG_API_TOKEN, LLM_API_KEY, LLM_MODEL
from urllib.parse import urlencode
from google import genai
from google.genai import types


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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    params = {
        "page": 1,
        "per_page": quantity,
        "query": query,
        "client_id": IMG_API_TOKEN,
    }
    url = f"https://api.unsplash.com/search/photos?{urlencode(params)}"
    try:
        async with session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return [img["urls"]["regular"] for img in data.get("results", [])]

    except client_exceptions.InvalidURL:
        raise ValueError(
            f"The provided URL seems invalid: '{url}'. "
            f"Please ensure it includes 'https://' and points to an image API."
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
Do not use Markdown. Write as html with html tags.
"""
            ),
        ],
    )
    chunks = []
    async for chunk in await client.aio.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            chunks.append(chunk.text)

    result = "".join(chunks)

    description = result.replace("{", "{{").replace("}", "}}")

    return description
        
