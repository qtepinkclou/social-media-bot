"""Create and verify Captcha to avoid malicoius explotation."""

import string
import random
import utils.constants as cnst
from captcha.image import ImageCaptcha
from commons import Commons


class MatchError(Exception):
    """Raise this if captcha does not match the input."""


class Randomite(Commons):
    """Generate Captcha and verify safe use."""

    def __init__(self):
        """Construct."""
        super().__init__()

        self.current_captcha_string = ''

        self.temp_captcha_folder = self.dir_create(
            cnst.TEMP_CAPTCHA_FOLDER
        )

    def delete_captcha(self):
        """Delete created captcha."""
        self.delete_files_in_path(self.temp_captcha_folder)

    def generate_random_string(self, **kwargs):
        """Generate random string of characters."""
        length = kwargs.get(
            'length',
            cnst.CAPTCHA_LENGTH
        )

        self.current_captcha_string = ''.join(random.choices(
            string.ascii_lowercase
            + string.digits,
            k=length
        )
        )

        return self.current_captcha_string

    def create_captcha_image(self, text, **kwargs):
        """Create captcha given string."""
        captcha_image_name = kwargs.get(
            'captcha_image_name',
            cnst.CAPTCHA_IMAGE_NAME
        )

        captcha_height = kwargs.get(
            'captcha_height',
            cnst.CAPTCHA_HEIGHT
        )

        captcha_width = kwargs.get(
            'captcha_width',
            cnst.CAPTCHA_WIDTH
        )

        captcha_font_sizes = kwargs.get(
            'captcha_font_sizes',
            cnst.CAPTCHA_FONT_SIZES
        )

        image = ImageCaptcha(
            width=captcha_width,
            height=captcha_height,
            font_sizes=captcha_font_sizes
        )
        file_path = self.get_path(
            cnst.TEMP_CAPTCHA_FOLDER,
            captcha_image_name
        )
        image.write(text, file_path)
        return file_path

    def validate_captcha(self, response):
        """Validate if input string is randomly generated text."""
        bool_result = (response == self.current_captcha_string)
        if bool_result is False:
            raise MatchError
        return bool_result
