"""Command-line interface for Font Samples Generator."""

import os
import argparse
from pathlib import Path
from typing import Tuple

from .generator import FontSampleGenerator


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate visual samples of fonts"
    )
    parser.add_argument(
        "--text",
        default="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        help="Text to render in font samples"
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=35,
        help="Font size for rendering"
    )
    parser.add_argument(
        "--image-size",
        type=str,
        default="250x250",
        help="Image size as WIDTHxHEIGHT"
    )
    parser.add_argument(
        "--fonts-dir",
        type=Path,
        default=Path("./fonts/"),
        help="Directory containing font files"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output_files/"),
        help="Directory to save generated samples"
    )

    args = parser.parse_args()

    # Parse image size
    try:
        width, height = map(int, args.image_size.split('x'))
        image_size: Tuple[int, int] = (width, height)
    except ValueError:
        print(f"Invalid image size format: {args.image_size}. Use WIDTHxHEIGHT")
        return

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Check if fonts directory exists
    if not args.fonts_dir.exists():
        print(f"Fonts directory not found: {args.fonts_dir}")
        return

    # Process all .ttf files
    font_files = list(args.fonts_dir.glob("*.ttf"))
    if not font_files:
        print(f"No .ttf files found in {args.fonts_dir}")
        return

    print(f"Processing {len(font_files)} font files...")

    for font_file in font_files:
        output_path = args.output_dir / f"{font_file.stem}.png"

        try:
            generator = FontSampleGenerator(
                str(font_file),
                args.text,
                image_size,
                args.font_size
            )
            generator.generate_sample(str(output_path))
            print(f"Generated: {output_path}")
        except Exception as e:
            print(f"Error processing {font_file}: {e}")


if __name__ == "__main__":
    main()