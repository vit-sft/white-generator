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


def format_error_message(status: int, store: str | None) -> str:
    """
    Return a message based on HTTP status and store type.
    """
    if status == 400:
        return "Bad Request - the store couldn't process your request properly."
    elif status == 404:
        if store == "play_store":
            return "App not found - it may have been removed from the Google Play Store."
        elif store == "app_store":
            return "App not found - it may have been removed from the Apple App Store."
        return "Page not found - the requested URL doesn't exist."
    elif status == 408:
        return "Request Timeout - the store took too long to respond. Try again shortly."
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