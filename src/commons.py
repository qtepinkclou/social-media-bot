"""Common methods needed by multiple modules."""

import os
from abc import ABCMeta
from pathlib import Path


class Commons(metaclass=ABCMeta):
    """Common methods."""

    def __init__(self):
        """Construct."""
        self.cwd = os.getcwd()

    def get_path(self, *args):
        """Get path of file/folder in CWD by passing directories below CWD."""
        path = self.cwd
        for respective in args:
            path += '/' + respective
        return path

    @staticmethod
    def dir_create(folder_path):
        """Check if directory exist, create it if it does not."""
        if os.path.isdir(folder_path) is False:
            os.makedirs(folder_path)
        return folder_path

    @staticmethod
    def delete_files_in_path(folder_path):
        """Delete files in path."""
        _ = [
            file.unlink() for
            file in Path(folder_path).glob('*')
            if file.is_file()
        ]
