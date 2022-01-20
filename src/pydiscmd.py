"""Top level functions for turning Discord message input to Python command."""

import io
from contextlib import redirect_stdout

# Constant variables
FILLER_FILE = 'filler.py'


def toText(discordMessage):
    """Extract the string of text from discord message."""
    return discordMessage.content


def saveToFile(text):
    """Write the text input to output file."""
    with open(FILLER_FILE, 'w', encoding='utf-8') as f:
        f.write(text)


def runTheFile():
    """Run saved file as Python script."""
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            exec(open(FILLER_FILE).read())
        except Exception:
            print('That was gibberish to me!')
        output = buf.getvalue()
    return output


def disectTheResults(output):
    """Disect given output line by line."""
    outputs = [item if output
               else 'Nothing to put out!'
               for item in output.rstrip('\n').split('\n')
               ]

    return outputs


def processCmd(text):
    """Save the text input to output FILLER_FILE."""
    saveToFile(text)
    rawOutput = runTheFile()
    return disectTheResults(rawOutput)


def modifyOutput(text, mod=None):
    """Modify the output text color to Discord.

    Use ``mod=o`` in order to get orange colored text as output
    """
    if mod == 'o':
        return '```fix\n{}\n```'.format(text)
    else:
        return text
