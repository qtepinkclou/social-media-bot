"""Retrieves any configuration value with given key."""


from dotenv import dotenv_values


class Config:
    """Do configure."""

    def __init__(self, key_file='src/.env'):
        """Construct method."""
        self.configuration = dotenv_values(key_file)

    def get_param(self, key, **kwargs):
        """Return value of key:value pair."""
        var_type = kwargs.get('var_type', 'str')

        if var_type == 'int':
            return int(self.configuration[key])

        elif var_type == 'Lstr':  # List of strings
            return self.configuration[key].split(
                sep=self.configuration['SEP']
            )

        elif var_type == 'Lint':  # List of integers
            return [
                int(value)
                for value
                in self.configuration[key].split(
                    sep=self.configuration['SEP']
                )
            ]

        return self.configuration[key]  # string
