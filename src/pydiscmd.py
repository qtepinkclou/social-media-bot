"""Top level functions for turning Discord message input to Python command."""

import io
from contextlib import redirect_stdout

# Constant variables
FILLER_FILE = 'filler.py'


def toText(discordMessage):
    """Extract the string of text from discord message.

    :param discordMessage: A handle to the :class:`discord.Message` which
      includes the text message sent from Discord
    :param type: class:`discord.Message`
    """
    return discordMessage.content


def saveToFile(text):
    """Write the text input to output file.

    :param text: Text to be saved
    :type text: string
    :return: None
    :rtype: None
    """
    with open(FILLER_FILE, 'w', encoding='utf-8') as f:
        f.write(text)


def runTheFile():
    """Run saved file as Python script.

    :return: Return of the Python script (lines seperated by \\n)
    :rtype: string
    """
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            exec(open(FILLER_FILE).read())
        except Exception:
            print('That was gibberish to me!')
        output = buf.getvalue()
    return output


def disectTheResults(output):
    """Disect given output line by line.

    :param output: Text to be disected
    :type output: string
    :return: Return of the Python script
    :rtype: A list of strings where each element represents a line of the
      total return
    """
    outputs = [item if output
               else 'Nothing to put out!'
               for item in output.rstrip('\n').split('\n')
               ]

    return outputs


def processCmd(text):
    """Save the text input to output FILLER_FILE.

    :param text: Text to be saved
    :type text: string, optional
    :return: Return of the Python script
    :rtype: A list of strings where each element represents a line of the
      total return
    """
    saveToFile(text)
    rawOutput = runTheFile()
    return disectTheResults(rawOutput)


def modifyOutput(text, mod=None):
    """Modify the output text color to Discord.

    Use ``mod=o`` in order to get orange colored text as output

    :param text: Text to be modified
    :type text: string
    """
    if mod == 'o':
        return '```fix\n{}\n```'.format(text)
    else:
        return text
