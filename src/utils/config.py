"""Retrieves any configuration value with given key."""


from dotenv import dotenv_values


class Config:
    def __init__(self, key_file='src/.env'):
        """Construct method."""
        self.configuration = dotenv_values(key_file)

    def get_parameter(self, key):
        """Return value of key:value pair."""
        return self.configuration[key]
