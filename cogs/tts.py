from discord.ext import commands
import discord
import random
import asyncio
import re


message_dict = {
    'MongoDB': 'もんごDB',
    'wavenet': 'ウェーブネット',
}


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id not in self.bot.voice_hooks.keys():
            return
        if message.author.bot:
            return
        if message.content.startswith("bard::"):
            return
        if message.content.startswith(";"):
            return
        text = message.clean_content
        text = re.sub(r"https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+", "URL省略、", text)
        for key, value in message_dict.items():
            text = text.replace(key, value)

        await asyncio.sleep(random.randrange(1, 3)/10)
        await self.bot.voice_hooks[message.channel.id].put([str(message.author.id).encode(), text.encode(), message.author])


def setup(bot):
    return bot.add_cog(TTS(bot))
