import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

APP_DIR = pathlib.Path(__file__).parent.parent
DIST_DIR = str(APP_DIR.parent / "dist")
STATIC_DIR = os.path.join(DIST_DIR, "source_target_files")
IMG_DIR = os.path.join(STATIC_DIR, "img")
CSS_DIR = os.path.join(STATIC_DIR, "css")
JS_DIR = os.path.join(STATIC_DIR, "js")
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")
COOKIE_DIR = str(APP_DIR / "cookie")

IMG_CX = os.getenv('IMG_CX')
IMG_API_TOKEN = os.getenv('IMG_API_TOKEN')

LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_MODEL = "gemini-2.5-flash-lite"

ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
BUCKET_NAME = "mtoffer-club"
AWS_REGION = "eu-north-1"
BASIC_FOLDER = 'public/cached-whites/'