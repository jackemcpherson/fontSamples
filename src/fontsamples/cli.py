"""Command-line interface for Font Samples Generator."""

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler
from typing_extensions import Annotated

from .generator import FontSampleError, FontSampleGenerator

console = Console()


def _setup_logging(verbose: bool) -> logging.Logger:
    """Configure logging with rich formatting.

    Args:
        verbose: If True, set DEBUG level; otherwise INFO level

    Returns:
        Configured logger instance
    """
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, show_path=False)]
    )

    return logging.getLogger(__name__)


def _parse_image_size(size_str: str) -> tuple[int, int]:
    """Parse image size string like '250x250' into tuple.

    Args:
        size_str: Image size string in format 'WIDTHxHEIGHT'

    Returns:
        Tuple of (width, height) as integers

    Raises:
        typer.BadParameter: If the format is invalid or values are non-positive
    """
    try:
        width, height = map(int, size_str.split('x'))
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")
        return (width, height)
    except ValueError as e:
        raise typer.BadParameter(
            f"Invalid image size format: {size_str}. Use WIDTHxHEIGHT with positive integers"
        ) from e


def _validate_text_input(text: str) -> str:
    """Validate and sanitize text input.

    Args:
        text: Input text to validate

    Returns:
        Validated text

    Raises:
        typer.BadParameter: If text is empty or invalid
    """
    if not text or not text.strip():
        raise typer.BadParameter("Text cannot be empty")

    # Remove any null bytes or control characters that could cause issues
    cleaned_text = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')

    if not cleaned_text.strip():
        raise typer.BadParameter("Text contains only control characters")

    return cleaned_text


def main_command(
    text: Annotated[
        str,
        typer.Option(
            "--text", "-t",
            help="Text to render in font samples"
        )
    ] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",

    font_size: Annotated[
        int,
        typer.Option(
            "--font-size", "-s",
            help="Font size for rendering",
            min=8,
            max=500
        )
    ] = 35,

    image_size: Annotated[
        str,
        typer.Option(
            "--image-size", "-i",
            help="Image size as WIDTHxHEIGHT (e.g., 250x250)"
        )
    ] = "250x250",

    fonts_dir: Annotated[
        Path,
        typer.Option(
            "--fonts-dir", "-f",
            help="Directory containing font files",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        )
    ] = Path("./fonts/"),

    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o",
            help="Directory to save generated samples"
        )
    ] = Path("./output_files/"),

    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose output and debug logging"
        )
    ] = False,
) -> None:
    """Generate visual samples for all TTF fonts in the specified directory.

    This command processes all .ttf files in the fonts directory and creates
    image samples with the specified text, saving them to the output directory.

    Args:
        text: Text to render in font samples
        font_size: Font size for rendering (8-500 points)
        image_size: Image dimensions as WIDTHxHEIGHT string
        fonts_dir: Directory containing TTF font files
        output_dir: Directory to save generated samples
        verbose: Enable verbose output and debug logging

    Raises:
        typer.Exit: If validation fails or errors occur during processing
    """
    logger = _setup_logging(verbose)

    try:
        # Validate and parse inputs
        validated_text = _validate_text_input(text)
        width, height = _parse_image_size(image_size)
        image_size_tuple = (width, height)

    except typer.BadParameter as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    logger.info("Starting font sample generation")
    logger.debug(
        "Configuration: text='%s', font_size=%d, image_size=%dx%d, fonts_dir=%s, output_dir=%s",
        validated_text[:50] + "..." if len(validated_text) > 50 else validated_text,
        font_size, width, height, fonts_dir, output_dir
    )

    # Ensure output directory exists
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Output directory ready: %s", output_dir)
    except (OSError, PermissionError) as e:
        console.print(f"[red]Error:[/red] Cannot create output directory: {e}")
        logger.error("Failed to create output directory: %s", output_dir, exc_info=True)
        raise typer.Exit(1) from e

    if verbose:
        console.print(f"[blue]Output directory:[/blue] {output_dir}")
        console.print(f"[blue]Fonts directory:[/blue] {fonts_dir}")
        console.print(f"[blue]Image size:[/blue] {width}x{height}")
        console.print(f"[blue]Font size:[/blue] {font_size}")
        console.print(f"[blue]Text:[/blue] '{validated_text}'")

    # Find font files
    font_files = list(fonts_dir.glob("*.ttf"))
    if not font_files:
        console.print(f"[yellow]Warning:[/yellow] No .ttf files found in {fonts_dir}")
        logger.warning("No TTF files found in directory: %s", fonts_dir)
        raise typer.Exit(0)

    logger.info("Found %d font files to process", len(font_files))
    console.print(f"[green]Processing {len(font_files)} font files...[/green]")

    success_count = 0
    error_count = 0
    errors_details = []

    with console.status("[bold green]Generating font samples...") as status:
        for font_file in font_files:
            output_path = output_dir / f"{font_file.stem}.png"

            if verbose:
                status.update(f"Processing {font_file.name}...")

            logger.debug("Processing font: %s -> %s", font_file.name, output_path.name)

            try:
                generator = FontSampleGenerator(
                    str(font_file),
                    validated_text,
                    image_size_tuple,
                    font_size
                )
                generator.generate_sample(str(output_path))

                if verbose:
                    console.print(f"[green]✓[/green] Generated: {output_path}")

                success_count += 1
                logger.debug("Successfully generated sample for %s", font_file.name)

            except FontSampleError as e:
                error_msg = f"Error processing {font_file.name}: {e}"
                console.print(f"[red]✗[/red] {error_msg}")
                logger.error("Font processing error for %s: %s", font_file.name, e)
                errors_details.append((font_file.name, str(e)))
                error_count += 1

            except Exception as e:
                error_msg = f"Unexpected error processing {font_file.name}: {e}"
                console.print(f"[red]✗[/red] {error_msg}")
                logger.error("Unexpected error for %s: %s", font_file.name, e, exc_info=True)
                errors_details.append((font_file.name, f"Unexpected error: {e}"))
                error_count += 1

    # Summary reporting
    console.print("\n[bold green]Summary:[/bold green]")
    console.print(f"  Successfully generated: {success_count} samples")

    if error_count > 0:
        console.print(f"  [red]Failed:[/red] {error_count} files")

        if verbose and errors_details:
            console.print("\n[yellow]Error details:[/yellow]")
            for font_name, error_detail in errors_details:
                console.print(f"  • {font_name}: {error_detail}")

        logger.warning("Processing completed with %d errors out of %d files",
                      error_count, len(font_files))
        raise typer.Exit(1)

    logger.info("All font samples generated successfully")
    console.print(f"\n[green]All samples saved to:[/green] {output_dir}")


def main() -> None:
    """Main CLI entry point.

    This function serves as the entry point for the fontsamples command.
    It initializes the typer application and runs the main command.
    """
    typer.run(main_command)


if __name__ == "__main__":
    main()
