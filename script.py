import os

from main import FontSampleGenerator

# Define constant parameters
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
image_size = (250, 250)
font_size = 35
directory = "./fonts/"  # replace with the path to your directory

# Ensure the output directory exists
if not os.path.exists("./output_files/"):
    os.makedirs("./output_files/")

# Loop through all .ttf files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".ttf"):
        font_path = os.path.join(directory, filename)
        output_path = f"./output_files/{filename[:-4]}.png"  # remove the .ttf extension and add .png

        # Initialize FontSampleGenerator and generate the sample
        generator = FontSampleGenerator(font_path, text, image_size, font_size)
        generator.generate_sample(output_path)
