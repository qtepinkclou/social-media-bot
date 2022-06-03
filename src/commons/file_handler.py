"""Common methods needed by multiple modules."""

import os
import shutil
from pathlib import Path


class FileHandler:
    """File handling methods."""

    cwd = os.getcwd()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileHandler, cls).__new__(cls)
        return cls.instance

    def get_path(self, *args):
        path = FileHandler.cwd
        for respective in args:
            path += '/' + respective
        return path

    @staticmethod
    def dir_create(dir_path):
        """Check if directory exist, create it if it does not."""
        if os.path.isdir(dir_path) is False:
            os.makedirs(dir_path)
        return dir_path

    @staticmethod
    def delete_files_in_path(folder_path):
        """Delete files in path."""
        _ = [
            file.unlink() for
            file in Path(folder_path).glob('*')
            if file.is_file() or file.is_folder()
        ]

    @staticmethod
    def remove_directory(dir_path):
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
