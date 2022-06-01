import discord
from discord.ext import commands

from . import cmd_help_msgs as msg
from .comms_handler import CommsHandler

from ....features.captcha_tester.captcha_tester import CaptchaTester
from ....features.captcha_tester.captcha_tester import CaptchaMatchError

from ....features.media_getter.media_handler.send_media import SendMediaHandler
from ....features.media_getter.media_handler.save_media import SaveMediaHandler


sender = SendMediaHandler()
saver = SaveMediaHandler()
capthca_tester = CaptchaTester()  # in case we want it


class MediaFeatureHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.comms_handler = self.bot.get_cog('CommsHandler')

    @commands.command(name='sendMedia', help=msg.SEND_MEDIA)
    async def send_media(self, ctx, *url):
        await sender.send_media(
            self.comms_handler,
            *url,
            ctx=ctx
        )

    @commands.command(name='saveMedia', help=msg.SAVE_MEDIA)
    async def save_media(self, ctx, cmd, *url):
        await saver.save_media(
            cmd,
            self.comms_handler,
            *url,
            ctx=ctx
        )

    @commands.command(name='printMedia', help=msg.PRINT_MEDIA)
    async def print_media(self, ctx, cmd):
        await saver.show_media_names(
            cmd=cmd,
            app_object=self.comms_handler,
            ctx=ctx
        )

    @commands.command(name='showMedia', help=msg.SHOW_MEDIA)
    async def show_media(self, ctx, cmd):
        await saver.show_media(
            cmd=cmd,
            app_object=self.comms_handler,
            ctx=ctx
        )

    @commands.command(name='deleteMedia', help=msg.DELETE_MEDIA)
    async def delete_media(self, ctx, cmd):
        await saver.delete_media(
            cmd=cmd,
            app_object=self.comms_handler,
            ctx=ctx
        )
