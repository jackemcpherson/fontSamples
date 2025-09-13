"""Tests for fontsamples package."""

import os
import tempfile
from pathlib import Path

import pytest
from PIL import Image, ImageFont

from fontsamples import (
    FontLoadError,
    FontSampleError,
    FontSampleGenerator,
    ImageGenerationError,
)


@pytest.fixture
def test_font_path() -> Path:
    """Get path to test font file."""
    return Path("./tests/test_font.ttf").resolve()


@pytest.fixture
def sample_generator(test_font_path: Path) -> FontSampleGenerator:
    """Create a FontSampleGenerator instance for testing."""
    return FontSampleGenerator(
        font_path=str(test_font_path),
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        image_size=(250, 250),
        font_size=45,
    )


@pytest.fixture
def temp_output_file() -> str:
    """Provide a temporary output file and clean up after test."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        output_path = tmp_file.name

    yield output_path

    if os.path.exists(output_path):
        os.remove(output_path)


def test_functional(sample_generator: FontSampleGenerator, temp_output_file: str) -> None:
    """Test that the program runs without errors."""
    sample_generator.generate_sample(output_path=temp_output_file)
    assert os.path.exists(temp_output_file)


def test_output_verification(sample_generator: FontSampleGenerator, temp_output_file: str) -> None:
    """Test if the image file is created in the expected directory."""
    sample_generator.generate_sample(temp_output_file)
    assert os.path.exists(temp_output_file)
    assert os.path.getsize(temp_output_file) > 0  # File should not be empty


def test_content_verification(sample_generator: FontSampleGenerator, temp_output_file: str) -> None:
    """Validate that the image generated has the expected properties like dimensions."""
    sample_generator.generate_sample(temp_output_file)

    with Image.open(temp_output_file) as img:
        assert img.size == (250, 250)
        assert img.mode == "RGB"


def test_font_verification(sample_generator: FontSampleGenerator) -> None:
    """Confirm that the bundled font can be loaded."""
    assert sample_generator.font_path.exists()

    # Test that the font can be loaded directly
    font = ImageFont.truetype(str(sample_generator.font_path), sample_generator.font_size)
    assert font is not None


def test_invalid_font_path() -> None:
    """Test that invalid font path raises FontLoadError during initialization."""
    with pytest.raises(FontLoadError, match="Font file not found"):
        FontSampleGenerator(
            font_path="./nonexistent_font.ttf",
            text="Test",
            image_size=(100, 100),
            font_size=20,
        )


def test_empty_text_raises_error() -> None:
    """Test that empty text raises ValueError."""
    with pytest.raises(ValueError, match="Text cannot be empty"):
        FontSampleGenerator(
            font_path="./tests/test_font.ttf",
            text="",
            image_size=(100, 100),
            font_size=20,
        )


def test_invalid_font_size_raises_error() -> None:
    """Test that invalid font size raises ValueError."""
    with pytest.raises(ValueError, match="Font size must be at least"):
        FontSampleGenerator(
            font_path="./tests/test_font.ttf",
            text="Test",
            image_size=(100, 100),
            font_size=5,  # Too small
        )


def test_invalid_image_dimensions_raises_error() -> None:
    """Test that invalid image dimensions raise ValueError."""
    with pytest.raises(ValueError, match="Image dimensions must be positive"):
        FontSampleGenerator(
            font_path="./tests/test_font.ttf",
            text="Test",
            image_size=(0, 100),  # Invalid width
            font_size=20,
        )

    with pytest.raises(ValueError, match="Image dimensions must be positive"):
        FontSampleGenerator(
            font_path="./tests/test_font.ttf",
            text="Test",
            image_size=(100, -50),  # Invalid height
            font_size=20,
        )


def test_whitespace_only_text_raises_error() -> None:
    """Test that whitespace-only text raises ValueError."""
    with pytest.raises(ValueError, match="Text cannot be empty"):
        FontSampleGenerator(
            font_path="./tests/test_font.ttf",
            text="   \t\n  ",  # Only whitespace
            image_size=(100, 100),
            font_size=20,
        )


def test_small_image_size(test_font_path: Path, temp_output_file: str) -> None:
    """Test that very small image sizes work correctly."""
    generator = FontSampleGenerator(
        font_path=str(test_font_path),
        text="Hi",
        image_size=(50, 50),
        font_size=10,
    )
    generator.generate_sample(temp_output_file)

    with Image.open(temp_output_file) as img:
        assert img.size == (50, 50)


def test_large_text_wrapping(test_font_path: Path, temp_output_file: str) -> None:
    """Test that long text is wrapped correctly."""
    long_text = "This is a very long text that should be wrapped across multiple lines when rendered"
    generator = FontSampleGenerator(
        font_path=str(test_font_path),
        text=long_text,
        image_size=(200, 200),
        font_size=16,
    )
    generator.generate_sample(temp_output_file)

    with Image.open(temp_output_file) as img:
        assert img.size == (200, 200)


def test_output_directory_creation(test_font_path: Path) -> None:
    """Test that output directories are created automatically."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "subdir" / "test_output.png"

        generator = FontSampleGenerator(
            font_path=str(test_font_path),
            text="Test",
            image_size=(100, 100),
            font_size=20,
        )

        generator.generate_sample(str(output_path))
        assert output_path.exists()


