import shutil
import uuid
import io
import requests

from ...commons.file_handler import FileHandler

from google.cloud import vision
from google.oauth2 import service_account


#  REGEX_FOR_DISCORD_IMAGE = r"media\.discordapp\.net/attachments/.{37}/"

not_image_url_msg = 'This link does not belong to an image'

google_came_up_empty_msg = 'Google could not hack it!'

tmp_google_lens = 'Tmp/GoogleLens'

image_formats = ('image/jpg', 'image/jpeg', 'image/png')


def connect_google_vision_w_credentials():
    credentials = service_account.Credentials.from_service_account_file(
        'src/features/landmark_detector/user_credentials.json'
    )
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client


def is_url_image(image_url):
    r = requests.head(image_url)
    if r.headers['content-type'] in image_formats:
        return True
    return False


class IncompatibleLinkError(Exception):
    """Raise this if given link is not of discord image"""


class LandmarkDetector:

    def __init__(self):
        self.file_handler = FileHandler()
        self.tmp_google_lens = self.file_handler.dir_create(
            tmp_google_lens
        )
        self.client = connect_google_vision_w_credentials()


    async def _get_image_from_app(self, app_object, **kwargs):
        image_url = await app_object.receive_from_user(
            content_type='single_media',
            **kwargs
        )
        if is_url_image(image_url):
            req = requests.get(image_url, stream=True)

            self.current_image_dir = self.tmp_google_lens \
                + '/' \
                + str(uuid.uuid4()) \
                + '.jpg'

            with open(
                self.current_image_dir,
                'wb'
            ) as out_file:
                shutil.copyfileobj(req.raw, out_file)

        else:
            await app_object.send_to_user(
                content=not_image_url_msg,
                content_type='text',
                **kwargs
            )
            raise IncompatibleLinkError

    async def _detect_landmark(self, app_object, **kwargs):
        with io.open(
            self.current_image_dir,
            'rb'
        ) as image_file:
            content = image_file.read()
            image = vision.Image(content=content)
            response = self.client.landmark_detection(image=image)

            landmarks = response.landmark_annotations
            landmark_names_list = []

            for landmark in landmarks:
                landmark_names_list.append(landmark.description)

            if landmark_names_list:
                output = ['Google Lens supposes this image belongs to:'] \
                    + list(dict.fromkeys(landmark_names_list))  # avoid repetitions
            else:
                output = [google_came_up_empty_msg]
                if response.error.message:
                    output.append(f'''An error occured with code:
                        {response.error.code} and message:
                        {response.error.message}''')

            for line in output:
                await app_object.send_to_user(
                    content=line,
                    content_type='text',
                    **kwargs
                )

    async def main_process(self, app_object, **kwargs):
        await self._get_image_from_app(app_object, **kwargs)
        await self._detect_landmark(app_object, **kwargs)
        self.file_handler.delete_files_in_path(
            self.tmp_google_lens
        )

