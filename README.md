# Font Samples Generator

This project provides an easy way to generate image samples of fonts. It's particularly useful for getting a visual representation of what different fonts look like with a specified text.

## Features

- **Font Sample Creation**: Generate a visual representation of a font with the specified text.
- **Customizable**: Adjust the size of the generated image and font size as needed.

## Temporary Script Usage

Currently, the project includes a temporary script that can generate font samples for all `.ttf` font files in a specified directory. The output samples are saved in the `./output_files/` directory.

```python
from main import FontSampleGenerator

# Define your parameters
text = "Your Sample Text"
image_size = (250, 250)
font_size = 35
directory = "./your_font_directory/"

# Use the script to generate samples
for filename in os.listdir(directory):
    if filename.endswith(".ttf"):
        font_path = os.path.join(directory, filename)
        output_path = f"./output_files/{filename[:-4]}.png"

        generator = FontSampleGenerator(font_path, text, image_size, font_size)
        generator.generate_sample(output_path)
```

## Upcoming Features

Frontend/CLI Component: In future iterations, we're looking forward to integrating a frontend or a command-line interface for easier user interactions, replacing the need for the temporary script.

## Contributing

If you have suggestions or want to improve the tool, feel free to open an issue or send a pull request.
