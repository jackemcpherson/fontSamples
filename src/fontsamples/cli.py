"""Command-line interface for Font Samples Generator."""

from pathlib import Path
from typing import Tuple

import typer
from rich.console import Console
from typing_extensions import Annotated

from .generator import FontSampleGenerator

app = typer.Typer(
    name="fontsamples",
    help="Generate visual samples of fonts as images",
    add_completion=False,
)
console = Console()


def parse_image_size(size_str: str) -> Tuple[int, int]:
    """Parse image size string like '250x250' into tuple."""
    try:
        width, height = map(int, size_str.split('x'))
        return (width, height)
    except ValueError:
        raise typer.BadParameter(f"Invalid image size format: {size_str}. Use WIDTHxHEIGHT")


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
            help="Enable verbose output"
        )
    ] = False,
) -> None:
    """
    Generate visual samples for all TTF fonts in the specified directory.

    This command processes all .ttf files in the fonts directory and creates
    image samples with the specified text, saving them to the output directory.
    """
    # Parse image size
    try:
        width, height = parse_image_size(image_size)
        image_size_tuple: Tuple[int, int] = (width, height)
    except typer.BadParameter as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        console.print(f"[blue]Output directory:[/blue] {output_dir}")
        console.print(f"[blue]Fonts directory:[/blue] {fonts_dir}")
        console.print(f"[blue]Image size:[/blue] {width}x{height}")
        console.print(f"[blue]Font size:[/blue] {font_size}")
        console.print(f"[blue]Text:[/blue] '{text}'")

    # Process all .ttf files
    font_files = list(fonts_dir.glob("*.ttf"))
    if not font_files:
        console.print(f"[yellow]Warning:[/yellow] No .ttf files found in {fonts_dir}")
        raise typer.Exit(0)

    console.print(f"[green]Processing {len(font_files)} font files...[/green]")

    success_count = 0
    error_count = 0

    with console.status("[bold green]Generating font samples...") as status:
        for font_file in font_files:
            output_path = output_dir / f"{font_file.stem}.png"

            if verbose:
                status.update(f"Processing {font_file.name}...")

            try:
                generator = FontSampleGenerator(
                    str(font_file),
                    text,
                    image_size_tuple,
                    font_size
                )
                generator.generate_sample(str(output_path))

                if verbose:
                    console.print(f"[green]✓[/green] Generated: {output_path}")

                success_count += 1

            except Exception as e:
                console.print(f"[red]✗[/red] Error processing {font_file.name}: {e}")
                error_count += 1

    # Summary
    console.print(f"\n[bold green]Summary:[/bold green]")
    console.print(f"  Successfully generated: {success_count} samples")
    if error_count > 0:
        console.print(f"  [red]Failed:[/red] {error_count} files")
        console.print(f"  [yellow]Check error messages above for details.[/yellow]")

    if error_count > 0:
        raise typer.Exit(1)


def main() -> None:
    """Main CLI entry point."""
    typer.run(main_command)


if __name__ == "__main__":
    main()