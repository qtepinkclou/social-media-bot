"""Create and verify Captcha to avoid malicoius explotation."""

import string
import random
import shutil
from captcha.image import ImageCaptcha
from utils.config import Config
from commons import Commons

cfg = Config()


class MatchError(Exception):
    """Raise this if captcha does not match the input."""


class Randomite(Commons):
    """Generate Captcha and verify safe use."""

    def __init__(self):
        """Construct."""
        super().__init__()
        temp_captcha_file = cfg.get_param('TEMP_CAPTCHA_FILE')

        self.current_captcha_string = 'None'
        self.temp_captcha = self.dir_create(temp_captcha_file)

    def delete_captcha(self):
        """Delete created captcha."""
        shutil.rmtree(self.temp_captcha)

    def generate_random_string(self, **kwargs):
        """Generate random string of characters."""
        length = kwargs.get(
            'length',
            cfg.get_param('CAPTCHA_LENGTH', var_type='int')
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
            cfg.get_param('CAPTCHA_IMAGE_NAME')
        )

        captcha_height = kwargs.get(
            'captcha_height',
            cfg.get_param('CAPTCHA_HEIGHT', var_type='int')
        )

        captcha_width = kwargs.get(
            'captcha_width',
            cfg.get_param('CAPTCHA_WIDTH', var_type='int')
        )

        captcha_font_sizes = kwargs.get(
            'captcha_font_sizes',
            cfg.get_param('CAPTCHA_FONT_SIZES', var_type='Lint')
        )

        image = ImageCaptcha(
            width=captcha_width,
            height=captcha_height,
            font_sizes=captcha_font_sizes
        )
        path = self.temp_captcha + '/' + captcha_image_name
        image.write(text, path)
        return path

    def validate_captcha(self, response):
        """Validate if input string is randomly generated text."""
        bool_result = (response == self.current_captcha_string)
        if bool_result is False:
            raise MatchError
        return bool_result
