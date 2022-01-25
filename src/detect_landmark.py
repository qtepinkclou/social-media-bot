"""Detect landmarks in images with using the power of Google Vision API.

# Requirements:

- You need to have your own Google Cloud account
    which should be authenticated as a service account.
    For more information refer to
    [link.](https://cloud.google.com/docs/authentication/production#windows)

**detect_landmark** taken and modified from
    [link.](https://github.com/googleapis/python-vision/blob/HEAD/samples/snippets/detect/detect.py)

**save_image** taken and modified from
    [link.](https://www.youtube.com/watch?v=pgmUBOV3IIs&ab_channel=LazyTech)

# Goal:

- Add another feature to functional-discord-bot

- Merge with similar features to form a class (later...)

- In the future train your own learning algorithm
    for landmark detection as well as other detection
    algorithms and use this file as a quickstart
    to utilize them in discord.

"""

import os
import shutil
import uuid
import re
import io
import requests
from google.cloud import vision

IS_DISCORDAPP_PATTERN = re.compile(r'discordapp\.com')
TEMP_GOOGLE_LENS_FILE = 'Temporary/GoogleLens'


class Landmarks():
    """API to use Google Lens."""

    def __init__(self):
        """Construct."""
        self.cwd = re.sub(
            '\\\\',  # pattern
            '/',     # replace
            os.getcwd()  # string
        )
        self.current_image_dir = 'None'
        self.temp_google_lens = self.dir_create(TEMP_GOOGLE_LENS_FILE)

    def __enter__(self):
        """Enter function."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit function."""
        shutil.rmtree(self.temp_google_lens)

    def get_image(self, image_url):
        """Save image sent from discord."""
        if IS_DISCORDAPP_PATTERN.search(image_url):
            req = requests.get(image_url, stream=True)
            self.current_image_dir = self.temp_google_lens + \
                '/' + str(uuid.uuid4()) + '.jpg'
            with open(self.current_image_dir, 'wb') as out_file:
                print('Saving image:' + self.current_image_dir)
                shutil.copyfileobj(req.raw, out_file)

        return self.current_image_dir

    def detect_landmarks(self):
        """Detect landmarks in the file."""
        client = vision.ImageAnnotatorClient()

        with io.open(self.current_image_dir, 'rb') as image_file:
            content = image_file.read()

            image = vision.Image(content=content)

            response = client.landmark_detection(image=image)
            landmarks = response.landmark_annotations
            landmark_names_list = []

            for landmark in landmarks:
                landmark_names_list.append(landmark.description)

            if response.error.message:
                raise Exception(
                    f'{response.error.message}'
                    '\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'
                )

            return set(landmark_names_list)

    def main_process(self, image_url):
        """Do the thing."""
        self.current_image_dir = self.get_image(image_url)
        predict_set = self.detect_landmarks()

        return predict_set

    def dir_create(self, folder_name):
        """Check if directory exist, create it if it does not."""
        path = self.cwd + '/' + folder_name

        if os.path.isdir(path) is False:
            os.makedirs(folder_name)
        return path
