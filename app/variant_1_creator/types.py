from typing import TypedDict, Optional, Literal

class AppData(TypedDict):
    """
    Data for creating a site. Icon and screenshots data have to be in base64 format.
    """
    title: str
    description: str
    icon_data: str
    screenshots_data: list[str]
