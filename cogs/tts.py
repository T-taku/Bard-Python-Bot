from discord.ext import commands
import discord
import re
import emoji_data_python


message_dict = {
    'MongoDB': 'もんごDB',
    'wavenet': 'ウェーブネット',
}


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return
        if message.guild.id not in self.bot.guild_setting.keys():
            return
        if message.channel.id not in self.bot.voice_hooks.keys():
            return
        if message.author.bot and not self.bot.guild_setting[message.guild.id]['bot']:
            return
        if not message.content:
            return
        if message.content.startswith("bard::"):
            return
        if message.content.startswith(";"):
            return
        text = message.clean_content
        lang = 'ja'
        if re.match("([a-zA-Z]{2})::(.+)", text):
            match = re.match("([a-zA-Z]{2})::(.+)", text)
            lang = match.groups()[0]
            text = match.groups()[1]
        text = re.sub(r"https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+", "URL省略、", text)
        for emoji_name in re.findall(r"<:(.+):[0-9]+>", text):
            if self.bot.guild_setting[message.guild.id]['emoji']:
                text = re.sub(rf"<:{emoji_name}:[0-9]+>", emoji_name, text)
            else:
                text = re.sub(rf"<:{emoji_name}:[0-9]+>", "", text)
                emojis = emoji_data_python.get_emoji_regex().findall(text)
                for emoji in emojis:
                    text = text.replace(emoji, '')

        for move_emoji_name in re.findall(r"<a:(.+):[0-9]+>", text):
            if self.bot.guild_setting[message.guild.id]['emoji']:
                text = re.sub(rf"<a:{move_emoji_name}:[0-9]+>", move_emoji_name, text)
            else:
                text = re.sub(rf"<a:{move_emoji_name}:[0-9]+>", '', text)

        text = re.sub(r"([^a-zA-Z])([w]+)([^a-zA-Z])", r"\1、わら、\3", text)
        text = re.sub(r"^([w]+)$", "わら", text)
        text = re.sub(r"([^a-zA-Z])([w]+)$", r"\1、わら", text)

        for key, value in message_dict.items():
            text = text.replace(key, value)

        await self.bot.voice_hooks[message.channel.id].put([str(message.author.id).encode(), text, message.author, lang])


def setup(bot):
    return bot.add_cog(TTS(bot))
