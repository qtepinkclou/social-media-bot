import unittest

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from landmark_detector import LandmarkDetector
from landmark_detector import IncompatibleLinkError

valid_discord_image_link = 'https://media.discordapp.net/attachments/920793483629977681/964681989447884810/peruz.jpg'
invalid_discord_image_link = 'just_some_website.com'

mock_requests = MagicMock()
mock_shutil = MagicMock()
mock_uuid = MagicMock()
mock_connection = MagicMock()
mock_open = MagicMock()


class TestLandmarkDetector(TestCase):

    @patch('landmark_detector.connect_google_vision', mock_connection)
    def setUp(self):
        self.test_landmark_detector = LandmarkDetector()


    @patch('landmark_detector.requests.get', mock_requests)
    @patch('landmark_detector.shutil', mock_shutil)
    @patch('landmark_detector.uuid.uuid4', mock_uuid)
    @patch('landmark_detector.open', mock_open)
    def test_get_discord_image(self):
        self.test_landmark_detector._get_discord_image(
            valid_discord_image_link
        )

        mock_requests.assert_called_with(
            valid_discord_image_link,
            stream=True
        )

        with self.assertRaises(IncompatibleLinkError):
            self.test_landmark_detector._get_discord_image(
                invalid_discord_image_link
            )
