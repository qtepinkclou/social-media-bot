import unittest

from unittest import TestCase

from download_manager import DownloadManager
from yt_loader import YTLoader
from insta_loader import InstaLoader


test_yt_link = 'https://www.youtube.com/watch?v=b3sOOBicyDY&list=PL_Qp9H9s6UZX6pcheo-EtdsYXnuOQzNVb&index=3&ab_channel=ThriftyVideoNetwork'
test_insta_link = 'https://www.instagram.com/p/CdpRx6ZtAiR/'
test_any_other_link = 'https://twitter.com/nikgeneburn/status/1522884280262737920'

test_path = 'some/path/to/save/the/file'

test_download_manager = DownloadManager()


class TestDownloadManager(TestCase):


    def test_relegate_task(self):
        test_yt = test_download_manager.relegate_task(test_yt_link)
        test_insta = test_download_manager.relegate_task(test_insta_link)
        test_any_other = test_download_manager.relegate_task(test_any_other_link)

        self.assertIsInstance(
            test_yt,
            YTLoader
        )
        self.assertIsInstance(
            test_insta,
            InstaLoader
        )
        self.assertIsInstance(
            test_any_other,
            YTLoader
        )






        