def test_cli_module_import() -> None:
    """Test that CLI module can be imported."""
    from fontsamples.cli import main
    assert callable(main)


def test_package_import() -> None:
    """Test that package can be imported correctly."""
    import fontsamples
    assert hasattr(fontsamples, "FontSampleGenerator")
    assert hasattr(fontsamples, "FontSampleError")
    assert hasattr(fontsamples, "FontLoadError")
    assert hasattr(fontsamples, "ImageGenerationError")
    assert fontsamples.__version__ is not None


def test_exception_hierarchy() -> None:
    """Test that exception hierarchy is correct."""
    assert issubclass(FontLoadError, FontSampleError)
    assert issubclass(ImageGenerationError, FontSampleError)
    assert issubclass(FontSampleError, Exception)


def test_constants_defined() -> None:
    """Test that constants are properly defined in the class."""
    assert hasattr(FontSampleGenerator, "LINE_SPACING_RATIO")
    assert hasattr(FontSampleGenerator, "MIN_FONT_SIZE")
    assert hasattr(FontSampleGenerator, "IMAGE_PADDING")
    assert hasattr(FontSampleGenerator, "BACKGROUND_COLOR")
    assert hasattr(FontSampleGenerator, "TEXT_COLOR")

    assert FontSampleGenerator.LINE_SPACING_RATIO == 0.2
    assert FontSampleGenerator.MIN_FONT_SIZE == 10
    assert FontSampleGenerator.IMAGE_PADDING == 20


def test_font_size_adjustment(test_font_path: Path, temp_output_file: str) -> None:
    """Test that font size adjustment works for very wide text."""
    # Use a very long text with large font size on small image
    initial_font_size = 50
    generator = FontSampleGenerator(
        font_path=str(test_font_path),
        text="WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        image_size=(100, 100),
        font_size=initial_font_size,
    )

    # The original font_size should remain unchanged (new behavior)
    assert generator.font_size == initial_font_size

    # But the sample should still be generated successfully with adjusted font
    generator.generate_sample(temp_output_file)
    assert os.path.exists(temp_output_file)

    # Verify the image was created with proper dimensions
    with Image.open(temp_output_file) as img:
        assert img.size == (100, 100)


def test_path_object_handling(test_font_path: Path, temp_output_file: str) -> None:
    """Test that Path objects are handled correctly."""
    generator = FontSampleGenerator(
        font_path=str(test_font_path),
        text="Test",
        image_size=(100, 100),
        font_size=20,
    )

    # The font_path should be converted to a resolved Path object
    assert isinstance(generator.font_path, Path)
    assert generator.font_path.is_absolute()
