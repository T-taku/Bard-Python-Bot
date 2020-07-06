import discord
from discord.ext import commands
from .cogs.utils.firebase import FireStore


class Bard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("bard::"), help_command=None)
        self.voice_hooks = {}
        self.firestore = FireStore(self)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game("Bard - 読み上げBot"))
