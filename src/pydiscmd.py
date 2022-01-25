"""Top level functions for turning Discord message input to Python command."""

import io
import runpy
from contextlib import redirect_stdout


# Constant variables
FILLER_FILE_NAME = 'FILLER'


def to_text(discord_message):
    """Extract the string of text from discord message."""
    return discord_message.content


def save_to_file(text):
    """Write the text input to output file."""
    with open(FILLER_FILE_NAME + '.py', 'w', encoding='utf-8') as file:
        file.write(text)


def run_the_file():
    """Run saved file as Python script."""
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            runpy.run_module(mod_name=FILLER_FILE_NAME)
        except (SyntaxError, NameError):
            print('That was gibberish to me!')
        output = buf.getvalue()
    return output


def disect_results(output):
    """Disect given output line by line."""
    outputs = [item if output
               else 'Nothing to put out!'
               for item in output.rstrip('\n').split('\n')
               ]
    return outputs


def process_command(text):
    """Save the text input to output FILLER_FILE."""
    save_to_file(text)
    raw_output = run_the_file()
    return disect_results(raw_output)


def modify_output(text, mod=None):
    """Modify the output text color to Discord.

    Use ``mod=o`` in order to get orange colored text as output
    """
    if mod == 'o':
        return f'```fix\n{text}\n```'

    return text
