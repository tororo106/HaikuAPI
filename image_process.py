import base64
import uuid
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple
from io import BytesIO

vertical_hyphen = '│'

def load_font(font_path: str, font_size: float) -> ImageFont.FreeTypeFont:
    try:
        font = ImageFont.truetype(font_path, int(font_size))
        return font
    except IOError as e:
        print(f"Error loading font '{font_path}': {e}")
        raise e

def add_horizontal_label(img: Image.Image, left_x: int, bottom_y: int, label: str,
                        font_path: str, font_size: float, font_color: Tuple[int, int, int, int]) -> None:
    draw = ImageDraw.Draw(img)
    font = load_font(font_path, font_size)
    text_size = draw.textsize(label, font=font)
    top_left = (left_x, bottom_y - text_size[1])
    draw.text(top_left, label, font=font, fill=font_color)

def add_vertical_label(img: Image.Image, left_x: int, top_y: int, label: str,
                      font_path: str, font_size: float, font_color: Tuple[int, int, int, int]) -> None:
    draw = ImageDraw.Draw(img)
    font = load_font(font_path, font_size)
    y = top_y
    for char in label:
        if char in ['〜', '~', '-', 'ー']:
            char = vertical_hyphen
        char_size = draw.textsize(char, font=font)
        draw.text((left_x, y), char, font=font, fill=font_color)
        y += char_size[1]

def add_vertical_top_align_label(img: Image.Image, left_x: int, label: str,
                                 font_path: str, font_size: float, font_color: Tuple[int, int, int, int],
                                 margin_px: int) -> None:
    add_vertical_label(img, left_x, margin_px, label, font_path, font_size, font_color)

def add_vertical_center_align_label(img: Image.Image, left_x: int, label: str,
                                    font_path: str, font_size: float, font_color: Tuple[int, int, int, int],
                                    margin_px: int) -> None:
    draw = ImageDraw.Draw(img)
    font = load_font(font_path, font_size)
    label_length = len(label)
    label_height = label_length * int(font_size)
    image_height = img.height
    padding = (image_height - 2 * margin_px - label_height) // 2
    y = margin_px + padding
    add_vertical_label(img, left_x, y, label, font_path, font_size, font_color)


def add_vertical_bottom_align_label(img: Image.Image, left_x: int, label: str,
                                    font_path: str, font_size: float, font_color: Tuple[int, int, int, int],
                                    margin_px: int) -> None:
    draw = ImageDraw.Draw(img)
    font = load_font(font_path, font_size)
    label_length = len(label)
    label_height = label_length * int(font_size)
    y = img.height - label_height - margin_px
    add_vertical_label(img, left_x, y, label, font_path, font_size, font_color)

def get_size(img: Image.Image) -> Tuple[int, int]:
    return img.size

def rect(img: Image.Image, x1: int, y1: int, x2: int, y2: int,
         thickness_px: int, color: Tuple[int, int, int, int]) -> None:
    draw = ImageDraw.Draw(img)
    for i in range(thickness_px):
        draw.line([(x1 + i, y1 + i), (x2 - i, y1 + i)], fill=color)
        draw.line([(x1 + i, y2 - i), (x2 - i, y2 - i)], fill=color)
        draw.line([(x1 + i, y1 + i), (x1 + i, y2 - i)], fill=color)
        draw.line([(x2 - i, y1 + i), (x2 - i, y2 - i)], fill=color)

def save_image(img: Image.Image, file_path: str) -> None:
    img.save(file_path, format='PNG')

def set_background_color(img: Image.Image, bg_color: Tuple[int, int, int, int]) -> None:
    background = Image.new('RGBA', img.size, bg_color)
    img.paste(background, (0, 0))

def new_image(width: int, height: int, background_color: Tuple[int, int, int, int]) -> Image.Image:
    return Image.new('RGBA', (width, height), background_color)

def paste_image(img: Image.Image, image_to_paste: Image.Image, left_x: int, top_y: int) -> None:
    img.paste(image_to_paste, (left_x, top_y), image_to_paste)

def resize_image(img: Image.Image, to_width: int, to_height: int) -> Image.Image:
    return img.resize((to_width, to_height), Image.ANTIALIAS)

def new_unique_file_name(extension: str) -> str:
    return f"{uuid.uuid4()}.{extension}"

def image_file_base64_encode(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_base64_encode(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
