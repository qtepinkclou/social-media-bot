import unittest

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from insta_loader import InstaLoader


mock_path = 'some/path/to/save/the/file'
mock_link = 'mockURL.com'

mock_instaloader = MagicMock()
mock_extract_shortcode = MagicMock()
mock_post = MagicMock()
mock_download = MagicMock()

test_insta_post_link = 'https://www.instagram.com/p/Cb5WT-Uhj6Z/'
test_insta_post_link_shortcode = 'Cb5WT-Uhj6Z'

test_insta_loader = InstaLoader()


class TestInstaLoader(TestCase):

    def test_extract_shortcode(self):
        test_shortcode = test_insta_loader._extract_shortcode(
                test_insta_post_link
        )
        self.assertEqual(
                test_shortcode,
                test_insta_post_link_shortcode
        )

    @patch('insta_loader.instaloader.Instaloader.download_post', mock_download)
    @patch('insta_loader.instaloader.Post.from_shortcode', mock_post)
    @patch('insta_loader.InstaLoader._extract_shortcode', mock_extract_shortcode)
    def test_download_media(self):
        result = test_insta_loader.download_media(
                mock_path,
                mock_link
        )

        mock_download.assert_called_with(
                mock_post(),
                target=mock_path
        ) # this might need *further* tuning


            

        


