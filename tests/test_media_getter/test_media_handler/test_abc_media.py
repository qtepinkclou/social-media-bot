import unittest

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from abc_media import ABCMediaHandler


mock_path = 'some/path/to/save/media'

mock_url_1 = 'various.com'
mock_url_2 = 'media_containing.com'
mock_url_3 = 'websites.com'

mock_download_manager = MagicMock()

test_abc_media_handler = ABCMediaHandler()


class TestABCMediaHandler(TestCase):

    @patch('abc_media.DownloadManager.relegate_task', mock_download_manager)
    def test_process_media(self):
        test_singular_link = test_abc_media_handler._process_media(
                mock_path,
                mock_url_1
        )
        self.assertEqual(
                mock_download_manager.call_count,
                1
        )

        test_multiple_link = test_abc_media_handler._process_media(
                mock_path,
                mock_url_1,
                mock_url_2,
                mock_url_3
        )
        self.assertEqual(
                mock_download_manager.call_count,
                4
        )
