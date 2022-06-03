import re

from . import regexen

from .implementations.yt_loader import YTLoader
from .implementations.insta_loader import InstaLoader


class DownloadManager:

    def __init__(self):
        self.yt_loader = YTLoader()
        self.insta_loader = InstaLoader()
        self.insta_pattern = re.compile(regexen.REGEX_FOR_INSTA_URL)
        self.yt_pattern = re.compile(regexen.REGEX_FOR_YT_URL)

    def relegate_task(self, url):

        if self.insta_pattern.match(url):
            return self.insta_loader
        elif self.yt_pattern.match(url):
            return self.yt_loader
        else:
            return self.yt_loader
