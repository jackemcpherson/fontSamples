# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Font Samples Generator is a modern Python package that creates visual samples of fonts by rendering specified text as images. The project follows current Python packaging standards with src-layout structure and modern tooling.

## Development Commands

### Environment Setup
```bash
uv sync --dev                    # Install all dependencies including dev tools
uv sync                         # Install only production dependencies
source .venv/bin/activate       # Activate virtual environment (Linux/macOS)
.venv\Scripts\activate          # Activate virtual environment (Windows)
```

### Code Quality
```bash
uv run ruff check              # Lint code
uv run ruff format             # Format code
uv run ruff check --fix        # Auto-fix linting issues
uv run mypy src/               # Type checking
```

### Testing
```bash
uv run pytest                          # Run all tests
uv run pytest tests/test_main.py       # Run specific test file
uv run pytest -v                       # Run tests with verbose output
uv run pytest --cov=fontsamples        # Run tests with coverage
uv run pytest --cov=fontsamples --cov-report=html  # Generate HTML coverage report
```

### Package Management
```bash
uv add <package>               # Add a new dependency
uv add --dev <package>         # Add a development dependency
uv remove <package>            # Remove a dependency
uv build                       # Build package for distribution
uv pip install dist/*.whl     # Install built package locally
```

### CLI Usage
```bash
uv run fontsamples --help                    # Show CLI help with rich formatting
uv run fontsamples -f ./fonts/ -o ./samples/  # Generate samples (short options)
uv run fontsamples --fonts-dir ./fonts/ --verbose  # Verbose mode with progress indicators
uv run fontsamples -t "Hello World" -s 48 -i 400x200  # Custom text, font size, and image size
uv run python -m fontsamples.cli            # Alternative CLI invocation
```

## Architecture

### Package Structure (src-layout)
- **`src/fontsamples/`**: Main package directory
  - **`__init__.py`**: Package exports and version
  - **`generator.py`**: Core `FontSampleGenerator` class (moved from `main.py`)
  - **`cli.py`**: Command-line interface (enhanced from `script.py`)
- **`tests/`**: Test suite with type annotations and modern pytest practices
- **`fonts/`**: Input directory for font files
- **`output_files/`**: Generated font sample images

### FontSampleGenerator Class (`src/fontsamples/generator.py`)
The core class handles:
- Font file loading and validation
- Text wrapping based on image dimensions
- Dynamic font size adjustment when text exceeds bounds
- Vertical text centering with proper line spacing
- Image generation with customizable background

### CLI Module (`src/fontsamples/cli.py`)
Modern command-line interface built with typer and rich, featuring:
- Type-hint based argument parsing with typer
- Rich colored output with progress indicators and status updates
- Short option aliases (-t, -s, -i, -f, -o, -v) for faster usage
- Built-in validation with helpful error messages
- Verbose mode for detailed processing information
- Configurable text, font size, and image dimensions
- Batch processing of font directories with success/error tracking
- Entry point via `fontsamples` command

### Font Processing Pipeline
1. **Validation**: Check font file existence and validity
2. **Text Analysis**: Calculate wrapping requirements and dimensions
3. **Dynamic Scaling**: Adjust font size if text exceeds image width
4. **Layout Calculation**: Center text vertically with 20% line spacing
5. **Rendering**: Generate image with cream background (#F8F5F0)
6. **Output**: Save as PNG with error handling

## Modern Tooling Stack

### Package Management: uv
- Fast dependency resolution and installation
- Virtual environment management
- Build system integration
- Lock file for reproducible builds

### Code Quality: ruff
- Fast linting (pycodestyle, pyflakes, isort, etc.)
- Automatic code formatting
- Import sorting and unused import removal
- Configured for Python 3.8+ compatibility

### Type Checking: mypy
- Static type analysis with strict configuration
- Full type annotation requirements
- Integration with IDE type checking
- **Future**: Will migrate to [ty](https://github.com/astral-sh/ty) when stable (late 2025)

### Testing: pytest
- Modern test fixtures and parametrization
- Coverage reporting integration
- Type-annotated test functions
- Automatic test discovery

### Build System: hatchling
- PEP 517/518 compliant build backend
- src-layout support
- Editable installs
- Distribution packaging

### CLI Framework: typer + rich
- Modern type-hint based CLI framework
- Automatic help generation from docstrings and type hints
- Built-in validation and error handling
- Rich terminal formatting with colors and progress indicators
- Short option aliases for improved usability

## Testing Strategy
- **Bundled Test Font**: `tests/test_font.ttf` ensures consistent cross-platform testing
- **Fixture-Based**: Proper pytest fixtures for setup/teardown
- **Type Annotations**: All test functions include type hints
- **Error Testing**: Validates error handling for invalid inputs
- **Integration Testing**: Tests CLI module imports and package structure
- **Coverage Tracking**: Measures test effectiveness

## Development Best Practices
- **Type Safety**: All code includes comprehensive type annotations
- **Error Handling**: Proper exception handling with descriptive messages
- **Documentation**: Docstrings for all public functions and classes
- **Path Handling**: Uses `pathlib.Path` for cross-platform compatibility
- **Resource Management**: Proper cleanup in tests and CLI operations