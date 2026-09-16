import asyncio
import json
import random
import shutil
from pathlib import Path

import aiofiles
from jinja2 import Environment, FileSystemLoader, select_autoescape

from white_generator.core.config import Variant2BuildContext
from white_generator.utils import build_directories, copy_all_files
from white_generator.variant_2_creator.constants import get_mini_app_params

DEFAULT_TEMPLATE_NAME = "index.html"
MIN_HOUSE_IMAGES = 8


class MiniAppBuilder:
    """Build a mini app from a game template."""

    def __init__(
        self,
        context: Variant2BuildContext,
        template_path: str | None = None,
    ):
        self.context = context
        self.base_dir = Path(__file__).parent
        self.template_dir = (
            Path(template_path)
            if template_path
            else self.base_dir / "mini_games" / "tower"
        )

        if not self.template_dir.is_dir():
            raise FileNotFoundError(
                f"Template directory not found: {self.template_dir}"
            )

    async def _load_template(
        self,
        template_name: str = DEFAULT_TEMPLATE_NAME,
    ) -> str:
        """Load a template file asynchronously."""
        template_path = self.template_dir / template_name

        async with aiofiles.open(template_path, "r", encoding="utf-8") as file:
            return await file.read()

    async def _render_template(
        self,
        template_content: str,
        context: dict,
    ) -> str:
        """Render template content with the provided context."""
        environment = Environment(
            loader=FileSystemLoader(str(self.template_dir.parent)),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True,
        )

        template = environment.from_string(template_content)
        return await template.render_async(**context)

    async def _copy_directory(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        """Copy all files from source directory to destination."""
        destination.mkdir(parents=True, exist_ok=True)
        await copy_all_files(str(source), str(destination))

    def _find_images(self, directory: Path) -> list[Path]:
        """Return supported image files from a directory."""
        return [path for path in directory.iterdir()]

    def _select_dynamic_images(self) -> tuple[Path, list[Path]]:
        """Select one currency image and unique house images."""
        image_dir = self.template_dir / "img"

        currency_images = self._find_images(image_dir / "currency")
        house_images = self._find_images(image_dir / "house")

        currency_image = random.choice(currency_images)
        selected_house_images = random.sample(
            house_images,
            MIN_HOUSE_IMAGES,
        )
        return currency_image, selected_house_images

    def _copy_dynamic_images(
        self,
        currency_image: Path,
        house_images: list[Path],
        destination: Path,
    ) -> None:
        """Copy selected dynamic images to the textures directory."""
        destination.mkdir(parents=True, exist_ok=True)

        shutil.copy(
            currency_image,
            destination / currency_image.name,
        )

        for image in house_images:
            shutil.copy(
                image,
                destination / image.name,
            )

    def _update_config(
        self,
        context: dict,
        currency_image: Path,
        house_images: list[Path],
    ) -> None:
        """Inject selected image paths into the game configuration."""
        config = json.loads(context.get("config_json", "{}"))

        config.setdefault("points", {})["currencyIcon"] = (
            f"textures/{currency_image.name}"
        )

        config.setdefault("block", {})["textures"] = [
            f"textures/{image.name}"
            for image in house_images
        ]

        context["config_json"] = json.dumps(config)

    def _set_base_url(self, context: dict) -> None:
        """Set the URL prefix for generated static files."""
        relative_path = Path(
            self.context.STATIC_DIR
        ).relative_to(
            self.context.DIST_DIR
        )

        context["base_url"] = f"{relative_path.as_posix()}/"

    async def _prepare_dynamic_assets(
        self,
        context: dict,
    ) -> None:
        """Select, copy, and configure dynamic game images."""
        currency_image, house_images = self._select_dynamic_images()

        textures_dir = Path(self.context.STATIC_DIR) / "textures"

        self._copy_dynamic_images(
            currency_image=currency_image,
            house_images=house_images,
            destination=textures_dir,
        )

        self._update_config(
            context=context,
            currency_image=currency_image,
            house_images=house_images,
        )

    async def _copy_static_assets(self) -> None:
        """Copy template assets and textures to the build directory."""
        static_dir = Path(self.context.STATIC_DIR)

        await asyncio.gather(
            self._copy_directory(
                self.template_dir / "assets",
                static_dir / "assets",
            ),
            self._copy_directory(
                self.template_dir / "textures",
                static_dir / "textures",
            ),
        )

    async def build(self, config_overrides: dict | None = None) -> str:
        """Build the mini app and return the absolute distribution path."""
        build_directories(self.context)

        context = get_mini_app_params()

        if config_overrides:
            context.update(config_overrides)

        await self._prepare_dynamic_assets(context)
        self._set_base_url(context)

        template_content = await self._load_template()
        rendered_html = await self._render_template(
            template_content,
            context,
        )

        output_path = Path(self.context.DIST_DIR) / "source_target.html"

        async with aiofiles.open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:
            await file.write(rendered_html)

        await self._copy_static_assets()

        return str(Path(self.context.DIST_DIR).resolve())

    async def build_from_config(self, game_config: dict) -> str:
        """Build the mini app using a custom game configuration."""
        return await self.build(
            config_overrides={
                "config_json": json.dumps(game_config),
            }
        )