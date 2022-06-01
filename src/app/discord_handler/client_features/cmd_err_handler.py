import discord
from discord.ext import commands


unknown_cmd_msg = 'I do not know that command?!'


class CmdErrHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.comms_handler = self.bot.get_cog('CommsHandler')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            await self.comms_handler.send_to_user(
                ctx=ctx,
                content=unknown_cmd_msg,
                content_type='text',
            )
