import os
import pathlib

from white_generator.core.settings import generate_random_id


class BuildContext:
    """Base class for build-specific dynamic paths."""
    def __init__(self, dist_dir: str):
        self.DIST_DIR = os.path.abspath(dist_dir)
        self.STATIC_DIR = os.path.join(self.DIST_DIR, "source_target_files", generate_random_id(8))
        self.IMG_DIR = os.path.join(self.STATIC_DIR, "img")

class Variant1BuildContext(BuildContext):
    def __init__(self, dist_dir: str):
        super().__init__(dist_dir)
        self.APP_DIR = pathlib.Path(__file__).parent.parent
        self.COOKIE_DIR = self.APP_DIR / "cookie"
        self.VAR1_DIR = self.APP_DIR / "variant_1_creator"
        self.FIDGETS_DIR = self.VAR1_DIR / "presets/fidgets"
        self.CSS_DIR = os.path.join(self.STATIC_DIR, "css")
        self.JS_DIR = os.path.join(self.STATIC_DIR, "js")
        self.FONTS_DIR = os.path.join(self.STATIC_DIR, "fonts")

class Variant2BuildContext(BuildContext):
    def __init__(self, dist_dir: str):
        super().__init__(dist_dir)
        # Variant 2 might have different sub-paths
        self.ASSETS_DIR = os.path.join(self.STATIC_DIR, "assets")
