"""Discord API to host several functionalities.

Currently supported modules are:
    ``pydiscmd``
    ``getmedia``
    ``detect_landmark``
    ``captcha_generator``
"""

import nest_asyncio
import asyncio

# Why doesn't it work when the following line is executed after any other
# import but works perfectly when located like this?
nest_asyncio.apply()

import os

from detect_landmark import Landmarks

from captcha_generator import Randomite
from captcha_generator import MatchError

import pydiscmd

from getmedia import SentMedia
from getmedia import SavedMedia

from discord import File as sendDiscord
from discord.ext import commands
import discord

from collections import defaultdict

from datetime import datetime
from utils.config import Config

# Constant variables
HELP_COMMENTS = {
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
    'Acquire saved media under given keyword',

    'detectLandmark':
    'Get the predicted name of the landmark which is in the provided image with the command'
               }

pythonState = defaultdict(str)  # dict containing user:state pairs

captchaControl = Randomite()

sender = SentMedia()  # initialize SentMedia
saver = SavedMedia()  # initialize SavedMedia

landmark = Landmarks()  # initialize Landmarks

config = Config()
TOKEN = config.get_parameter("DISCORD_TOKEN")  # Abstract token

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """Notify successful connection to Discord server."""
    print(
        f'{bot.user.name} is connected to the Discord! \n'
         )


@bot.listen()
async def on_message(message):
    """Treat the content of the message depending on pythonState."""
    if message.author == bot.user or message.content.startswith('!'):
        return

    userName = message.author.name

    if pythonState[userName] == 'running':
        _message = pydiscmd.toText(message)
        rawOutputList = pydiscmd.processCmd(_message)

        finalOutputList = [
                           pydiscmd.modifyOutput(item, mod='o')
                           for item in rawOutputList
                           ]

        for _ in finalOutputList:
            await message.channel.send(_)


@bot.command(name='togglePython', help=HELP_COMMENTS['togglePython'])
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


@bot.command(name='sendMedia', help=HELP_COMMENTS['sendMedia'])
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


@bot.command(name='saveMedia', help=HELP_COMMENTS['saveMedia'])
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


@bot.command(name='deleteMedia', help=HELP_COMMENTS['deleteMedia'])
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


@bot.command(name='printMedia', help=HELP_COMMENTS['printMedia'])
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


@bot.command(name='showMedia', help=HELP_COMMENTS['showMedia'])
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


@bot.command(name='detectLandmark', help=HELP_COMMENTS['detectLandmark'])
async def detectLandmark(ctx):
    """Detect Landmark."""
    await ctx.send('Pass the Captcha Test before getting an answer. You have 20 seconds to submit.')

    def check(m: discord.Message):  # m = discord.Message.
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

    # generate string
    captchaString = captchaControl.generate_random_string()
    # generate image
    captchaDir = captchaControl.create_captcha_image(
      captchaString,
      fonts_dir=captchaControl.permFonts  # fonts directory
      )
    # send image
    await ctx.send(file=sendDiscord(captchaDir))

    # wait for answer
    try:
        msg = await bot.wait_for(event='message', check=check, timeout=20.0)

    except asyncio.TimeoutError:
        await ctx.send('Times up on the test, try again.')
        return

    else:
        try:
            captchaControl.validate_captcha(msg.content)
        except MatchError:
            await ctx.send("You failed the Captcha Test, you may try again.")
            return
        else:
            await ctx.send("You have passed the Captcha Test fellow human! Wait for me to check out that building")
            try:
                imageUrl = ctx.message.attachments[0].url

            except IndexError:
                print('There are no attachments!')
                await ctx.send('You did not send a proper image with the command!')
                return

            else:
                predictSet = None
                with landmark:
                    predictSet = landmark.main_process(imageUrl)

                if predictSet:
                    await ctx.send("Google Lens supposes this image belongs to:")
                    for prediction in predictSet:
                        await ctx.send("- {} \n".format(prediction))

                else:
                    await ctx.send("Google Lens could not hack it.")
                return


def main():
    """Run Discord Bot."""
    bot.run(TOKEN)


if __name__ == '__main__':  # FIX NEEDED!!!! Do not use this implementation
    main()
