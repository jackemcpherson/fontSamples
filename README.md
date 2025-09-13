# Font Samples Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](https://mypy-lang.org/)

A modern Python package for generating visual samples of fonts as images. Perfect for font previews, documentation, and design workflows.

## Features

- **🎨 Visual Font Samples**: Generate clean, professional-looking font samples
- **⚡ Fast Processing**: Efficiently process multiple fonts in batch
- **🎛️ Customizable**: Adjust text, size, dimensions, and styling
- **📦 Easy Installation**: Modern packaging with uv support
- **🔧 Developer-Friendly**: CLI interface and Python API
- **📐 Smart Text Handling**: Automatic text wrapping and font scaling
- **🎯 Type Safe**: Full type annotations and mypy compatibility

## Installation

### Using uv (recommended)

```bash
uv add fontsamples
```

### Using pip

```bash
pip install fontsamples
```

### Development Installation

```bash
git clone https://github.com/jackmcpherson/fontSamples.git
cd fontSamples
uv sync --dev
```

## Quick Start

### Command Line Interface

Generate samples for all fonts in a directory:

```bash
fontsamples --fonts-dir ./fonts/ --output-dir ./samples/
```

Customize the output:

```bash
fontsamples \
    --text "The Quick Brown Fox" \
    --font-size 48 \
    --image-size 400x200 \
    --fonts-dir ./fonts/ \
    --output-dir ./samples/
```

### Python API

```python
from fontsamples import FontSampleGenerator

# Generate a single font sample
generator = FontSampleGenerator(
    font_path="./fonts/MyFont.ttf",
    text="Hello, World!",
    image_size=(300, 150),
    font_size=32
)
generator.generate_sample("./output/sample.png")

# Batch process multiple fonts
import os
from pathlib import Path

fonts_dir = Path("./fonts")
output_dir = Path("./samples")
output_dir.mkdir(exist_ok=True)

for font_file in fonts_dir.glob("*.ttf"):
    generator = FontSampleGenerator(
        font_path=str(font_file),
        text="Sample Text",
        image_size=(250, 250),
        font_size=35
    )
    output_path = output_dir / f"{font_file.stem}.png"
    generator.generate_sample(str(output_path))
```

## Project Structure

This project follows modern Python packaging standards:

```
fontSamples/
├── src/fontsamples/          # Source package
│   ├── __init__.py          # Package exports
│   ├── generator.py         # Core FontSampleGenerator class
│   └── cli.py              # Command-line interface
├── tests/                   # Test suite
│   ├── test_main.py        # Main test file
│   └── test_font.ttf       # Bundled test font
├── fonts/                  # Input fonts directory
├── output_files/           # Generated samples directory
├── pyproject.toml          # Modern Python project configuration
└── README.md              # This file
```

## Development

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jackmcpherson/fontSamples.git
cd fontSamples

# Install dependencies
uv sync --dev

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### Development Commands

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=fontsamples --cov-report=html

# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/

# Run all quality checks
uv run ruff check && uv run ruff format --check && uv run mypy src/ && uv run pytest
```

### Building and Publishing

```bash
# Build package
uv build

# Install locally for testing
uv pip install dist/*.whl
```

## Architecture

### Core Components

- **FontSampleGenerator**: Main class handling font rendering and image generation
- **CLI Module**: Command-line interface for batch processing
- **Smart Text Processing**: Automatic wrapping, scaling, and centering

### Font Processing Pipeline

1. **Font Loading**: Validate and load font file using PIL
2. **Text Analysis**: Calculate text dimensions and wrapping requirements
3. **Dynamic Scaling**: Adjust font size if text exceeds image bounds
4. **Layout Calculation**: Center text vertically with proper line spacing
5. **Rendering**: Generate final image with customizable background
6. **Output**: Save as PNG with optimized settings

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks (`uv run ruff check && uv run mypy src/ && uv run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Tooling Migration

This project uses modern Python tooling:

- **uv**: Fast Python package manager and resolver
- **ruff**: Lightning-fast linter and formatter
- **mypy**: Static type checker
- **pytest**: Testing framework
- **hatchling**: Build backend

> **Future Migration Note**: We plan to migrate from mypy to [ty](https://github.com/astral-sh/ty) (Astral's new type checker) once it reaches stable release in late 2025. ty promises significantly faster type checking performance while maintaining compatibility.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Pillow](https://python-pillow.org/) for image processing
- Powered by [uv](https://docs.astral.sh/uv/) and [ruff](https://docs.astral.sh/ruff/) from Astral
- Inspired by the need for better font preview tools