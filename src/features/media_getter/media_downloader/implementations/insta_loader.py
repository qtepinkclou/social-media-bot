import re

from .. import regexen

import instaloader

from instaloader import Instaloader
from instaloader import Post


instaloader_configuration = {
    'download_video_thumbnails': False,
    'compress_json': False,
    'save_metadata': False,
    'post_metadata_txt_pattern': ''
}


class InstaLoader:

    def __init__(self):
        self.insta_loader = Instaloader(instaloader_configuration)
        self.insta_shortcode_pattern = re.compile(regexen.REGEX_FOR_INSTA_URL)

    def _extract_shortcode(self, url):
        insta_post_shortcode_search = self.insta_shortcode_pattern.search(url)

        if insta_post_shortcode_search:
            return insta_post_shortcode_search[1]

        return ''

    def download_media(self, save_path, url):
        insta_shortcode = self._extract_shortcode(url)

        if insta_shortcode:
            self.insta_loader['dirname_pattern'] = save_path
            post = Post.from_shortcode(
                self.insta_loader.context,
                insta_shortcode
            )
            self.insta_loader.download_post(post, target='')
