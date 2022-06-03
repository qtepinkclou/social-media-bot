from abc import ABCMeta

from ....commons.file_handler import FileHandler
from ..media_downloader.download_manager import DownloadManager


class ABCMediaHandler(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        self.download_manager = DownloadManager()

    def _process_media(self, save_path, *urls):
        list_of_urls = list({*urls})  # avoid repetitions
        for url in list_of_urls:
            loader = self.download_manager.relegate_task(url)
            loader.download_media(save_path, url)
