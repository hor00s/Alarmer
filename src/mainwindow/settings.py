import os
import re
import json
import shutil
from typing import Any, Callable
from colormap import hex2rgb

from mainwindow.actions import _pop_up_lbl, pop_up
from .constants import (
    CONFIG_FILE,
    SOUND,
    BG,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog


def get_config_attribute(attr: str, file: str=CONFIG_FILE) -> Any:
    """Get a certain attribute from the config file

    :param str attr: The attribute to be pulled
    :param str file: The location of the config file
    :return Any:
    """    
    with open(file, mode='r') as f:
        data = json.load(f)
    return data[attr]


def set_configuration(config: str, new_value: str, file: str=CONFIG_FILE):
    """Change a configuration in ../.config.json

    :param str config: The key of the configuration
    :param str new_value: The new value
    :param str file: The location of the config file
    """    
    with open(file, mode='r') as f:
        data = json.load(f)
    
    data[config] = new_value

    with open(file, mode='w') as f:
        json.dump(data, f, indent=4)


def set_background(bg_lbl, size: tuple, fixed_size: bool):
    """Set a new background for the ui

    :param QLabel bg_lbl: Background tab's label
    :param tuple size: Size of the window
    :param bool fixed_size: Scale the image to the size of the window
    """    
    pixmap = QPixmap(BG)
    if fixed_size:
        w, h = size
        pixmap = QPixmap(BG).scaledToHeight(h).scaledToWidth(w)
    bg_lbl.setPixmap(pixmap)


def _replace_background(path: str, new_bg_name, extension):
    shutil.copy(path, 'components')
    os.remove(os.path.join(BG))
    os.rename(os.path.join('components', new_bg_name), os.path.join('components', f'bg.{extension}'))

def change_background(self, ask_dialog: Callable, pop_up: Callable, pop_up_lbl):
    """Opens a file dilog, user picks an image and this function
    moves the image in the /components and changes it's name to -> bg.<extension>

    :param Callable ask_dialog: PyQt's filedialog
    :param Callable ask_dialog: PyQt's filedialog
    :param Callable pop_up: Pop up function
    :param QLabel pop_lbl: Pop up label
    """    
    img = QFileDialog.getOpenFileName(self, "Open file", "", "Jpeg (*.jpg);;Png (*.png)")
    path, _ = img
    new_bg_name = path.split(os.sep)[-1]
    extension = new_bg_name[-3:]
    if path:
        ask_dialog("Scale image", "Would you like to the image to be scaled?", "By clicking `yes` the image that you selected\
            will be scaled up/down to the size of the window, otherwise it will preserve it's original size. It is recommended\
            that if the image is too big to click `yes`")
        _replace_background(path, new_bg_name, extension)
        pop_up(pop_up_lbl, "Backgound has been changed!")


def _replace_sound(path: str):
    os.remove(SOUND)
    shutil.copy(path, 'components')

def change_alarm_sound(self, pop_up: Callable, pop_up_lbl):
    """Opens a file dilog, user picks a sound and this function
    replaces the old sound with the new one in the /components
    :param Callable pop_up: Pop up function
    :param QLabel pop_lbl: Pop up label
    """   
    path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Mp3 (*.mp3)")
    if path:
        _replace_sound(path)
        pop_up(pop_up_lbl, "Alarm sound has been changed!")


def _validate_hex(hex_value: str):
    pattern = '^#+([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'
    return re.match(pattern, hex_value)


def _validate_rgb(rgb: list):
    return all(list(map(lambda i: 0 <= int(i) <= 255, rgb)))


def _validate_padding(padding: int):
    return int(padding)


def get_color(color_value: str, pop_up: Callable, pop_lbl, file: str=CONFIG_FILE):
    """Validates a color value and writes it in the the .config file

    :param str color_value: A value as HEX or RGB
    :param Callable pop_up: Pop up function
    :param QLabel pop_lbl: Pop up label
    """    
    try:
        if color_value.startswith('#') and _validate_hex(color_value):
            color = list(hex2rgb(color_value))
        else:
            color = color_value.split(',')
        color = list(map(lambda i: int(i), color))
        if _validate_rgb(color):
            set_configuration('text_tab1_color', color, file)
        else:
            pop_up(pop_lbl, "RGB Values go from 0 up to 255")
    except ValueError:
        pop_up(pop_lbl, "Color could not be resolved either as `rbg` or `hex` please try again!")


def get_header(new_header: str, pop_up: Callable, pop_lbl, file: str=CONFIG_FILE):
    """Validates the new header and writes it in the .config file

    :param str new_header: New haeder
    :param Callable pop_up: Pop up function
    :param QLabel pop_up_lbl: Pop up label
    """    
    if len(new_header) <= 20:
        set_configuration('tab1_header', str(new_header), file)
        pop_up(pop_lbl, 'Header has been changed!')
    else:
        pop_up(pop_lbl, 'Header text cannot be more that 20 characters long')


def get_padding(padding: int, pop_up: Callable, pop_lbl, file: str=CONFIG_FILE):
    try:
        set_configuration('list_padding', _validate_padding(padding), file)
    except ValueError:
        pop_up(pop_lbl, "Invalid value for list padding")
