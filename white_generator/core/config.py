import os
import pathlib


class AppConfig:
    def __init__(self):
        self.APP_DIR = pathlib.Path(__file__).parent.parent
        self.COOKIE_DIR = pathlib.Path(self.APP_DIR / "cookie")
        self.VAR1_DIR = pathlib.Path(self.APP_DIR / "variant_1_creator")
        self.FIDGETS_DIR = pathlib.Path(self.VAR1_DIR / "presets/fidgets")
        
        self.DIST_DIR = None
        self.STATIC_DIR = None
        self.IMG_DIR = None
        self.CSS_DIR = None
        self.JS_DIR = None
        self.FONTS_DIR = None

        # Static settings
        self.LLM_TEXT_MODEL = "gemini-2.5-flash-lite"
        self.LLM_IMAGE_MODEL = "gemini-2.0-flash-preview-image-generation"
        self.BUCKET_NAME = "mtoffer-club"
        self.AWS_REGION = "eu-north-1"
        self.BASIC_FOLDER = "public/cached-whites/"

    def set_dist_dir(self, path: str):
        """Set the base build directory and dependent paths."""
        self.DIST_DIR = os.path.abspath(path)
        self.STATIC_DIR = os.path.join(self.DIST_DIR, "source_target_files")
        self.IMG_DIR = os.path.join(self.STATIC_DIR, "img")
        self.CSS_DIR = os.path.join(self.STATIC_DIR, "css")
        self.JS_DIR = os.path.join(self.STATIC_DIR, "js")
        self.FONTS_DIR = os.path.join(self.STATIC_DIR, "fonts")


config = AppConfig()
