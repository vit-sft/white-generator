from white_generator.core.config import config
from urllib.parse import urlencode
from google import genai
from google.genai import types
from google.api_core import exceptions as google_exceptions
from aiohttp import ClientSession, client_exceptions, ClientError
import random
import asyncio
from white_generator.variant_1_creator.schemas import AppUrlData


class AppDataGenerator:
    """
    Async client for app data generation. 
    Has to be in async with statement. 
    """

    def __init__(self, img_cx: str, img_api_token: str, llm_api_key: str):
        self.img_cx = img_cx
        self.img_api_token = img_api_token
        self.llm_api_key = llm_api_key
        self._session: ClientSession | None = None
        self._llm_client = genai.Client(api_key=self.llm_api_key)

    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get_images_query(self, query: str, quantity: int):
        """
        Fetches image URLs from Google Search.
        """

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        all_images = []

        params = {
            "q": query,
            "cx": self.img_cx,
            "key": self.img_api_token,
            "searchType": "image",
            "safe": "off",
            "num": quantity,
            "start": 1,
        }

        url = f"https://www.googleapis.com/customsearch/v1?{urlencode(params)}"
        try:
            async with self._session.get(url, headers=headers) as resp:
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
            raise ValueError(f"The provided URL seems invalid: '{url}'. ")

        except client_exceptions.ClientConnectorError:
            raise ConnectionError(
                f"Could not connect to '{url}'. Check your internet connection or verify that the API is reachable."
            )

        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while fetching '{url}': {str(e)}"
            )

    async def generate_app_desc(self, app_name):
        model = config.LLM_MODEL
        promt = f"Write a short, engaging app store description for an app called '{app_name}'."
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
            async for (
                chunk
            ) in await self._llm_client.aio.models.generate_content_stream(
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

    async def generate_data(self, generation_query: str) -> AppUrlData:
        """
        Generating data from an image API and LLM API
        """
        icon_query = generation_query + " square logo"
        screenshots_query = generation_query + " slots play"

        icon_task = asyncio.create_task(self.get_images_query(icon_query, 1))
        screenshots_task = asyncio.create_task(
            self.get_images_query(screenshots_query, random.randint(4, 8))
        )
        desc_task = asyncio.create_task(self.generate_app_desc(generation_query))

        icon_url, screenshot_urls, description = await asyncio.gather(
            icon_task, screenshots_task, desc_task
        )
        return AppUrlData(
            title=generation_query,
            description=description,
            icon_url=icon_url[0],
            screenshot_urls=screenshot_urls,
            app_url='about:blank" target="_blank',
        )
