import json
import random

# Randomization pools

FALLBACK_COLORS = [
    "linear-gradient(180deg, #6ec6ff 0%, #cdeffd 60%, #eaf7ff 100%)",
    "linear-gradient(180deg, #89f7fe 0%, #66a6ff 100%)",
    "linear-gradient(180deg, #fbc2eb 0%, #a6c1ee 100%)",
    "linear-gradient(180deg, #84fab0 0%, #8fd3f4 100%)",
    "linear-gradient(180deg, #fa709a 0%, #fee140 100%)",
    "linear-gradient(180deg, #cfd9df 0%, #e2ebf0 100%)",
    "linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
]

BLOCK_COLOR_SETS = [
    ["#8b5a2b", "#a0672f", "#7a4a24", "#93613a"],
    ["#4f46e5", "#6366f1", "#4338ca", "#818cf8"],
    ["#16a34a", "#22c55e", "#15803d", "#4ade80"],
    ["#dc2626", "#ef4444", "#b91c1c", "#f87171"],
    ["#ca8a04", "#eab308", "#a16207", "#facc15"],
    ["#0891b2", "#06b6d4", "#0e7490", "#22d3ee"],
    ["#9333ea", "#a855f7", "#7e22ce", "#c084fc"],
]

FOOTER_COLOR_SETS = [
    {"backgroundColor": "#6b7280", "borderColor": "#facc15"},
    {"backgroundColor": "#1e293b", "borderColor": "#38bdf8"},
    {"backgroundColor": "#334155", "borderColor": "#a78bfa"},
    {"backgroundColor": "#374151", "borderColor": "#34d399"},
    {"backgroundColor": "#7c2d12", "borderColor": "#fb923c"},
    {"backgroundColor": "#3f3f46", "borderColor": "#f472b6"},
    {"backgroundColor": "#14532d", "borderColor": "#bef264"},
]

POINT_COLORS = [
    "#1e293b",
    "#111827",
    "#374151",
    "#312e81",
    "#164e63",
    "#3f3f46",
    "#581c87",
]

BASIC_FONTS = [
    "Arial, sans-serif",
    "Verdana, sans-serif",
    "Tahoma, sans-serif",
    "Trebuchet MS, sans-serif",
    "Georgia, serif",
    "Times New Roman, serif",
    "Courier New, monospace",
]

POINT_LABELS = [
    "Best Score",
    "High Score",
    "Best",
    "Top Score",
    "Record",
    "Highest Score",
    "Score",
]

BUTTON_COLOR_SETS = [
    {
        "gradientStart": "#ff8a00",
        "gradientEnd": "#ff3d00",
        "borderColor": "#ffd166",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#2563eb",
        "gradientEnd": "#4f46e5",
        "borderColor": "#93c5fd",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#16a34a",
        "gradientEnd": "#15803d",
        "borderColor": "#86efac",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#db2777",
        "gradientEnd": "#be185d",
        "borderColor": "#f9a8d4",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#7c3aed",
        "gradientEnd": "#4c1d95",
        "borderColor": "#c4b5fd",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#0891b2",
        "gradientEnd": "#0e7490",
        "borderColor": "#67e8f9",
        "textColor": "#ffffff",
    },
    {
        "gradientStart": "#ca8a04",
        "gradientEnd": "#a16207",
        "borderColor": "#fde68a",
        "textColor": "#ffffff",
    },
]

GAME_OVER_TEXTS = [
    "Game Over",
    "Game Over!",
    "Try Again",
    "You Lost!",
    "Round Over",
    "Better Luck Next Time!",
    "Nice Try!",
]


# Config generator

def get_random_game_config():
    """
    Return a randomized game configuration.
    """

    footer = random.choice(FOOTER_COLOR_SETS)
    button = random.choice(BUTTON_COLOR_SETS)

    config = {
        "background": {
            "fallbackColor": random.choice(FALLBACK_COLORS),
            "scrollPixelsPerBlock": 4,
            "maxScroll": 400,
        },

        "block": {
            "colors": random.choice(BLOCK_COLOR_SETS),
            "borderRadius": random.choice([4, 6, 8, 10]),
            "shadow": random.random() < 0.70,
        },

        "footer": {
            "backgroundColor": footer["backgroundColor"],
            "borderColor": footer["borderColor"],
            "borderWidth": random.choice([4, 5, 6, 7]),
        },

        "points": {
            "bestLabel": random.choice(POINT_LABELS),
            "font": random.choice(BASIC_FONTS),
            "color": random.choice(POINT_COLORS),
            "fontSize": random.randint(28, 32),
        },

        "button": {
            "retryLabel": random.choice([
                "Retry",
                "Try Again",
                "Play Again",
                "Restart",
                "Again",
            ]),
            "gradientStart": button["gradientStart"],
            "gradientEnd": button["gradientEnd"],
            "borderColor": button["borderColor"],
            "textColor": button["textColor"],
            "borderRadius": random.choice([8, 10, 12, 14, 16]),
        },

        "gameOverText": random.choice(GAME_OVER_TEXTS),

        "game": {
            "topMargin": random.choice([30, 35, 40, 45, 50]),
            "moveSpeed": random.choice([1.8, 2.0, 2.2, 2.4, 2.6]),
        },
    }

    return config


def get_mini_app_params(base_url: str = "") -> dict:
    """
    Generate the mini app configuration parameters dynamically.
    """
    default_game_config = get_random_game_config()
    return {
        "base_url": base_url,
        "config_json": json.dumps(default_game_config),
    }