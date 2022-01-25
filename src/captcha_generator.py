"""Create and verify Captcha to avoid malicoius explotation."""

import string
import random
import os
import re
import shutil
from captcha.image import ImageCaptcha

CAPTCHA_LENGTH = 5  # number of characters in the string.
CAPTCHA_HEIGHT = 200
CAPTCHA_WIDTH = 320
TEMP_CAPTCHA_FILE = 'Temporary/_Captcha'
CAPTCHA_IMAGE_NAME = 'CAPTCHA.png'

# You need .ttf files in the below directory.
PERM_FONT_TYPES_FOLDER = 'Permanent/_Captcha/fonts'


class MatchError(Exception):
    """Raise this if captcha does not match the input."""


class Randomite():
    """Generate Captcha and verify safe use."""

    def __init__(self):
        """Construct."""
        self.cwd = re.sub(
            '\\\\',  # pattern
            '/',     # replace
            os.getcwd()  # string
        )
        self.current_captcha_string = 'None'
        self.temp_captcha = self.dir_create(TEMP_CAPTCHA_FILE)
        self.perm_fonts = self.dir_create(PERM_FONT_TYPES_FOLDER)
        self.captcha_image_path = self.temp_captcha + '/' + CAPTCHA_IMAGE_NAME

    def delete_captcha(self):
        """Delete created captcha."""
        shutil.rmtree(self.temp_captcha)

    def generate_random_string(self, length=CAPTCHA_LENGTH):
        """Generate random string of characters."""
        self.current_captcha_string = ''.join(random.choices(
            string.ascii_lowercase
            + string.digits,
            k=length
        )
        )
        return self.current_captcha_string

    def create_captcha_image(self, text, fonts_dir=None):
        """Create captcha given string."""
        fonts_dir = fonts_dir if fonts_dir else None

        try:
            each_font = [fonts_dir + '/' + fontName
                         for fontName in
                         os.listdir(fonts_dir)
                         ]

        except TypeError:
            print("No .ttf files found.")
            image = ImageCaptcha(
                width=CAPTCHA_WIDTH,
                height=CAPTCHA_HEIGHT,
                font_sizes=[100]
            )
        else:
            image = ImageCaptcha(
                width=CAPTCHA_WIDTH,
                height=CAPTCHA_HEIGHT,
                fonts=each_font,
                font_sizes=[100 for i in each_font]
            )

        finally:
            image.write(text, self.captcha_image_path)
        return self.captcha_image_path

    def validate_captcha(self, response):
        """Validate if input string is randomly generated text."""
        bool_result = (response == self.current_captcha_string)
        if bool_result is False:
            raise MatchError
        return bool_result

    def dir_create(self, folder_name):  # This is becoming too common!
        """Check if directory exist, create it if it does not."""
        path = self.cwd + '/' + folder_name

        if os.path.isdir(path) is False:
            os.makedirs(folder_name)
        return path
