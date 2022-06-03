import discord
from discord.ext import commands

from . import cmd_help_msgs as msg
from .comms_handler import CommsHandler

from ....features.captcha_tester.captcha_tester import CaptchaTester
from ....features.captcha_tester.captcha_tester import CaptchaMatchError

from ....features.landmark_detector.landmark_detector import LandmarkDetector
from ....features.landmark_detector.landmark_detector import IncompatibleLinkError

landmark_detector = LandmarkDetector()
captcha_tester = CaptchaTester()


class LandmarkFeatureHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.comms_handler = self.bot.get_cog('CommsHandler')

    @commands.command(name='detectLandmark', help=msg.DETECT_LANDMARK)
    async def detect_landmarks(self, ctx):
        try:
            await captcha_tester.main_process(
                app_object=self.comms_handler,
                ctx=ctx
            )
        except CaptchaMatchError:
            return

        try:
            await landmark_detector.main_process(
                app_object=self.comms_handler,
                ctx=ctx
            )
        except IncompatibleLinkError:
            return
