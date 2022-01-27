"""Discord API to host several functionalities.

Currently supported modules are:
    ``pydiscmd``
    ``getmedia``
    ``detect_landmark``
    ``captcha_generator``
"""


import os
import asyncio
import nest_asyncio
import discord
from datetime import datetime
from collections import defaultdict
from discord.ext import commands
from discord import File as sendDiscord
from utils.config import Config
from pydiscmd import PyCmd
from getmedia import SavedMedia
from getmedia import SentMedia
from captcha_generator import MatchError
from captcha_generator import Randomite
from detect_landmark import Landmarks

nest_asyncio.apply()

python_state = defaultdict(str)  # dict containing user:state pairs

cfg = Config()

conv = PyCmd()

captchaControl = Randomite()

sender = SentMedia()
saver = SavedMedia()

landmark = Landmarks()

bot = commands.Bot(command_prefix='!')

TOKEN = cfg.get_param("DISCORD_TOKEN")


@bot.event
async def on_ready():
    """Notify successful connection to Discord server."""
    print(
        f'{bot.user.name} is connected to the Discord! \n'
    )


@bot.listen()
async def on_message(message):
    """Treat the content of the message depending on python_state."""
    if message.author == bot.user or message.content.startswith('!'):
        return

    user_name = message.author.name

    if python_state[user_name] == 'running':
        raw_output_list = conv.process_command(message)

        final_output_list = [
            conv.modify_output(item, mod='o')
            for item in raw_output_list
        ]

        for output_line in final_output_list:
            await message.channel.send(output_line)


@bot.command(name='togglePython', help=cfg.get_param('TOOGLE_PYTHON'))
async def change_state(ctx):
    """Toggle between Discord chat prompt and Python command prompt."""
    user_name = ctx.author.name

    if user_name not in python_state:
        python_state[user_name] = 'idle'

    if python_state[user_name] == 'idle':
        await ctx.send(
            f'You can only chat in Python now {user_name}. '
            'Your Python Mode is ON'
        )

        python_state[user_name] = 'running'

    elif python_state[user_name] == 'running':
        await ctx.send(
            f'You can chat as you wish {user_name}. '
            'Your Python Mode is OFF'
        )

        python_state[user_name] = 'idle'


@bot.command(name='sendMedia', help=cfg.get_param('SEND_MEDIA'))
async def send_media(ctx, *url):
    """Directly acquire and do not store media from multiple URLs."""
    start_time = datetime.now()

    with sender:
        sender.send_media(*url)

        for media_name in os.listdir(sender.temp_youtube):
            await ctx.send(
                file=sendDiscord(
                    sender.temp_youtube + '/' + media_name
                )
            )

        for media_name in os.listdir(sender.temp_instagram):
            await ctx.send(
                file=sendDiscord(
                    sender.temp_instagram + '/' + media_name
                )
            )

    time_took = datetime.now() - start_time

    await ctx.send(f'Process time: {time_took} seconds.')


@bot.command(name='saveMedia', help=cfg.get_param('SAVE_MEDIA'))
async def save_media(ctx, cmd, *url):
    """Save media from multiple URLs under a keyword."""
    start_time = datetime.now()

    saver.save_media(cmd, *url)

    await ctx.send(
        'Saved the following media and linked '
        f'them with command {cmd}'
    )

    for saved_media_name in saver.show_media_names(cmd):
        await ctx.send(saved_media_name)

    time_took = datetime.now() - start_time

    await ctx.send(f'Process time: {time_took} seconds.')


@bot.command(name='deleteMedia', help=cfg.get_param('DELETE_MEDIA'))
async def delete_media(ctx, cmd='fold'):
    """Delete media related with given keyword."""
    deleted_media_names = saver.delete_media(cmd)

    await ctx.send(
        'Deleted following media linked '
        f'with command {cmd}:'
    )

    for deleted_media_name in deleted_media_names:
        await ctx.send(deleted_media_name)


@bot.command(name='printMedia', help=cfg.get_param('PRINT_MEDIA'))
async def print_media(ctx, cmd='fold'):
    """Show a list of saved media under given keyword."""
    saved_media_names = saver.show_media_names(cmd)

    await ctx.send(
        f'The command {cmd} has the following '
        'media linked with it:'
    )

    for saved_media_name in saved_media_names:
        await ctx.send(saved_media_name)


@bot.command(name='showMedia', help=cfg.get_param('SHOW_MEDIA'))
async def show_media(ctx, cmd='fold'):
    """Acquire saved media under given keyword."""
    media_dirs = saver.show_media(cmd)

    if 'There are no media' in media_dirs[0]:
        await ctx.send(media_dirs[0])

    else:
        for media_name in media_dirs:
            await ctx.send(file=sendDiscord(media_name))


@bot.command(name='detectLandmark', help=cfg.get_param('DETECT_LANDMARK'))
async def detect_landmarks(ctx):
    """Detect Landmark if the Captcha Test is passed."""
    await ctx.send(
        'Pass the Captcha Test before getting an answer. '
        'You have 20 seconds to submit.'
    )

    def check(msg: discord.Message):  # msg = discord.Message.
        return (msg.author.id == ctx.author.id
                and msg.channel.id == ctx.channel.id
                )

    # generate string
    captcha_string = captchaControl.generate_random_string()
    # generate image
    captcha_dir = captchaControl.create_captcha_image(
        captcha_string)
    # send image
    await ctx.send(file=sendDiscord(captcha_dir))

    # wait for answer
    try:
        msg = await bot.wait_for(event='message', check=check, timeout=20.0)

    except asyncio.TimeoutError:
        await ctx.send('Times up on the test, try again.')
        return

    else:
        # if answer is true carry on..
        try:
            captchaControl.validate_captcha(msg.content)
        except MatchError:
            await ctx.send("You failed the Captcha Test, you may try again.")
            return
        else:
            await ctx.send(
                'You have passed the Captcha Test '
                'fellow human! Wait for me to check'
                'out that building'
            )
            try:
                image_url = ctx.message.attachments[0].url

            except IndexError:
                await ctx.send(
                    'You did not send a proper image with the command!'
                )
                return

            else:
                predict_set = None
                with landmark:
                    predict_set = landmark.main_process(image_url)

                if predict_set:
                    await ctx.send(
                        'Google Lens supposes this image belongs to:'
                    )
                    for prediction in predict_set:
                        await ctx.send(f'- {prediction} \n')

                else:
                    await ctx.send("Google Lens could not hack it.")
                return


def main():
    """Run Discord Bot."""
    bot.run(TOKEN)
