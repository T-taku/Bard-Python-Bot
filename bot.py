import discord
from discord.ext import commands
from cogs.utils.firebase import FireStore
from cogs.utils.db import DB


class Bard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("bard::"), help_command=None)
        self.voice_hooks = {}
        self.firestore = FireStore(self)
        self.guild_setting = {}
        self.db = DB()

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
        await self.change_presence(activity=discord.Game("Bard - 読み上げBot"))

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return

        await super().on_command_error(context, exception)
