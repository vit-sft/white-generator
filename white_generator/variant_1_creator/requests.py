from aiohttp import ClientSession, client_exceptions
from white_generator.variant_1_creator.helpers import identify_store, format_error_message


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
