"""Top level functions for turning Discord message input to Python command."""

import io
import runpy
from contextlib import redirect_stdout
from utils.config import Config
from commons import Commons

cfg = Config()


class PyCmd(Commons):
    """Treat string as if Python command."""

    def __init__(self):
        """Construct."""
        super().__init__()
        self.filler_file = cfg.get_param('FILLER_FILE_NAME')
        self.filler_path = self.cwd + '/' + self.filler_file + '.py'

        self.current_input = str()
        self.current_output_list = []

    def save_to_file(self, discord_message):
        """Write the text input to output file."""
        self.current_input = discord_message.content
        with open(
            self.filler_file + '.py',
            'w',
            encoding='utf-8'
        ) as file:
            file.write(self.current_input)

    def run_the_file(self):
        """Run saved file as Python script."""
        with io.StringIO() as buf, redirect_stdout(buf):
            try:
                runpy.run_path(self.filler_path)
            except (SyntaxError, NameError):
                print('That was gibberish to me!')
            output = buf.getvalue()

        self.current_output_list = [
            item if output
            else 'Nothing to put out!'
            for item in output.rstrip('\n').split('\n')
        ]
        return self.current_output_list

    def process_command(self, text):
        """Save the text input to output FILLER_FILE."""
        self.save_to_file(text)
        raw_output_list = self.run_the_file()
        return raw_output_list

    def modify_output(self, raw_text, mod=None):
        """Modify the output text color to Discord.

        Use ``mod=o`` in order to get orange colored text as output
        """
        if mod == 'o':
            return f'```fix\n{raw_text}\n```'

        return raw_text
