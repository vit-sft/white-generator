import random

def get_random_style():
    """
    Selects a random template, color palette, and font for the website build.
    Returns font_url and root for css.
    """
    
    # list of color palettes
    palettes = {
        "Ocean": {
            "primary": "#00A7E1", "secondary": "#F1F1F2", "background": "#FFFFFF",
            "text_primary": "#00171F", "text_secondary": "#003459"
        },
        "Forest": {
            "primary": "#4A7856", "secondary": "#F2EAE4", "background": "#FFFFFF",
            "text_primary": "#223326", "text_secondary": "#3E5346"
        },
        "Sunset": {
            "primary": "#FF6B6B", "secondary": "#FFD166", "background": "#FFF9F0",
            "text_primary": "#073B4C", "text_secondary": "#118AB2"
        },
        "Charcoal": {
            "primary": "#36454F", "secondary": "#F5F5F5", "background": "#FFFFFF",
            "text_primary": "#1A1A1A", "text_secondary": "#5A5A5A"
        },
        "Royal": {
            "primary": "#4169E1", "secondary": "#F0F8FF", "background": "#FFFFFF",
            "text_primary": "#00008B", "text_secondary": "#191970"
        }
    }
    palette_name = random.choice(list(palettes.keys()))
    
    # list of Google Fonts
    fonts = {
        "Poppins": "'Poppins', sans-serif",
        "Roboto": "'Roboto', sans-serif",
        "Montserrat": "'Montserrat', sans-serif",
        "Lato": "'Lato', sans-serif",
        "Open Sans": "'Open Sans', sans-serif",
    }
    font_name = random.choice(list(fonts.keys()))
    font_family = fonts[font_name]
    font_url = f"https://fonts.googleapis.com/css2?family={font_name.replace(' ', '+')}:wght@400;700&display=swap"

    colors = palettes[palette_name]
    primary = colors['primary'] 
    secondary = colors['secondary']
    background = colors['background']
    text_primary = colors['text_primary'] 
    text_secondary = colors['text_secondary']
    
    root_element = f""":root {{
        --font-family: {font_family};
        --background: {background};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --primary: {primary};
        --secondary: {secondary};
    }}"""

    return {
        "font_url": font_url,
        "root_element": root_element
    }