import textwrap
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


class FontSampleGenerator:
    def __init__(
        self, font_path: str, text: str, image_size: Tuple[int, int], font_size: int
    ):
        self.font_path = font_path
        self.text = text
        self.image_size = image_size
        self.font_size = font_size

    def _wrap_text(self, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """
        Wrap text to fit within a specified width.

        Parameters:
            font (ImageFont.FreeTypeFont): The font to be used.
            max_width (int): The maximum width of a text line.

        Returns:
            List[str]: List of lines after wrapping the text.
        """
        return textwrap.wrap(self.text, width=int(max_width / font.getbbox("A")[2]))

    def _adjust_font_size(
        self, font: ImageFont.FreeTypeFont, max_width: int
    ) -> ImageFont.FreeTypeFont:
        """
        Adjust font size if the text is too wide.

        Parameters:
            font (ImageFont.FreeTypeFont): The font to be adjusted.
            max_width (int): The maximum width of a text line.

        Returns:
            ImageFont.FreeTypeFont: The adjusted font.
        """
        lines = self._wrap_text(font, max_width)
        while font.getbbox(lines[0])[2] > max_width and self.font_size > 10:
            self.font_size -= 1
            font = ImageFont.truetype(self.font_path, self.font_size)
            lines = self._wrap_text(font, max_width)
        return font

    def _compute_total_text_height(
        self, font: ImageFont.FreeTypeFont, lines: List[str]
    ) -> float:
        """
        Compute the total height of all lines, including spaces between them.

        Parameters:
            font (ImageFont.FreeTypeFont): The font to be used.
            lines (List[str]): The wrapped lines of text.

        Returns:
            float: The total text height value.
        """
        line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
        spacing_between_lines = line_height * 0.2  # 20% space between lines.
        return (
            len(lines) * (line_height + spacing_between_lines) - spacing_between_lines
        )

    def _compute_start_height(self, total_text_height: float) -> float:
        """
        Compute the starting height to vertically center the text.

        Parameters:
            total_text_height (float): Total height of the text block.

        Returns:
            float: The starting height value.
        """
        return (self.image_size[1] - total_text_height) / 2

    def generate_sample(self, output_path: str) -> None:
        """
        Generate font sample and save to the given output path.

        Parameters:
            output_path (str): The path where the output image should be saved.
        """
        img = Image.new("RGB", self.image_size, "#F8F5F0")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except OSError as e:
            raise Exception(f"Unable to load font at {self.font_path}. Error: {e}")

        max_width = self.image_size[0] - 20
        font = self._adjust_font_size(font, max_width)
        lines = self._wrap_text(font, max_width)

        total_text_height = self._compute_total_text_height(font, lines)
        current_height = self._compute_start_height(total_text_height)

        for line in lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            width = (self.image_size[0] - text_width) / 2
            draw.text((width, current_height), line, fill="black", font=font)
            line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
            spacing_between_lines = line_height * 0.2
            current_height += line_height + spacing_between_lines

        img.save(output_path)
