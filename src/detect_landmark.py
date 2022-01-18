"""Detect landmarks in images with using the power of Google Vision API.

# Requirements:

- You need to have your own Google Cloud account which should be authenticated as a service account. For more information refer to [link.](https://cloud.google.com/docs/authentication/production#windows)

**detect_landmark** taken and modified from [link.](https://github.com/googleapis/python-vision/blob/HEAD/samples/snippets/detect/detect.py)

**save_image** taken and modified from [link.](https://www.youtube.com/watch?v=pgmUBOV3IIs&ab_channel=LazyTech)

# Goal:

- Add another feature to functional-discord-bot

- Merge with similar features to form a class (later...)

- In the future train your own learning algorithm for landmark detection as well as other detection algorithms and use this file as a quickstart to utilize them in discord.

"""

import os
import shutil
import requests
import uuid
import re

IS_DISCORDAPP_PATTERN = re.compile(r'discordapp\.com')
TEMP_GOOGLE_LENS_FILE = 'Temporary/GoogleLens'


class Landmarks():
    """API to use Google Lens."""

    def __init__(self):
        """Construct."""
        self.CWD = re.sub(
                      '\\\\',  # pattern
                      '/',     # replace
                      os.getcwd()  # string
                      )

    def __enter__(self):
        """Enter function."""
        self.tempGL = self.checkDirElseCreate(TEMP_GOOGLE_LENS_FILE)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit function."""
        shutil.rmtree(self.tempGL)

    def get_image(self, imageUrl):
        """Save image sent from discord."""
        imageDir = 'None'

        if IS_DISCORDAPP_PATTERN.search(imageUrl):
            req = requests.get(imageUrl, stream=True)
            imageDir = self.tempGL + '/' + str(uuid.uuid4()) + '.jpg'
            with open(imageDir, 'wb') as out_file:
                print('Saving image:' + imageDir)
                shutil.copyfileobj(req.raw, out_file)

        return imageDir

    def detect_landmarks(self, path):
        """Detect landmarks in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

            image = vision.Image(content=content)

            response = client.landmark_detection(image=image)
            landmarks = response.landmark_annotations
            landmarkNames = []

            for landmark in landmarks:
                landmarkNames.append(landmark.description)

            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
            return set(landmarkNames)

    def main_process(self, imageUrl):
        """Do the thing."""
        imageDir = self.get_image(imageUrl)
        predictSet = self.detect_landmarks(imageDir)

        return predictSet

    def checkDirElseCreate(self, folderName):
        """Check if directory exist, create it if it does not."""
        path = self.CWD + '/' + folderName

        if os.path.isdir(path) is False:
            os.makedirs(folderName)
        return path
