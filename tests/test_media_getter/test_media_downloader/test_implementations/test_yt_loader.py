import unittest

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from yt_loader import YTLoader


mock_link = 'mockURL.com'
mock_path = 'some/path/to/save/the/file'

mock_youtube_dl = MagicMock()

test_yt_loader = YTLoader()


class TestYTLoader(TestCase):

    @patch('yt_loader.YoutubeDL.download', mock_youtube_dl)
    def test_download_media(test):
        test_yt_loader.download_media(mock_path, mock_link)

        mock_youtube_dl.assert_called_with(
                [mock_link]
        )
        

        


