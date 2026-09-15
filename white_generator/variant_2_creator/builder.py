import asyncio
import os
from pathlib import Path

import aiofiles
from jinja2 import Environment, FileSystemLoader, select_autoescape

from white_generator.core.config import Variant2BuildContext
from white_generator.utils import build_directories, copy_all_files
from white_generator.variant_2_creator.constants import MINI_APP_CONSTANTS


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

    async def _copy_favicon(self, source_favicon: Path, dest_dir: Path):
        """
        Copy favicon to destination directory.

        Args:
            source_favicon: Source favicon path.
            dest_dir: Destination directory.
        """
        dest_path = dest_dir / source_favicon.name
        os.makedirs(dest_dir, exist_ok=True)
        import shutil
        await asyncio.to_thread(shutil.copy2, str(source_favicon), str(dest_path))

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
        context = MINI_APP_CONSTANTS.copy()
        
        # Override with any provided config
        if config_overrides:
            context.update(config_overrides)

        # Set base_url to the random static directory
        # Get the relative path from DIST_DIR
        rel_path = os.path.relpath(self.context.STATIC_DIR, self.context.DIST_DIR)
        context["base_url"] = f"{rel_path}/"
        
        # Load template
        template_content = await self._load_template_async("index.html")
        
        # Render template
        rendered_html = await self._render_template(template_content, context)

        # Define output paths
        index_path = os.path.join(self.context.DIST_DIR, "source_target.html")
        
        # Get source assets directory
        source_assets_dir = self.template_dir / "assets"
        source_textures_dir = self.template_dir / "textures"
        dest_assets_dir = Path(self.context.STATIC_DIR) / "assets"
        dest_textures_dir = Path(self.context.STATIC_DIR) / "textures"
        # Write rendered HTML
        async with aiofiles.open(index_path, "w", encoding="utf-8") as f:
            await f.write(rendered_html)

        # Copy assets and favicon in parallel
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
