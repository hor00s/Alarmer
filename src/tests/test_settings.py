import os
import sys
import unittest
sys.path.append('.')
from mainwindow.constants import (
    DEFAULT_SOUNDS,
    DEFAULT_BG,
    TEST_CONFIG,
)
from mainwindow.settings import (
    get_config_attribute,
    set_configuration,
    _replace_background,
    _replace_sound,
    _validate_hex,
    _validate_rgb,
)


class TestSettings(unittest.TestCase):
    def test_get_config(self):
        self.assertIsInstance(get_config_attribute('text_tab1_color', TEST_CONFIG), list)

    def test_set_config(self):
        new_color = [50, 20, 255]
        set_configuration('text_tab1_color', new_color, TEST_CONFIG)
        self.assertEqual(get_config_attribute('text_tab1_color', TEST_CONFIG), new_color)

    def test_replace_sound(self):
        current_sound = os.listdir('components')
        dsound1, dsound2, *_ = os.listdir(DEFAULT_SOUNDS)
        sound1 = os.path.join(DEFAULT_SOUNDS, dsound1)
        sound2 = os.path.join(DEFAULT_SOUNDS, dsound2)
        if dsound1 in current_sound:
            _replace_sound(sound2)
        elif dsound2 in current_sound:
            _replace_sound(sound1)
        new_sound = os.listdir('components')
        self.assertFalse(current_sound == new_sound, msg='Sound failed to change')
    
    def test_validate_hex(self):
        valid = ['#008000', '#800080', '#ff0000', '#FFFFFF']
        invalid = ['#ff56r4', '#12345aa', '#OO4566', '#XF4566', '#WW4566']
        for v in valid:
            self.assertTrue(_validate_hex(v), msg='A valid hex value fails to pass')
        for i in invalid:
            self.assertFalse(_validate_hex(i), msg='An invalid hex value passes')

    def test_validate_rgb(self):
        valid = [[244, 0, 255], [255, 0, 0], [145, 100, 182], [0, 0, 255]]
        invalid = [[230, 200, 256], [256, 9, 0], [0, 256, 100]]
        for v in valid:
            self.assertTrue(_validate_rgb(v), msg='A valid rgb value fails to pass')
        for i in invalid:
            self.assertFalse(_validate_rgb(i), msg='An invalid rgb value passes')

    def _test_replace_bg(self): # TODO: How to test the bg?
        with open(os.path.join('components' 'bg.png'), mode='rb') as f:
            current_bg = f.read()

        # _replace_background()


if __name__ == '__main__':
    unittest.main()
