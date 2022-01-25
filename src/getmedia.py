"""Download and maintain media from Youtube, Twitter, Instagram."""


import os
import shutil
import re
from abc import ABCMeta
from multiprocessing import Pool
import instaloader
from instaloader import Post
from youtube_dl import YoutubeDL


# Constant variables
IS_INSTA_PATTERN = re.compile(r'instagram\.com/p/')
INSTA_SHORTCODE_PATTERN = re.compile(r'/p/(.+)/')
TEMP_FILE_NAME = 'Temporary'
TEMP_YT_NAME = 'Temporary/youtube'
TEMP_INSTA_NAME = 'Temporary/instagram'
PERM_FILE_NAME = 'Permanent'


class Media(metaclass=ABCMeta):
    """An abstract Base class to acquire and maintain media from internet."""

    def __init__(self):
        """Construct method."""
        self.cwd = re.sub(  # current working directory
            '\\\\',  # pattern
            '/',     # replace
            os.getcwd()  # string
        )

    def download_insta(self, save_folder, url):
        """Download Instagram media from given URL and save to given Path."""
        insta_shortcode = INSTA_SHORTCODE_PATTERN.search(url).group(1)
        path = self.cwd + '/' + save_folder

        instance = instaloader.Instaloader(
            download_video_thumbnails=False,
            compress_json=False,
            save_metadata=False,
            post_metadata_txt_pattern='',
            dirname_pattern=path
        )

        post = Post.from_shortcode(instance.context, insta_shortcode)
        instance.download_post(post, target='')

    def download_youtube(self, save_folder, url):
        """Download Youtube and Twitter media from URL and save it to Path."""
        path = self.cwd + '/' + save_folder
        options_youtube = {
            'format': 'best',
            'outtmpl': path + '.mp4',
            'noplaylist': True,
            'extract-audio': True,
        }

        with YoutubeDL(options_youtube) as ydl:
            ydl.download([url])

    def process_media(self, youtube_folder, instagram_folder, *url):
        """Input URLs to respected methods and save them in given paths."""
        list_of_urls = list({*url})  # Avoid repetitions
        instagram_bundle = []
        youtube_bundle = []

        # Assign each URL to its respective method
        for url in list_of_urls:
            if IS_INSTA_PATTERN.search(url):
                instagram_bundle.append([instagram_folder, url])
            else:
                youtube_bundle.append([youtube_folder, url])

        # If there is only one URL, do not initiate Pool for YT
        if len(youtube_bundle) > 1:
            with Pool() as pool:
                pool.starmap(self.download_youtube, youtube_bundle)

        elif len(youtube_bundle) == 1:
            self.download_youtube(youtube_bundle[0][0], youtube_bundle[0][1])

        # If there is only one URL, do not initiate Pool for IG
        if len(instagram_bundle) > 1:
            with Pool() as pool:
                pool.starmap(self.download_insta, instagram_bundle)
        elif len(instagram_bundle) == 1:
            self.download_insta(instagram_bundle[0][0], instagram_bundle[0][1])

    def dir_create(self, folder_name):
        """Check if directory exist, create it if it does not."""
        path = self.cwd + '/' + folder_name

        if os.path.isdir(path) is False:
            os.makedirs(folder_name)
        return path


class SentMedia(Media):
    """Download and remove media inside ``with`` statement.

    Works with Youtube, Twitter and Instagram
    """

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.temp_folder_name = TEMP_FILE_NAME
        self.temp_youtube = TEMP_YT_NAME
        self.temp_instagram = TEMP_INSTA_NAME

    def __enter__(self):
        """Create YT and IG files under ``self.tempFolder`` directory."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove YT and IG files under ``self.tempFolder`` directory."""
        shutil.rmtree(self.temp_youtube)
        shutil.rmtree(self.temp_instagram)

    def send_media(self, *url):
        """Abstract class functionality to temporarily download media."""
        self.process_media(self.temp_youtube, self.temp_instagram, *url)


class SavedMedia(Media):
    """Download and maintain media."""

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.perm_folder = PERM_FILE_NAME

    def save_media(self, cmd, *url):
        """Abstract class functionality to permanently download media."""
        command_folder = self.get_command_path(cmd)
        self.process_media(command_folder, command_folder, *url)

        return self.show_media_names(cmd)

    def show_media_names(self, cmd):
        """Get titles of media related to command."""
        command_folder = self.get_command_path(cmd)

        if os.path.isdir(command_folder):

            media_names_list = os.listdir(command_folder)
            return media_names_list

        return [
            'There is no media '
            'linked with the command: '
            f' {cmd}'
        ]

    def show_media(self, cmd):
        """Get absolute directory path of media related to cmd."""
        command_folder = self.get_command_path(cmd)

        if os.path.isdir(command_folder):

            show_media_list = []
            names = os.listdir(command_folder)

            for index in enumerate(names):
                show_media_list.append(
                    command_folder
                    + '/'
                    + names[index[0]]
                )

            return show_media_list

        return [
            'There is no media linked '
            'with the command '
            f'{cmd}'
        ]

    def delete_media(self, cmd):
        """Delete saved media related to command."""
        command_folder = self.get_command_path(cmd)

        if os.path.isdir(command_folder):
            deleted_media_list = self.show_media_names(cmd)
            shutil.rmtree(command_folder)
            return deleted_media_list

        return [
            'There are no media linked '
            'with the command'
            f'\' {cmd} \''
        ]

    def get_command_path(self, cmd):
        """Get the path of command folder."""
        command_folder = self.perm_folder + '/' + cmd
        return command_folder
