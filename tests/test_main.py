"""Tests for fontsamples package."""

import os
from pathlib import Path
from typing import Generator

import pytest
from PIL import Image, ImageFont

from fontsamples.generator import FontSampleGenerator


@pytest.fixture
def sample_generator() -> FontSampleGenerator:
    """Create a FontSampleGenerator instance for testing."""
    return FontSampleGenerator(
        font_path="./tests/test_font.ttf",  # Reference the bundled font
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        image_size=(250, 250),
        font_size=45,
    )


@pytest.fixture
def temp_output_path() -> Generator[str, None, None]:
    """Provide a temporary output path and clean up after test."""
    output_path = "test_output.png"
    yield output_path
    if os.path.exists(output_path):
        os.remove(output_path)


def test_functional(sample_generator: FontSampleGenerator, temp_output_path: str) -> None:
    """Test that the program runs without errors."""
    try:
        sample_generator.generate_sample(output_path=temp_output_path)
    except Exception as e:
        pytest.fail(f"Function raised {e} unexpectedly!")


def test_output_verification(sample_generator: FontSampleGenerator, temp_output_path: str) -> None:
    """Test if the image file is created in the expected directory."""
    sample_generator.generate_sample(temp_output_path)
    assert os.path.exists(temp_output_path)


def test_content_verification(sample_generator: FontSampleGenerator) -> None:
    """Validate that the image generated has the expected properties like dimensions."""
    output_path = "test_output_content.png"
    try:
        sample_generator.generate_sample(output_path)

        with Image.open(output_path) as img:
            assert img.size == (250, 250)
            assert img.mode == "RGB"
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def test_font_verification(sample_generator: FontSampleGenerator) -> None:
    """Confirm that the bundled font can be loaded."""
    assert os.path.exists(sample_generator.font_path)

    try:
        ImageFont.truetype(sample_generator.font_path, sample_generator.font_size)
    except Exception as e:
        pytest.fail(f"Font at {sample_generator.font_path} couldn't be loaded: {e}")


def test_invalid_font_path() -> None:
    """Test that invalid font path raises appropriate exception."""
    generator = FontSampleGenerator(
        font_path="./nonexistent_font.ttf",
        text="Test",
        image_size=(100, 100),
        font_size=20,
    )

    with pytest.raises(Exception, match="Unable to load font"):
        generator.generate_sample("test_invalid.png")


def test_cli_module_import() -> None:
    """Test that CLI module can be imported."""
    try:
        from fontsamples.cli import main
        assert callable(main)
    except ImportError as e:
        pytest.fail(f"Could not import CLI module: {e}")


def test_package_import() -> None:
    """Test that package can be imported correctly."""
    try:
        import fontsamples
        assert hasattr(fontsamples, "FontSampleGenerator")
        assert fontsamples.__version__ is not None
    except ImportError as e:
        pytest.fail(f"Could not import package: {e}")