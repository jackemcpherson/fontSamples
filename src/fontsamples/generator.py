"""Font sample generator module."""

import logging
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class FontSampleError(Exception):
    """Base exception for font sample generation errors."""
    pass


class FontLoadError(FontSampleError):
    """Raised when a font file cannot be loaded."""
    pass


class ImageGenerationError(FontSampleError):
    """Raised when image generation fails."""
    pass


class FontSampleGenerator:
    """Generate visual font samples as PNG images.

    This class creates image samples of fonts with customizable text, size,
    and dimensions. It handles text wrapping, font size adjustment, and
    vertical centering automatically.

    Attributes:
        font_path: Path to the TTF font file
        text: Text to render in the sample
        image_size: Tuple of (width, height) for output image
        font_size: Initial font size in points
    """

    LINE_SPACING_RATIO = 0.2
    MIN_FONT_SIZE = 10
    IMAGE_PADDING = 20
    BACKGROUND_COLOR = "#F8F5F0"
    TEXT_COLOR = "black"

    def __init__(
        self,
        font_path: str,
        text: str,
        image_size: tuple[int, int],
        font_size: int
    ) -> None:
        """Initialize the FontSampleGenerator.

        Args:
            font_path: Path to the TTF font file
            text: Text to render in the sample
            image_size: Tuple of (width, height) for output image
            font_size: Initial font size in points
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")

        if font_size < self.MIN_FONT_SIZE:
            raise ValueError(f"Font size must be at least {self.MIN_FONT_SIZE}")

        if image_size[0] <= 0 or image_size[1] <= 0:
            raise ValueError("Image dimensions must be positive")

        self.font_path = Path(font_path).resolve()
        self.text = text
        self.image_size = image_size
        self.font_size = font_size

        if not self.font_path.exists():
            raise FontLoadError(f"Font file not found: {font_path}")

        if self.font_path.suffix.lower() != '.ttf':
            logger.warning("Font file may not be TTF format: %s", font_path)

    def _wrap_text(self, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
        """Wrap text to fit within a specified width.

        Args:
            font: The font to be used for measuring text
            max_width: The maximum width of a text line in pixels

        Returns:
            List of lines after wrapping the text
        """
        if max_width <= 0:
            return [self.text]

        char_width = font.getbbox("A")[2]
        if char_width <= 0:
            return [self.text]

        chars_per_line = max(1, int(max_width / char_width))
        return textwrap.wrap(self.text, width=chars_per_line)

    def _compute_total_text_height(
        self, font: ImageFont.FreeTypeFont, lines: list[str]
    ) -> float:
        """Compute the total height of all lines, including spacing.

        Args:
            font: The font to be used for measuring text
            lines: The wrapped lines of text

        Returns:
            The total text height value in pixels
        """
        if not lines:
            return 0.0

        line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
        spacing_between_lines = line_height * self.LINE_SPACING_RATIO
        return (
            len(lines) * (line_height + spacing_between_lines) - spacing_between_lines
        )

    def _compute_start_height(self, total_text_height: float) -> float:
        """Compute the starting height to vertically center the text.

        Args:
            total_text_height: Total height of the text block in pixels

        Returns:
            The starting height value for vertical centering
        """
        return max(0, (self.image_size[1] - total_text_height) / 2)

    def _load_font_with_size(self, size: int) -> ImageFont.FreeTypeFont:
        """Load font with specified size.

        Args:
            size: Font size in points

        Returns:
            Loaded font object

        Raises:
            FontLoadError: If font cannot be loaded
        """
        try:
            return ImageFont.truetype(str(self.font_path), size)
        except OSError as e:
            logger.error(
                "Failed to load font: %s (size: %d)",
                self.font_path, size, exc_info=True
            )
            raise FontLoadError(
                f"Unable to load font at {self.font_path}"
            ) from e

    def _adjust_font_size_for_fit(
        self,
        draw: ImageDraw.ImageDraw,
        font: ImageFont.FreeTypeFont,
        lines: list[str],
        max_width: int
    ) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
        """Adjust font size to fit text within maximum width.

        Args:
            draw: ImageDraw object for text measurement
            font: Initial font object
            lines: Text lines to fit
            max_width: Maximum allowed width in pixels

        Returns:
            Tuple of (adjusted_font, adjusted_lines, final_font_size)
        """
        current_font = font
        current_lines = lines
        current_size = self.font_size

        while (
            current_lines and
            draw.textbbox((0, 0), current_lines[0], font=current_font)[2] > max_width
            and current_size > self.MIN_FONT_SIZE
        ):
            current_size -= 1
            current_font = self._load_font_with_size(current_size)
            current_lines = self._wrap_text(current_font, max_width)

        logger.debug(
            "Font size adjusted from %d to %d for width constraint",
            self.font_size, current_size
        )

        return current_font, current_lines, current_size

    def generate_sample(self, output_path: str) -> None:
        """Generate font sample and save to the given output path.

        Args:
            output_path: The path where the output image should be saved

        Raises:
            FontLoadError: If the font file cannot be loaded
            ImageGenerationError: If image generation fails
        """
        logger.info(
            "Generating font sample: %s -> %s (size: %d, dimensions: %dx%d)",
            self.font_path.name, output_path, self.font_size,
            self.image_size[0], self.image_size[1]
        )

        try:
            img = Image.new("RGB", self.image_size, self.BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)

            font = self._load_font_with_size(self.font_size)
            max_width = max(1, self.image_size[0] - (2 * self.IMAGE_PADDING))
            lines = self._wrap_text(font, max_width)

            if not lines:
                raise ImageGenerationError("No text lines to render")

            font, lines, final_font_size = self._adjust_font_size_for_fit(
                draw, font, lines, max_width
            )

            total_text_height = self._compute_total_text_height(font, lines)
            current_height = self._compute_start_height(total_text_height)

            logger.debug("Rendering %d lines of text", len(lines))

            for line in lines:
                if not line.strip():
                    continue

                text_width = draw.textbbox((0, 0), line, font=font)[2]
                x_position = max(0, (self.image_size[0] - text_width) / 2)

                draw.text(
                    (x_position, current_height),
                    line,
                    fill=self.TEXT_COLOR,
                    font=font
                )

                line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
                spacing_between_lines = line_height * self.LINE_SPACING_RATIO
                current_height += line_height + spacing_between_lines

            output_path_obj = Path(output_path)
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)

            img.save(str(output_path_obj))

            logger.info("Font sample saved successfully: %s", output_path)

        except (OSError, ValueError) as e:
            logger.error(
                "Failed to generate font sample: %s",
                output_path, exc_info=True
            )
            raise ImageGenerationError(
                f"Failed to generate image: {e}"
            ) from e
