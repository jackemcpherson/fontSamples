# Font Samples Generator

A Python tool for generating visual samples of fonts as images.

## Installation

```bash
# Using uv (recommended)
uv add fontsamples

# Using pip
pip install fontsamples
```

## Usage

### Command Line

```bash
# Generate samples for all fonts in a directory
fontsamples --fonts-dir ./fonts/ --output-dir ./samples/

# Customize the output
fontsamples -t "Hello World" -s 48 -i 400x200 -f ./fonts/ -o ./samples/ -v
```

### Python API

```python
from fontsamples import FontSampleGenerator

generator = FontSampleGenerator(
    font_path="./fonts/MyFont.ttf",
    text="Hello, World!",
    image_size=(300, 150),
    font_size=32
)
generator.generate_sample("./output/sample.png")
```

## Development

```bash
git clone https://github.com/jackmcpherson/fontSamples.git
cd fontSamples
uv sync --dev

# Run tests
uv run pytest

# Code quality
uv run ruff check
uv run mypy src/
```

## License

MIT License