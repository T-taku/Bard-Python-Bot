from discord.ext import commands
import discord
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
        if not message.content:
            return
        if message.content.startswith("bard::"):
            return
        if message.content.startswith(";"):
            return
        text = message.clean_content
        text = re.sub(r"https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+", "URL省略、", text)
        for emoji_name in re.findall(r"<:(.+):[0-9]+>", text):
            text = re.sub(rf"<:{emoji_name}:[0-9]+>", emoji_name, text)

        for move_emoji_name in re.findall(r"<a:(.+):[0-9]+>", text):
            text = re.sub(rf"<a:{move_emoji_name}:[0-9]+>", move_emoji_name, text)

        text = re.sub(r"[^a-zA-Z]([w]+)[^a-zA-Z]", "わら", text)
        text = re.sub(r"^([w]+)$", "わら", text)

        for key, value in message_dict.items():
            text = text.replace(key, value)

        await self.bot.voice_hooks[message.channel.id].put([str(message.author.id).encode(), text, message.author])


def setup(bot):
    return bot.add_cog(TTS(bot))
