import os
import pathlib

APP_DIR = pathlib.Path(__file__).parent.parent
DIST_DIR = str(APP_DIR.parent / "dist")
STATIC_DIR = os.path.join(DIST_DIR, "static")
IMG_DIR = os.path.join(STATIC_DIR, "img")
CSS_DIR = os.path.join(STATIC_DIR, "css")
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")