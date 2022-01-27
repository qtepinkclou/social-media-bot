"""Common methods needed by multiple modules."""

import os
from abc import ABCMeta


class Commons(metaclass=ABCMeta):
    """Common methods."""

    def __init__(self):
        """Construct."""
        self.cwd = os.getcwd()

    def dir_create(self, folder_name):
        """Check if directory exist, create it if it does not."""
        path = self.cwd + '/' + folder_name

        if os.path.isdir(path) is False:
            os.makedirs(folder_name)
        return folder_name
