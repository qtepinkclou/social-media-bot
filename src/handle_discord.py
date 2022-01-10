"""Discord API to host several functionalities.

Currently supported modules are:
    ``pydiscmd``

    ``getmedia``
"""

import nest_asyncio

# Why doesn't it work when the following line is executed after any other
# import but works perfectly when located like this?
nest_asyncio.apply()

import os

import pydiscmd

from getmedia import SentMedia
from getmedia import SavedMedia

from discord import File as sendDiscord
from discord.ext import commands

from collections import defaultdict

from datetime import datetime

from utils.config import Config


pythonState = defaultdict(str)  # dict containing user:state pairs

helpComments = {  # Does this really belong here?
    'togglePython':
    'Toggle between Discord chat prompt and Python command prompt.',

    'sendMedia':
    'Directly acquire media from multiple URLs',

    'saveMedia':
    'Save media from multiple URLs under a keyword',

    'deleteMedia':
    'Delete media related with given keyword',

    'printMedia':
    'Show a list of saved media under given keyword',

    'showMedia':
    'Acquire saved media under given keyword'
               }

sender = SentMedia()  # initialize SentMedia
saver = SavedMedia()  # initialize SavedMedia

config = Config()

TOKEN = config.get_parameter("DISCORD_TOKEN")  # Abstract token

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """Notify successful connection to Discord server."""
    print(
        f'{bot.user.name} is connected to the Discord! \n'
         )


@bot.command(name='togglePython', help=helpComments['togglePython'])
async def change_state(ctx):
    """Toggle between Discord chat prompt and Python command prompt."""
    global pythonState
    userName = ctx.author.name

    if userName not in pythonState:
        pythonState[userName] = 'idle'

    if pythonState[userName] == 'idle':
        await ctx.send(
                       'You can only chat in Python now {}. '
                       'Your Python Mode is ON'.format(userName)
                       )

        pythonState[userName] = 'running'

    elif pythonState[userName] == 'running':
        await ctx.send(
                       'You can chat as you wish {}. '
                       'Your Python Mode is OFF'.format(userName)
                       )

        pythonState[userName] = 'idle'


@bot.command(name='sendMedia', help=helpComments['sendMedia'])
async def sendMedia(ctx, *url):
    """Directly acquire and do not store media from multiple URLs.

    :param url: Variable length argument list of URLs
    :type url: List of string
    """
    startTime = datetime.now()

    with sender:
        sender.sendMedia(*url)

        for mediaName in os.listdir(sender.tempYT):
            await ctx.send(file=sendDiscord(sender.tempYT + '/' + mediaName))

        for mediaName in os.listdir(sender.tempIG):
            await ctx.send(file=sendDiscord(sender.tempIG + '/' + mediaName))

    timeTook = datetime.now() - startTime

    await ctx.send('Process time: {} seconds.'.format(timeTook))


@bot.command(name='saveMedia', help=helpComments['saveMedia'])
async def saveMedia(ctx, cmd, *url):
    """Save media from multiple URLs under a keyword.

    :param cmd: Keyword related with saved media
    :type cmd: string
    :param url: Variable length argument list of URLs
    :type url: List of string
    """
    startTime = datetime.now()

    saver.saveMedia(cmd, *url)

    await ctx.send(
                   'Saved the following media and linked '
                   'them with command \' {} \':'.format(cmd)
                   )

    for savedMediaName in saver.printExistingMediaNames(cmd):
        await ctx.send(savedMediaName)

    timeTook = datetime.now() - startTime

    await ctx.send('Process time: {} seconds.'.format(timeTook))


@bot.command(name='deleteMedia', help=helpComments['deleteMedia'])
async def deleteMedia(ctx, cmd='fold'):
    """Delete media related with given keyword.

    :param cmd: Keyword related with saved media
    :type cmd: string, optional
    """
    deletedMediaNames = saver.deleteMedia(cmd)

    await ctx.send(
                   'Deleted following media linked '
                   'with command \' {} \':'.format(cmd)
                   )

    for deletedMediaName in deletedMediaNames:
        await ctx.send(deletedMediaName)


@bot.command(name='printMedia', help=helpComments['printMedia'])
async def printMedia(ctx, cmd='fold'):
    """Show a list of saved media under given keyword.

    :param cmd: Keyword related with saved media
    :type cmd: string, optional
    """
    savedMediaNames = saver.printExistingMediaNames(cmd)

    await ctx.send(
                   'The command \' {} \' has the following '
                   'media linked with it:'.format(cmd)
                   )

    for savedMediaName in savedMediaNames:
        await ctx.send(savedMediaName)


@bot.command(name='showMedia', help=helpComments['showMedia'])
async def showMedia(ctx, cmd='fold'):
    """Acquire saved media under given keyword.

    :param cmd: Keyword related with saved media
    :type cmd: string, optional
    """
    mediaDirs = saver.showMedia(cmd)

    if 'There are no media' in mediaDirs[0]:
        await ctx.send(mediaDirs[0])

    else:
        for mediaName in mediaDirs:
            await ctx.send(file=sendDiscord(mediaName))


@bot.listen()
async def on_message(message):
    """Treat the content of the message depending on pythonState."""
    if message.author == bot.user or message.content.startswith('!'):
        return

    userName = message.author.name

    if pythonState[userName] == 'running':
        _message = pydiscmd.toText(message)
        rawOutputList = pydiscmd.processCmd(_message, pydiscmd.fillerFile)

        finalOutputList = [
                           pydiscmd.modifyOutput(item, mod='o')
                           for item in rawOutputList
                           ]

        for _ in finalOutputList:
            await message.channel.send(_)


def main():
    """Run Discord Bot."""
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
