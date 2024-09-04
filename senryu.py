from dataclasses import dataclass, field
from typing import Optional, Tuple
from PIL import Image
import image_process as img_proc

DEFAULT_SENRYU_HEIGHT = 1000
DEFAULT_SENRYU_WIDTH = 550

DEFAULT_FIRST_SENTENCE_LEFT_X = 390
DEFAULT_SECOND_SENTENCE_LEFT_X = 270
DEFAULT_THIRD_SENTENCE_LEFT_X = 160
DEFAULT_AUTHOR_NAME_LEFT_X = 60

DEFAULT_FONT_SIZE = 90.0
DEFAULT_AUTHOR_NAME_FONT_SIZE = 50.0
DEFAULT_FONT_PATH = "fonts/default.ttf"

DEFAULT_MARGIN_PX = 70
DEFAULT_THICK_BORDER_PX = 40
DEFAULT_THIN_BORDER_PX = 10

DEFAULT_BACKGROUND_COLOR = (236, 236, 208, 255)
DEFAULT_FONT_COLOR = (0, 0, 0, 255)
DEFAULT_THICK_BORDER_COLOR = (0, 128, 79, 255)
DEFAULT_THIN_BORDER_COLOR = (151, 151, 53, 255)

DEFAULT_SERVICE_NAME_FONT_SIZE = 30.0

@dataclass
class Senryu:
    first_sentence: str
    second_sentence: str
    third_sentence: str
    author_name: str

@dataclass
class SenryuImageOption:
    senryu_height: Optional[int] = None
    senryu_width: Optional[int] = None
    first_sentence_left_x: Optional[int] = None
    second_sentence_left_x: Optional[int] = None
    third_sentence_left_x: Optional[int] = None
    author_name_left_x: Optional[int] = None
    font_size: Optional[float] = None
    author_name_font_size: Optional[float] = None
    font_path: Optional[str] = None
    margin_px: Optional[int] = None
    font_color: Optional[Tuple[int, int, int, int]] = None
    background_color: Optional[Tuple[int, int, int, int]] = None
    thick_border_color: Optional[Tuple[int, int, int, int]] = None
    thin_border_color: Optional[Tuple[int, int, int, int]] = None
    thick_border_px: Optional[int] = None
    thin_border_px: Optional[int] = None
    service_name: Optional[str] = None
    service_name_font_size: Optional[float] = None

def complete_senryu_image_option(option: SenryuImageOption) -> None:
    if option.senryu_height is None:
        option.senryu_height = DEFAULT_SENRYU_HEIGHT
    if option.senryu_width is None:
        option.senryu_width = DEFAULT_SENRYU_WIDTH
    if option.first_sentence_left_x is None:
        option.first_sentence_left_x = DEFAULT_FIRST_SENTENCE_LEFT_X
    if option.second_sentence_left_x is None:
        option.second_sentence_left_x = DEFAULT_SECOND_SENTENCE_LEFT_X
    if option.third_sentence_left_x is None:
        option.third_sentence_left_x = DEFAULT_THIRD_SENTENCE_LEFT_X
    if option.author_name_left_x is None:
        option.author_name_left_x = DEFAULT_AUTHOR_NAME_LEFT_X
    if option.font_color is None:
        option.font_color = DEFAULT_FONT_COLOR
    if option.font_path is None or option.font_path == "":
        option.font_path = DEFAULT_FONT_PATH
    if option.font_size is None or option.font_size == 0:
        option.font_size = DEFAULT_FONT_SIZE
    if option.author_name_font_size is None or option.author_name_font_size == 0:
        option.author_name_font_size = DEFAULT_AUTHOR_NAME_FONT_SIZE
    if option.background_color is None:
        option.background_color = DEFAULT_BACKGROUND_COLOR
    if option.thick_border_color is None:
        option.thick_border_color = DEFAULT_THICK_BORDER_COLOR
    if option.thin_border_color is None:
        option.thin_border_color = DEFAULT_THIN_BORDER_COLOR
    if option.thick_border_px is None or option.thick_border_px == 0:
        option.thick_border_px = DEFAULT_THICK_BORDER_PX
    if option.thin_border_px is None or option.thin_border_px == 0:
        option.thin_border_px = DEFAULT_THIN_BORDER_PX
    if option.margin_px is None or option.margin_px == 0:
        option.margin_px = DEFAULT_MARGIN_PX
    if option.service_name_font_size is None or option.service_name_font_size == 0:
        option.service_name_font_size = DEFAULT_SERVICE_NAME_FONT_SIZE

def create_image(senryu: Senryu, option: SenryuImageOption) -> Image.Image:
    complete_senryu_image_option(option)

    img = img_proc.new_image(option.senryu_width, option.senryu_height, option.background_color)

    try:
        img_proc.add_vertical_top_align_label(
            img,
            option.first_sentence_left_x,
            senryu.first_sentence,
            option.font_path,
            option.font_size,
            option.font_color,
            option.margin_px
        )

        img_proc.add_vertical_center_align_label(
            img,
            option.second_sentence_left_x,
            senryu.second_sentence,
            option.font_path,
            option.font_size,
            option.font_color,
            option.margin_px
        )

        img_proc.add_vertical_bottom_align_label(
            img,
            option.third_sentence_left_x,
            senryu.third_sentence,
            option.font_path,
            option.font_size,
            option.font_color,
            option.margin_px
        )

        img_proc.add_vertical_bottom_align_label(
            img,
            option.author_name_left_x,
            senryu.author_name,
            option.font_path,
            option.author_name_font_size,
            option.font_color,
            option.margin_px
        )

        img_proc.rect(
            img,
            0,
            0,
            option.senryu_width - 1,
            option.senryu_height - 1,
            option.thick_border_px,
            option.thick_border_color
        )

        border_thickness_diff = option.thick_border_px - option.thin_border_px

        img_proc.rect(
            img,
            border_thickness_diff,
            border_thickness_diff,
            option.senryu_width - border_thickness_diff - 1,
            option.senryu_height - border_thickness_diff - 1,
            option.thin_border_px,
            option.thin_border_color
        )

        if option.service_name:
            img_proc.add_horizontal_label(
                img,
                option.thick_border_px,
                option.senryu_height - option.thin_border_px,
                option.service_name,
                option.font_path,
                option.service_name_font_size,
                (255, 255, 255, 255)
            )

    except Exception as e:
        print(f"Error creating image: {e}")
        raise e

    return img
