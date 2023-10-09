from typing import Tuple
from PIL import Image, ImageFont, ImageDraw
import textwrap


class FontSampleGenerator:
    def __init__(
        self, font_path: str, text: str, image_size: Tuple[int, int], font_size: int
    ):
        self.font_path = font_path
        self.text = text
        self.image_size = image_size
        self.font_size = font_size

    def _wrap_text(self, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """Wrap text to fit within a specified width."""
        bbox = font.getbbox("A")
        return textwrap.wrap(self.text, width=int(max_width / (bbox[2] - bbox[0])))

    def generate_sample(self, output_path: str) -> None:
        """Generate font sample and save to the given output path."""
        img = Image.new("RGB", self.image_size, "#F8F5F0")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError as e:
            raise Exception(f"Unable to load font at {self.font_path}. Error: {e}")

        max_width = self.image_size[0] - 20
        lines = self._wrap_text(font, max_width)

        # Adjust font size if the first line is too wide
        while (
            draw.textbbox((0, 0), lines[0], font=font)[2] > max_width
            and self.font_size > 10
        ):
            self.font_size -= 1
            font = ImageFont.truetype(self.font_path, self.font_size)
            lines = self._wrap_text(font, max_width)

        total_text_height = len(lines) * (
            font.getbbox(lines[0])[3] - font.getbbox(lines[0])[1]
        )
        start_height = (self.image_size[1] - total_text_height) / 2

        current_height = start_height
        for line in lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            text_height = draw.textbbox((0, 0), line, font=font)[3]
            width = (self.image_size[0] - text_width) / 2
            draw.text((width, current_height), line, fill="black", font=font)
            current_height += text_height

        img.save(output_path)
