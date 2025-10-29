from typing import List
from pydantic import BaseModel, Field

class AppData(BaseModel):
    """
    Schema for storing app data loaded from a local JSON file.
    Contains Base64-encoded image data rather than URLs.
    """
    title: str
    description: str
    icon_data: str = Field(..., description="Base64-encoded icon image")
    screenshots_data: List[str] = Field(..., description="List of Base64-encoded screenshots")
    app_url: str = Field(default='about:blank" target="_blank', description="Default URL to open app preview or external link")

class AppUrlData(BaseModel):
    """
    Schema for app data fetched directly from URL.
    Contains image URLs rather than encoded data.
    """
    title: str
    description: str
    icon_url: str = Field(..., description="Url to get icon image")
    screenshot_urls: List[str] = Field(..., description="List of urls for screenshots")
    app_url: str = Field(..., description="URL to open app and get values from")