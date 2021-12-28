from dotenv import dotenv_values


""" Retrieves any configuration value with given key """
class Config:
    def __init__(self, key_file='.env'):
        self.configuration = dotenv_values(key_file)

    def get_parameter(self, key):
        return self.configuration[key]
