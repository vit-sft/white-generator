"""
Constants module for variant_2_creator mini app builder.
"""

import json

# Default game configuration
DEFAULT_GAME_CONFIG = {
    "background": {
        "image": "./textures/sky.png",
        "fallbackColor": "linear-gradient(180deg, #6ec6ff 0%, #cdeffd 60%, #eaf7ff 100%)",
        "scrollPixelsPerBlock": 4,
        "maxScroll": 400
    },
    "block": {
        "colors": [
            "#8b5a2b",
            "#a0672f",
            "#7a4a24",
            "#93613a"
        ],
        "textures": [
            "./textures/house-1.png",
            "./textures/house-2.png",
            "./textures/house-3.png",
            "./textures/house-4.png",
            "./textures/house-5.png",
            "./textures/house-6.png",
            "./textures/house-7.png",
            "./textures/house-8.png"
        ],
        "borderRadius": 6,
        "shadow": True
    },
    "footer": {
        "backgroundColor": "#6b7280",
        "borderColor": "#facc15",
        "borderWidth": 6
    },
    "points": {
        "bestLabel": "Best Score",
        "font": "system-ui, sans-serif",
        "color": "#1e293b",
        "fontSize": 30,
        "currencyIcon": "./textures/currency.png"
    },
    "button": {
        "retryLabel": "Retry",
        "gradientStart": "#ff8a00",
        "gradientEnd": "#ff3d00",
        "borderColor": "#ffd166",
        "textColor": "#ffffff",
        "borderRadius": 12
    },
    "gameOverText": "Game Over",
    "game": {
        "topMargin": 40,
        "moveSpeed": 2.2
    }
}

# Configuration constants for the mini app
# Note: config_json is a Jinja2 safe JSON string
MINI_APP_CONSTANTS = {
    "base_url": "",  # Will be set dynamically based on random dir
    "config_json": json.dumps(DEFAULT_GAME_CONFIG)
}

# Also export the default config for easy access
DEFAULT_CONFIG = DEFAULT_GAME_CONFIG
