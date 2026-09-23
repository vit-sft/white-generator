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

PRIVACY_TEXTS = [
    "We respect your privacy. Any personal information you provide is handled in accordance with applicable data protection laws. For more details, see our ",
    
    "Your privacy matters to us. We handle personal information responsibly and take reasonable steps to protect the information you provide. Learn more in our ",
    
    "We value your privacy and take reasonable measures to protect the information you provide while using the game. For additional information, please read our ",
    
    "We are committed to protecting your privacy. Information you provide may be used to operate, maintain, and improve the game. For more information, please see our ",
    
    "Your information is important to us. We collect and use personal information only when necessary to provide and improve the game. Please review our ",
    
    "We aim to handle your information responsibly and transparently. Any personal information is processed in accordance with applicable requirements. More details are available in our ",
]


RESPONSIBLE_USE_TEXTS = [
    "Play for fun and keep your sessions balanced. Step away from the game from time to time and give yourself a chance to rest.",

    "Enjoy the challenge without overdoing it. Short breaks between sessions can help keep the experience comfortable and enjoyable.",

    "Keep gameplay part of a balanced routine. Avoid long uninterrupted sessions and take time away from the screen when needed.",

    "There is no need to rush. Play when you have time to enjoy it, take breaks regularly, and keep your overall screen time in check.",

    "Have fun stacking and know when to pause. Regular breaks and moderate play can help you enjoy the game without spending too much time on it.",
]


TERMS_TEXTS = [
    "Welcome to {app_name}! By using this game, you agree to these terms and to use the app for its intended entertainment purposes.",
    
    "Thanks for playing {app_name}! By accessing or using the game, you agree to follow these terms and use the service responsibly.",
    
    "Welcome to {app_name}. By playing the game, you agree to these terms and acknowledge that the game is provided for entertainment purposes.",
    
    "By using {app_name}, you agree to follow these terms and use the game only for its intended purpose. Please use the service responsibly.",
    
    "Enjoy {app_name}! By using the game, you agree to these terms and to follow the rules and guidelines provided within the app.",
]


RULES_TEXTS = [
    "Tap the screen to stop the moving block and place it on the tower. Each new block is slightly narrower than the last. Keep stacking to increase your score. The game ends when a block misses the tower. Press Retry to start a new game.",
    
    "Tap to stop the moving block when it lines up with the tower. Every successful stack makes the next block slightly narrower. Keep building the tower to earn a higher score. Missing the tower ends the game.",
    
    "Stop the moving block with a tap and place it on the tower. Blocks become narrower as you progress, making each move more challenging. Stack as high as possible and avoid missing the tower.",
    
    "Tap at the right moment to place each block on the tower. Each new block becomes a little smaller, so precision is important. Continue stacking to improve your score. The game ends when a block misses.",
    
    "Time your tap carefully and land the moving block on the tower. The blocks gradually become narrower as your tower grows. Keep stacking for a higher score, but one missed block will end the game.",
    
    "Tap the screen when the moving block is aligned with the tower. Successfully placed blocks let you continue while making the next block slightly narrower. Build the highest tower you can before a block misses.",
]


COOKIE_TEXTS = [
    "This app uses cookies and similar technologies to remember your preferences and improve your experience.",
    
    "We use cookies to remember settings and preferences and to help provide a smooth gaming experience.",
    
    "Cookies may be used to remember your preferences and selected settings while you use the app.",
    
    "This app uses cookies and similar technologies to maintain preferences and improve the functionality of the game.",
    
    "We use cookies to help remember your settings and provide a consistent experience when you return to the game.",
]

def generate_random_name() -> str:
    adjectives = [
        "Happy", "Lucky", "High", "Super", "Mega", 
        "Bright", "Fast", "Smart", "Cool", "Epic",
        "Alpha", "Turbo", "Ultra", "Grand", "Prime"
    ]
    nouns = [
        "Level", "Press", "Tower", "Zone", "Hub", 
        "Base", "Core", "Point", "Link", "Force",
        "Stack", "Grid", "Node", "Wave", "Flow"
    ]
    return f"{random.choice(adjectives)} {random.choice(nouns)}"


def generate_support_email(app_name: str) -> str:
    """
    Convert the app name into a simple Gmail-style support address.

    Example:
        "Happy Level" -> "support.happy.level@gmail.com"
    """
    app_slug = app_name.lower().replace(" ", ".")
    return f"support.{app_slug}@gmail.com"


def get_random_game_config():
    """
    Return a randomized game configuration.
    """

    footer = random.choice(FOOTER_COLOR_SETS)
    button = random.choice(BUTTON_COLOR_SETS)

    app_name = generate_random_name()
    support_email = generate_support_email(app_name)

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
            **random.choice([
                {
                    "retryLabel": "Retry",
                    "startLabel": "Start",
                    "resumeLabel": "Resume",
                },
                {
                    "retryLabel": "Try Again",
                    "startLabel": "Play",
                    "resumeLabel": "Continue",
                },
                {
                    "retryLabel": "Play Again",
                    "startLabel": "Let's Play",
                    "resumeLabel": "Keep Playing",
                },
                {
                    "retryLabel": "Restart",
                    "startLabel": "Begin",
                    "resumeLabel": "Continue Game",
                },
                {
                    "retryLabel": "Again",
                    "startLabel": "Start Game",
                    "resumeLabel": "Back to Game",
                },
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
            "moveSpeed": random.choice([2.2, 2.4, 2.6, 2.8, 3.0]),
        },

        "legal": {
            "gameTitle": app_name,

            "termsAndPolicies": {
                "privacyText": random.choice(PRIVACY_TEXTS),
                "privacyPolicyLinkText": random.choice([
                    "Privacy Policy",
                    "Privacy Details",
                ]),
                "privacyPolicyUrl": "",

                "contactText": f"Contact us at {support_email}",

                "responsibleUseText": random.choice(
                    RESPONSIBLE_USE_TEXTS
                ),

                "termsText": random.choice(
                    TERMS_TEXTS
                ).format(app_name=app_name),
            },

            "rules": {
                "text": random.choice(RULES_TEXTS),
            },

            "cookies": {
                "text": random.choice(COOKIE_TEXTS),

                "acceptAllLabel": random.choice([
                    "Accept All",
                    "Accept",
                    "Allow All",
                    "Accept Cookies",
                ]),

                "acceptNecessaryLabel": random.choice([
                    "Necessary Only",
                    "Only Necessary",
                    "Essential Only",
                    "Accept Necessary",
                ]),

                "backgroundColor": "#1e293b",
            },
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
