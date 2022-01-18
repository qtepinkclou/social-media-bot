"""Create and verify Captcha to avoid malicoius explotation."""

from captcha.image import ImageCaptcha
import string
import random
import os
import re
import shutil

CAPTCHA_LENGTH = 5  # number of characters in the string.
CAPTCHA_HEIGHT = 200
CAPTCHA_WIDTH = 320
TEMP_CAPTCHA_FILE = 'Temporary/_Captcha'
CAPTCHA_IMAGE_NAME = 'CAPTCHA.png'

# You need .ttf files in the below directory.
PERM_FONT_TYPES_FOLDER = 'Permanent/_Captcha/fonts'


class MatchError(Exception):
    """Raise this if captcha does not match the input."""

    pass


class Randomite():
    """Generate Captcha and verify safe use."""

    def __init__(self):
        """Construct."""
        self.CWD = re.sub(
                      '\\\\',  # pattern
                      '/',     # replace
                      os.getcwd()  # string
                      )
        self.tempCaptcha = self.checkDirElseCreate(TEMP_CAPTCHA_FILE)
        self.permFonts = self.checkDirElseCreate(PERM_FONT_TYPES_FOLDER)
        self.captchaImagePath = self.tempCaptcha + '/' + CAPTCHA_IMAGE_NAME

    def delete_captcha(self):
        """Delete created captcha."""
        shutil.rmtree(self.tempCaptcha)

    def generate_random_string(self, length=None):
        """Generate random string of characters."""
        self.captchaString = ''.join(random.choices(
                                    string.ascii_lowercase
                                    + string.digits,
                                    k=CAPTCHA_LENGTH
                                               )
                                     )
        return self.captchaString

    def create_captcha_image(self, string, fonts_dir=None):
        """Create captcha given string."""
        fonts_dir = fonts_dir if fonts_dir else None

        try:
            eachFont = [fonts_dir + '/' + fontName
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
                                 fonts=eachFont,
                                 font_sizes=[100 for i in eachFont]
                                 )

        finally:
            image.write(string, self.captchaImagePath)
            return self.captchaImagePath

    def validate_captcha(self, input):
        """Validate if input string is randomly generated text."""
        boolResult = (input == self.captchaString)
        if boolResult is False:
            raise MatchError
        else:
            return boolResult

    def checkDirElseCreate(self, folderName):  # This is becoming too common!
        """Check if directory exist, create it if it does not."""
        path = self.CWD + '/' + folderName

        if os.path.isdir(path) is False:
            os.makedirs(folderName)
        return path
