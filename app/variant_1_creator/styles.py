import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "presets/fonts")


def get_random_style():
    """
    Selects a random template, color palette, and font for the website build.
    Returns font_url and root for css.
    """

    # list of color palettes
    palettes = {
        "Ocean": {
            "primary": "#00A7E1",
            "secondary": "#F1F1F2",
            "background": "#FFFFFF",
            "text_primary": "#00171F",
            "text_secondary": "#003459",
        },
        "Forest": {
            "primary": "#4A7856",
            "secondary": "#F2EAE4",
            "background": "#FFFFFF",
            "text_primary": "#223326",
            "text_secondary": "#3E5346",
        },
        "Sunset": {
            "primary": "#FF6B6B",
            "secondary": "#FFD166",
            "background": "#FFF9F0",
            "text_primary": "#073B4C",
            "text_secondary": "#118AB2",
        },
        "Charcoal": {
            "primary": "#36454F",
            "secondary": "#F5F5F5",
            "background": "#FFFFFF",
            "text_primary": "#1A1A1A",
            "text_secondary": "#5A5A5A",
        },
        "Royal": {
            "primary": "#4169E1",
            "secondary": "#F0F8FF",
            "background": "#FFFFFF",
            "text_primary": "#00008B",
            "text_secondary": "#191970",
        },
    }
    palette_name = random.choice(list(palettes.keys()))
    chosen_font = random.choice(os.listdir(FONTS_DIR))
    font_dir = os.path.join(FONTS_DIR, chosen_font)

    colors = palettes[palette_name]
    primary = colors["primary"]
    secondary = colors["secondary"]
    background = colors["background"]
    text_primary = colors["text_primary"]
    text_secondary = colors["text_secondary"]

    root_element = f""":root {{
        --font-family: "{chosen_font}", sans-serif;
        --background: {background};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --primary: {primary};
        --secondary: {secondary};
    }}"""

    return {"font": [chosen_font, font_dir], "root_element": root_element}


def get_font_face(chosen_font, font_dir):
    font_files = [f for f in os.listdir(font_dir)]

    if not font_files:
        raise FileNotFoundError(f"No .ttf font files found in {font_dir}")

    css_blocks = []

    for filename in font_files:
        font_family = chosen_font

        weight = 400
        style = "normal"

        lower_name = filename.lower()
        if "bold" in lower_name:
            weight = 700
        if "italic" in lower_name:
            style = "italic"

        css = f"""
        @font-face {{
        font-family: '{font_family}';
        src: url('../fonts/{chosen_font}/{filename}') format('truetype');
        font-weight: {weight};
        font-style: {style};
        }}
        """
        css_blocks.append(css.strip())

    full_css = "\n\n".join(css_blocks)
    return full_css
