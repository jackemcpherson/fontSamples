import textwrap
from PIL import Image, ImageFont, ImageDraw


def generate_font_sample(font_path, text, image_size, font_size, output_path):
    # Create a new image with white background
    img = Image.new("RGB", image_size, "#F8F5F0")
    draw = ImageDraw.Draw(img)

    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Unable to load font at {font_path}")
        return

    # Calculate the maximum width of a line
    max_width = image_size[0] - 20  # subtract a small margin

    # Wrap the text
    lines = textwrap.wrap(text, width=int(max_width / font_size))

    # Calculate total height of the text
    total_text_height = len(lines) * font.getsize(lines[0])[1]

    # Calculate start height to center vertically
    start_height = (image_size[1] - total_text_height) / 2

    current_height = start_height  # start drawing text from the start height
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        if (
            text_width > max_width
        ):  # if the line is still too wide, reduce the font size
            while text_width > max_width:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(line, font=font)

        # Calculate the width of the line to center it
        width = (image_size[0] - text_width) / 2
        # Draw the line
        draw.text((width, current_height), line, fill="black", font=font)

        current_height += (
            text_height  # update the current height position for the next line
        )

    # Save the image
    img.save(output_path)


font_path = "./fonts/reader-medium-pro.ttf"  # replace with the path to your .ttf file
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
image_size = (250, 250)  # replace with the desired image size
font_size = 45  # replace with the desired font size
output_path = "output_files/output.png"  # replace with the desired output path

generate_font_sample(font_path, text, image_size, font_size, output_path)
