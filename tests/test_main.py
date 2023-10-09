import os
import pytest
from PIL import Image, ImageFont
from main import FontSampleGenerator


@pytest.fixture
def sample_generator():
    return FontSampleGenerator(
        font_path="./fonts/reader-medium-pro.ttf",
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        image_size=(250, 250),
        font_size=45,
    )


def test_functional(sample_generator):
    """Test that the program runs without errors."""
    try:
        sample_generator.generate_sample(output_path="test_output.png")
        os.remove("test_output.png")  # Clean up after test
    except Exception as e:
        pytest.fail(f"Function raised {e} unexpectedly!")


def test_output_verification(sample_generator):
    """Test if the image file is created in the expected directory."""
    output_path = "test_output.png"
    sample_generator.generate_sample(output_path)
    assert os.path.exists(output_path)
    os.remove(output_path)  # Clean up after test


def test_content_verification(sample_generator):
    """Validate that the image generated has the expected properties like dimensions."""
    output_path = "test_output_content.png"
    sample_generator.generate_sample(output_path)

    with Image.open(output_path) as img:
        assert img.size == (250, 250)
        assert img.mode == "RGB"

    os.remove(output_path)  # Clean up after test


def test_font_verification(sample_generator):
    """Confirm that the text rendered can use the desired font."""
    assert os.path.exists(sample_generator.font_path)

    try:
        ImageFont.truetype(sample_generator.font_path, sample_generator.font_size)
    except Exception:
        pytest.fail(f"Font at {sample_generator.font_path} couldn't be loaded!")
