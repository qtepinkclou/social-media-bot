import discord

import asyncio

from discord import File
from discord.ext import commands


class CommsHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def receive_from_user(self, ctx, content_type, wait_for=None):

        if content_type == 'single_media':
            try:
                media_url = ctx.message.attachments[0].url
            except IndexError:
                await ctx.send(
                    'You did not send an attachment!'
                )
                return ''
            else:
                return media_url
        elif content_type == 'multi_media':
            raise NotImplementedError
        elif content_type == 'text':
            if wait_for:
                def check(msg: discord.Message):
                    return (
                        msg.author.id == ctx.author.id
                        and msg.channel.id == ctx.channel.id
                    )
                try:
                    response_object = await self.bot.wait_for(
                        event='message',
                        check=check,
                        timeout=wait_for
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        'Times up, try again.'
                    )
                    return ''
                else:
                    return response_object.content
            else:
                raise NotImplementedError

    async def send_to_user(self, ctx, content, content_type):
        if content_type == 'media':
            await ctx.send(file=File(content))
        elif content_type == 'text':
            await ctx.send(content)
