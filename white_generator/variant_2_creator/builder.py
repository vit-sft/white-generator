import asyncio
import json
import os
import random
import shutil
from pathlib import Path

import aiofiles
from jinja2 import Environment, FileSystemLoader, select_autoescape

from white_generator.core.config import Variant2BuildContext
from white_generator.utils import build_directories, copy_all_files
from white_generator.variant_2_creator.constants import get_mini_app_params


class MiniAppBuilder:
    """
    Builder for mini apps (like tower game).
    Uses Jinja2 templates and async operations.
    """

    def __init__(self, context: Variant2BuildContext, template_path: str | None = None):
        """
        Initialize the MiniAppBuilder.

        Args:
            context: Variant2BuildContext instance for this build.
            template_path: Path to the template directory. 
                          Defaults to mini_games/tower in variant_2_creator.
        """
        self.context = context
        self.base_dir = Path(__file__).parent
        if template_path:
            self.template_dir = Path(template_path)
        else:
            # Default to tower game template
            self.template_dir = self.base_dir / "mini_games" / "tower"

        # Ensure template directory exists
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")


    async def _load_template_async(self, template_name: str = "index.html") -> str:
        """
        Load a template file asynchronously.

        Args:
            template_name: Name of the template file.

        Returns:
            Template content as string.
        """
        template_path = self.template_dir / template_name
        async with aiofiles.open(template_path, "r", encoding="utf-8") as f:
            return await f.read()

    async def _render_template(
        self, 
        template_content: str, 
        context: dict
    ) -> str:
        """
        Render a Jinja2 template with the given context asynchronously.

        Args:
            template_content: The template content as string.
            context: Dictionary of variables for the template.

        Returns:
            Rendered HTML content.
        """
        # Create Jinja2 environment with async support
        env = Environment(
            loader=FileSystemLoader(str(self.template_dir.parent)),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True
        )
        
        # Create template from string
        template = env.from_string(template_content)
        
        # Render template asynchronously
        rendered = await template.render_async(**context)
        return rendered

    async def _copy_assets(self, source_assets_dir: Path, dest_assets_dir: Path):
        """
        Copy all assets from source to destination directory.

        Args:
            source_assets_dir: Source directory containing assets.
            dest_assets_dir: Destination directory for assets.
        """
        os.makedirs(dest_assets_dir, exist_ok=True)
        await copy_all_files(str(source_assets_dir), str(dest_assets_dir))

    async def build(self, config_overrides: dict | None = None) -> str:
        """
        Build the mini app with the given configuration.

        Args:
            config_overrides: Optional dictionary to override default constants.

        Returns:
            Absolute path to the built distribution directory.
        """
        # Build directories
        build_directories(self.context)

        # Prepare context with constants
        context = get_mini_app_params()

        # Override with any provided config
        if config_overrides:
            context.update(config_overrides)

        # ------------------------------------------------------------------
        # Prepare dynamic images
        # ------------------------------------------------------------------

        source_img_dir = self.template_dir / "img"

        dest_textures_dir = Path(self.context.STATIC_DIR) / "textures"
        dest_textures_dir.mkdir(parents=True, exist_ok=True)

        # Separate currency and house images by subdirectory
        source_currency_dir = source_img_dir / "currency"
        source_house_dir = source_img_dir / "house"

        currency_images = [
            path for path in source_currency_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ] if source_currency_dir.exists() else []
        house_images = [
            path for path in source_house_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ] if source_house_dir.exists() else []

        if not currency_images:
            raise FileNotFoundError(
                f"No currency images found in {source_img_dir}"
            )

        if len(house_images) < 8:
            raise ValueError(
                f"Need at least 8 house images in {source_img_dir}, "
                f"but found {len(house_images)}"
            )

        # Choose one random currency image
        currency_image = random.choice(currency_images)

        # Choose 8 random house images
        # random.sample() guarantees unique images
        selected_house_images = random.sample(house_images, 8)

        # Copy currency image
        currency_destination = dest_textures_dir / currency_image.name
        shutil.copy2(currency_image, currency_destination)

        # Copy house images
        for house_image in selected_house_images:
            house_destination = dest_textures_dir / house_image.name
            shutil.copy2(house_image, house_destination)

        # ------------------------------------------------------------------
        # Update dynamic texture paths in template context
        # ------------------------------------------------------------------
        # 1. Parse the existing config_json string into a dict
        config_data = json.loads(context.get("config_json", "{}"))

        # 2. Inject the dynamic texture paths inside config_data
        config_data.setdefault("points", {})
        config_data["points"]["currencyIcon"] = f"textures/{currency_image.name}"

        config_data.setdefault("block", {})
        config_data["block"]["textures"] = [
            f"textures/{house_image.name}"
            for house_image in selected_house_images
        ]

        # 3. Overwrite config_json in context with the updated serialized JSON string
        context["config_json"] = json.dumps(config_data)
        print('contextcontextcontextcontext', context)

        # ------------------------------------------------------------------
        # Set base_url to the random static directory
        # ------------------------------------------------------------------

        rel_path = os.path.relpath(
            self.context.STATIC_DIR,
            self.context.DIST_DIR,
        )
        context["base_url"] = f"{rel_path}/"

        # ------------------------------------------------------------------
        # Load template
        # ------------------------------------------------------------------

        template_content = await self._load_template_async("index.html")

        # ------------------------------------------------------------------
        # Render template
        # ------------------------------------------------------------------

        rendered_html = await self._render_template(
            template_content,
            context,
        )

        # ------------------------------------------------------------------
        # Define output paths
        # ------------------------------------------------------------------

        index_path = os.path.join(
            self.context.DIST_DIR,
            "source_target.html",
        )

        # Get source assets directory
        source_assets_dir = self.template_dir / "assets"
        source_textures_dir = self.template_dir / "textures"

        dest_assets_dir = Path(self.context.STATIC_DIR) / "assets"

        # ------------------------------------------------------------------
        # Write rendered HTML
        # ------------------------------------------------------------------

        async with aiofiles.open(
            index_path,
            "w",
            encoding="utf-8",
        ) as f:
            await f.write(rendered_html)

        # ------------------------------------------------------------------
        # Copy static assets/textures in parallel
        # ------------------------------------------------------------------

        copy_tasks = [
            self._copy_assets(source_assets_dir, dest_assets_dir),
            self._copy_assets(source_textures_dir, dest_textures_dir),
        ]

        await asyncio.gather(*copy_tasks)

        return os.path.abspath(self.context.DIST_DIR)

    async def build_from_config(self, game_config: dict) -> str:
        """
        Build mini app with custom game configuration.

        Args:
            game_config: Dictionary containing game configuration.
                        This will override the default config in the template.

        Returns:
            Absolute path to the built distribution directory.
        """
        # Update the config_json in constants with the provided game_config
        config_overrides = {
            "config_json": f"{game_config}"
        }
        return await self.build(config_overrides)
