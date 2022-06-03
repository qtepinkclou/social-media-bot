"""Retrieves any configuration value with given key."""

from dotenv import dotenv_values


class Config:
    """Do configure."""

    def __init__(self, key_file='.env'):
        """Construct method."""
        self.configuration = dotenv_values(key_file)

    def get_param(self, key):
        return self.configuration[key]  # string
