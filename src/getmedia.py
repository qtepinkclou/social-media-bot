"""Download and maintain media from Youtube, Twitter, Instagram."""


import sys
import os
import shutil
import re
from abc import ABCMeta
import instaloader
from instaloader import Post
from youtube_dl import YoutubeDL
from multiprocessing import Pool

# Constant variables
IS_INSTA_PATTERN = re.compile(r'instagram\.com/p/')
INSTA_SHORTCODE_PATTERN = re.compile(r'/p/(.+)/')


def blockPrint():
    """Toggle block all print statements in script."""
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    """Toggle enable all print statements in script."""
    sys.stdout = sys.__stdout__


class Media(metaclass=ABCMeta):
    """An abstract Base class to acquire and maintain media from internet.

    :param CWD: Current working directory path
    :type CWD: string
    """

    def __init__(self):
        """Construct method."""
        self.CWD = re.sub(
                      '\\\\',  # pattern
                      '/',     # replace
                      os.getcwd()  # string
                      )

    def dlIG(self, path, url):
        """Download Instagram media from given URL and save to given Path.

        :param path: Path for the file to be saved
        :type path: string
        :param url: URL of the media to be downloaded
        :type url: string
        """
        shortCode = INSTA_SHORTCODE_PATTERN.search(url).group(1)

        instance = instaloader.Instaloader(
                                           download_video_thumbnails=False,
                                           compress_json=False,
                                           save_metadata=False,
                                           post_metadata_txt_pattern='',
                                           dirname_pattern=path
                                            )

        post = Post.from_shortcode(instance.context, shortCode)
        instance.download_post(post, target='')

    def dlYT(self, path, url):
        """Download Youtube and Twitter media from given URL and save to given Path.

        :param path: Path for the file to be saved
        :type path: string
        :param url: URL of the media to be downloaded
        :type url: string
        """
        optionsYT = {
                     'format': 'best',
                     'outtmpl': '{}/%(title)s'.format(path)+'.mp4',
                     'noplaylist': True,
                     'extract-audio': True,
                     }

        with YoutubeDL(optionsYT) as ydl:
            blockPrint()
            ydl.download([url])
            enablePrint()

    def processMedia(self, pathYT, pathIG, *url):
        r"""Input URLs to respected methods and save them in given paths.

        :param pathYT: Download path of Youtube and Twitter URLs
        :type pathYT: string
        :param pathIG: Download path of Instagram URLs
        :type pathIG: string
        :param url: Variable length argument list of URLs
        :type url: List of string
        """
        listOfURLs = list({*url})  # Avoid repetitions
        IG = []
        YT = []

        # Assign each URL to its respective method
        for URL in listOfURLs:
            if IS_INSTA_PATTERN.search(URL):
                IG.append([pathIG, URL])
            else:
                YT.append([pathYT, URL])

        # If there is only one URL, do not initiate Pool for YT
        if len(YT) > 1:
            with Pool() as pool:
                pool.starmap(self.dlYT, YT)
        elif len(YT) == 1:
            self.dlYT(YT[0][0], YT[0][1])

        # If there is only one URL, do not initiate Pool for IG
        if len(IG) > 1:
            with Pool() as pool:
                pool.starmap(self.dlIG, IG)
        elif len(IG) == 1:
            self.dlIG(IG[0][0], IG[0][1])

    def checkDirElseCreate(self, folderName):
        """Check if directory exist, create it if it does not."""
        path = self.CWD + '/' + folderName

        if os.path.isdir(path) is False:
            os.makedirs(folderName)
        return path


class SentMedia(Media):
    """Download and remove media inside ``with`` statement.

    Works with Youtube, Twitter and Instagram

    :param tempFolder: Absolute path where media will be
      temporarily downloaded in OS
    :type tempFolder: string
    """

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.tempFolder = self.checkDirElseCreate('Temporary')

    def __enter__(self):
        """Create YT and IG files under ``self.tempFolder`` directory."""
        self.tempYT = self.checkDirElseCreate('Temporary/youtube')
        self.tempIG = self.checkDirElseCreate('Temporary/instagram')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove YT and IG files under ``self.tempFolder`` directory."""
        shutil.rmtree(self.tempYT)
        shutil.rmtree(self.tempIG)

    def sendMedia(self, *url):
        r"""Abstract class functionality to temporarily download media to one command.

        :param url: Variable length argument list of URLs
        :type url: List of string
        """
        self.processMedia(self.tempYT, self.tempIG, *url)


class SavedMedia(Media):
    """Download and maintain media.

    Works with Youtube, Twitter and Instagram

    :param permFolder: Absolute path where media will be downloaded in OS
    :type permFolder: string
    """

    def __init__(self):
        """Construct method."""
        super().__init__()
        self.permFolder = self.checkDirElseCreate('Permanent')

    def saveMedia(self, cmd, *url):
        r"""Abstract class functionality to permanently download media in one command.

        :param cmd: Keyword related with saved media
        :type cmd: string
        :param url: Variable length argument list of URLs
        :type url: List of string
        :return: Titles of saved media
        :rtype: List of strings
        """
        commandFolder = self.getCommandPath(cmd)
        self.processMedia(commandFolder, commandFolder, *url)

        return self.printExistingMediaNames(cmd)

    def printExistingMediaNames(self, cmd):
        """Get titles of media related to command.

        :param cmd: Keyword related with saved media
        :type cmd: string
        :return: Titles of media related to command
        :rtype: List of strings
        """
        commandFolder = self.getCommandPath(cmd)

        if os.path.isdir(commandFolder):

            mediaNamesList = os.listdir(commandFolder)
            return mediaNamesList

        return [
                'There is no media '
                'linked with the command:'
                ' \' {} \''.format(cmd)
                ]

    def showMedia(self, cmd):
        """Get absolute directory path of media related to cmd.

        :param cmd: Keyword related with saved media
        :type cmd: string
        :return: Absolute path of media related to command in OS
        :rtype: List of strings
        """
        commandFolder = self.getCommandPath(cmd)

        if os.path.isdir(commandFolder):

            showMediaList = []
            names = os.listdir(commandFolder)

            for i in range(len(names)):
                showMediaList.append(commandFolder
                                     + '/'
                                     + names[i]
                                     )

            return showMediaList

        return [
                'There is no media linked '
                'with the command \' {} \''.format(cmd)
                ]

    def deleteMedia(self, cmd):
        """Delete saved media related to command.

        :param cmd: Keyword related with saved media
        :type cmd: string
        :return: Deleted titles of media related to command
        :rtype: List of strings
        """
        commandFolder = self.getCommandPath(cmd)

        if os.path.isdir(commandFolder):
            deletedMediaList = self.printExistingMediaNames(cmd)
            shutil.rmtree(commandFolder)
            return deletedMediaList

        return [
                'There are no media linked '
                'with the command \' {} \''.format(cmd)
                ]

    def getCommandPath(self, cmd):
        """Get the path of command folder.

        :param cmd: Keyword related with saved media
        :type cmd: string
        :return: Absolute path of command folder in OS
        :rtype: string
        """
        commandFolder = self.permFolder + '/' + cmd
        return commandFolder


if __name__ == '__main__':
    print('madela')
