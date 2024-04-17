from PIL import Image, ImageDraw, ImageFont
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
import os
from math import ceil
import argparse


# Constants
PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1
COMMON_MONO_FONT_FILENAMES = [
    'DejaVuSansMono.ttf',  # Linux
    'Consolas Mono.ttf',   # MacOS
    'Arial.ttf',           # Windows
]
_DEFAULT_FONT = os.path.join(os.path.dirname(
    __file__), 'font', 'NotoSansCJK-Bold.ttc')


def drawimage(imagepath: str, saveas: str, scale: int) -> tuple[int, int]:
    """
    Converts an image file to a text file representation using ASCII characters.

    Args:
        imagepath (str): The path to the input image file.
        saveas (str): The path to save the output text file.
        scale (int): The scaling factor to resize the image.

    Returns:
        tuple[int, int]: A tuple containing the width and height of the resized image.
    """
    img = Image.open(imagepath)
    w, h = img.size
    _, extension = os.path.splitext(imagepath)
    img.resize((w//scale, h//scale)).save(f"resized.{extension.lower()}")
    img = Image.open(f"resized.{extension.lower()}")
    w, h = img.size

    grid = []
    for i in range(h):
        grid.append(["X"] * w)
    pix = img.load()

    for y in range(h):
        for x in range(w):
            if sum(pix[x, y]) == 0:
                grid[y][x] = "#"
            elif sum(pix[x, y]) in range(1, 100):
                grid[y][x] = "X"
            elif sum(pix[x, y]) in range(100, 200):
                grid[y][x] = "%"
            elif sum(pix[x, y]) in range(200, 300):
                grid[y][x] = "&"
            elif sum(pix[x, y]) in range(300, 400):
                grid[y][x] = "*"
            elif sum(pix[x, y]) in range(400, 500):
                grid[y][x] = "+"
            elif sum(pix[x, y]) in range(500, 600):
                grid[y][x] = "^"
            elif sum(pix[x, y]) in range(600, 700):
                grid[y][x] = "'"
            elif sum(pix[x, y]) in range(700, 750):
                grid[y][x] = "-"
            else:
                grid[y][x] = " "
    art = open(saveas, "w")

    for row in grid:
        art.write("".join(row)+"\n")

    art.close()
    return w, h


def textfile_to_image(textfile_path: str, target_width: int, target_height: int, font_size: int = 12) -> Image.Image:
    """
    Converts a text file to an image with specified width and height.

    Args:
        textfile_path (str): The path to the input text file.
        target_width (int): The desired width of the output image.
        target_height (int): The desired height of the output image.
        font_size (int, optional): The font size to use for rendering the text. Defaults to 12.

    Returns:
        PIL.Image.Image: The generated image from the text file.
    """

    with open(textfile_path, 'r') as f:
        ascii_text = f.read()

    lines = ascii_text.split('\n')
    num_lines = len(lines)
    longest_line = max(lines, key=len)

    font = ImageFont.load_default()
    _, _, char_width, char_height = font.getbbox("X")

    orig_width = len(longest_line) * char_width
    orig_height = num_lines * char_height

    aspect_ratio = orig_width / orig_height

    if aspect_ratio > (target_width / target_height):
        W = target_width
        H = int(W / aspect_ratio)
    else:
        H = target_height
        W = int(H * aspect_ratio)

    img = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(img)

    char_width = W / len(longest_line)
    char_height = H / num_lines
    x, y = 0, 0
    for line in lines:
        for char in line:
            draw.text((x, y), char, fill="black", font=font)
            x += char_width
        x = 0
        y += char_height

    return img


def main(args):
    drawimage(args.input_image, "new.txt", args.ascii_scale)
    image = textfile_to_image('new.txt', 1000, 1000)
    image.show()
    image.save(args.output_image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Image_to_Ascii_to_Image",
        description="Converts an image to ASCII art and back to an image."
    )
    parser.add_argument(
        "-f",
        "--input_image",
        required=True,
        help="Path to the input image file."
    )
    parser.add_argument(
        "-o",
        "--output_image",
        default="output.png",
        help="Name for the output image file."
    )
    parser.add_argument(
        "-s",
        "--ascii_scale",
        type=int,
        default=5,
        help="Scaling factor for the ASCII conversion."
    )
    args = parser.parse_args()
    main(args)
