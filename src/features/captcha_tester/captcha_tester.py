import string
import random

from ...commons.file_handler import FileHandler

from captcha.image import ImageCaptcha


tmp_captcha_folder_name = 'Tmp/Captcha'

waiting_period = 20.0 
captcha_entrance_msg = f"""Pass the Captcha Test before the command can be executed.
 You have {waiting_period} seconds to submit."""
captcha_match_msg = """You have now passed the Captcha Test fellow human!
Wait for me while I execute the task you really wanted in the first place."""
captcha_fail_msg = """You failed the Captcha Test, you may try again."""


class CaptchaMatchError(Exception):
    """Raise this if captcha does not match with the input"""


class CaptchaTester:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CaptchaTester, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.file_handler = FileHandler()
        self.tmp_captcha_folder = self.file_handler.dir_create(
            tmp_captcha_folder_name
        )
        self.image = ImageCaptcha(
            width=320,
            height=200,
            font_sizes=[100, ]
        )

    def _generate_random_string(self):
        self.current_captcha_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=5
        )
        )

    def _create_captcha_image(self):
        self.current_captcha_image_path = self.file_handler.get_path(
            self.tmp_captcha_folder,
            'CAPTCHA.png'
        )
        self.image.write(
            self.current_captcha_string,
            self.current_captcha_image_path
        )

    async def _send_captcha_image(self, app_object, **kwargs):
        await app_object.send_to_user(
            content=captcha_entrance_msg,
            content_type='text',
            **kwargs)
        await app_object.send_to_user(
            content=self.current_captcha_image_path,
            content_type='media',
            **kwargs
        )

    async def _validate_captcha(self, app_object, **kwargs):
        response = await app_object.receive_from_user(
            content_type='text',
            wait_for=waiting_period,
            **kwargs
        )

        bool_result = (response == self.current_captcha_string)
        if bool_result is False:
            await app_object.send_to_user(
                content=captcha_fail_msg,
                content_type='text',
                **kwargs
            )
            raise CaptchaMatchError
        await app_object.send_to_user(
            content=captcha_match_msg,
            content_type='text',
            **kwargs
        )

    async def main_process(self, app_object, **kwargs):
        self._generate_random_string()
        self._create_captcha_image()
        await self._send_captcha_image(app_object, **kwargs)
        await self._validate_captcha(app_object, **kwargs)
        self.file_handler.delete_files_in_path(
            self.tmp_captcha_folder
        )
