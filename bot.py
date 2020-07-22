import discord
from discord.ext import commands
from cogs.utils.firebase import FireStore
from cogs.utils.db import DB
import asyncio
import aiohttp


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ', '::', 'bard::']
    return base


class Bard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, help_command=None)
        self.voice_hooks = {}
        self.firestore = FireStore(self)
        self.guild_setting = {}
        self.db = DB()
        self.access_token = None
        self.loop.create_task(self.access_token_loop())

    async def error(self, e):
        await self.get_channel(733199945930113074).send(e)

    async def update_guild_setting(self, guild_id):
        """
        bot, name, emoji
        :return:
        """
        bot = await self.db.get_guild_setting('bot', guild_id)
        name = await self.db.get_guild_setting('name', guild_id)
        emoji = await self.db.get_guild_setting('emoji', guild_id)
        limit = await self.db.get_limit(guild_id)
        self.guild_setting[guild_id] = dict(bot=bot, name=name, emoji=emoji, limit=limit)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game("::help | Bard - 読み上げBot"))

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return

        await super().on_command_error(context, exception)

    async def access_token_loop(self):
        while not self.is_closed():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://127.0.0.1:5000') as r:
                    self.access_token = await r.text()

            await asyncio.sleep(3000)
