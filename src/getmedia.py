"""Download and maintain media from Youtube, Twitter, Instagram."""


import os
import shutil
import re
import instaloader
import src.utils.constants as cnst
from abc import ABCMeta
from collections import defaultdict
from multiprocessing import Pool
from instaloader import Post
from youtube_dl import YoutubeDL
from src.utils.file_handler import FileHandler

fh = FileHandler()

class Media(metaclass=ABCMeta):
    """An abstract class to acquire and maintain media from internet."""

    def __init__(self):
        """Construct method."""
        super().__init__()

        self.insta_pattern = re.compile(
            cnst.INSTA_PATTERN
        )

        self.insta_shortcode_pattern = re.compile(
            cnst.INSTA_SHORTCODE_PATTERN
        )

    def download_insta(self, save_path, url):
        """Download Instagram media from given URL and save to given Path."""
        insta_shortcode = self.insta_shortcode_pattern.search(url).group(1) ##
        save_path = fh.dir_create(save_path)

        instance = instaloader.Instaloader(
            download_video_thumbnails=False,
            compress_json=False,
            save_metadata=False,
            post_metadata_txt_pattern='',
            dirname_pattern=save_path
        )

        post = Post.from_shortcode(instance.context, insta_shortcode)
        instance.download_post(post, target='')

    def download_youtube(self, save_path, url):
        """Download Youtube and Twitter media from URL and save it to Path."""
        save_path = fh.dir_create(save_path)
        options_youtube = {
            'format': 'best',
            'outtmpl': save_path + '/' + '%(title)s.mp4',
            'noplaylist': True,
            'extract-audio': True,
        }

        with YoutubeDL(options_youtube) as ydl:
            ydl.download([url])

    def process_media(self, youtube_path, instagram_path, *url):
        """Input URLs to respected methods and save them in given paths."""
        list_of_urls = list({*url})  # Avoid repetitions
        instagram_bundle = []
        youtube_bundle = []

        # Assign each URL to its respective method
        for url in list_of_urls:
            if self.insta_pattern.search(url):
                instagram_bundle.append([instagram_path, url])
            else:
                youtube_bundle.append([youtube_path, url])

        # If there is only one URL, do not initiate Pool for YT
        if len(youtube_bundle) > 1:
            with Pool() as pool:
                pool.starmap(self.download_youtube, youtube_bundle)

        elif len(youtube_bundle) == 1:
            self.download_youtube(youtube_bundle[0][0], youtube_bundle[0][1])  ## @# TODO:

        # If there is only one URL, do not initiate Pool for IG
        if len(instagram_bundle) > 1:
            with Pool() as pool:
                pool.starmap(self.download_insta, instagram_bundle)
        elif len(instagram_bundle) == 1:
            self.download_insta(instagram_bundle[0][0], instagram_bundle[0][1])


class SentMedia(Media):
    """Download and remove media inside ``with`` statement.

    Works with Youtube, Twitter and Instagram
    """

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.temp_youtube = ''
        self.temp_instagram = ''

    def __enter__(self):
        """Create YT and IG files under ``self.tempFolder`` directory."""
        self.temp_youtube = fh.dir_create(
            cnst.TEMP_YT_FOLDER
        )
        self.temp_instagram = fh.dir_create(
            cnst.TEMP_INSTA_FOLDER
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove temporary YT and IG files directory."""
        fh.delete_files_in_path(self.temp_youtube)
        fh.delete_files_in_path(self.temp_instagram)

    def send_media(self, *url):
        """Abstract class functionality to temporarily download media."""
        self.process_media(self.temp_youtube, self.temp_instagram, *url)


class SavedMedia(Media):
    """Download and maintain media."""

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.command_folders = defaultdict(str)

    def save_media(self, cmd, *url):
        """Abstract class functionality to permanently download media."""
        self.command_folders[cmd] = fh.dir_create(
            fh.get_path(
                cnst.PERM_FOLDER_NAME,
                cmd
            )
        )

        self.process_media(
            self.command_folders[cmd], self.command_folders[cmd],
            *url
        )

        return self.show_media_names(cmd)

    def show_media_names(self, cmd):
        """Get titles of media related to command."""
        if os.path.isdir(self.command_folders[cmd]):

            media_names_list = os.listdir(self.command_folders[cmd])
            return media_names_list

        return [
            'There is no media '
            'linked with the command: '
            f' {cmd}'
        ]

    def show_media(self, cmd):
        """Get absolute directory path of media related to cmd."""
        if os.path.isdir(self.command_folders[cmd]):

            show_media_list = []
            media_names = os.listdir(self.command_folders[cmd])

            show_media_list = [
                fh.get_path(
                    cnst.PERM_FOLDER_NAME,
                    cmd,
                    media_name
                ) for media_name in media_names
            ]

            return show_media_list

        return [
            'There is no media linked '
            'with the command '
            f'{cmd}'
        ]

    def delete_media(self, cmd):
        """Delete saved media related to command."""
        if os.path.isdir(self.command_folders[cmd]):
            deleted_media_list = self.show_media_names(cmd)
            shutil.rmtree(self.command_folders[cmd])
            return deleted_media_list

        return [
            'There are no media linked '
            'with the command'
            f'\' {cmd} \''
        ]
