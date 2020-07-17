from discord.ext import commands
import discord
import re
import emoji_data_python


class TTSRequest:
    def __init__(self, text, message, lang, voice, speed, pitch):
        self.text = text
        self.guild = message.guild
        self.message = message
        self.lang = lang
        self.voice = voice
        self.speed = speed
        self.pitch = pitch


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
            lang = match.groups()[0] if match.groups()[0] in ['en'] else 'ja'
            text = match.groups()[1]

        text = await self.make_text(text, message)
        setting = await self.bot.db.get_user_setting(message.author.id)
        await self.bot.voice_hooks[message.channel.id].put(
            TTSRequest(text, message, lang, setting['voice'], setting['speed'], setting['pitch'])
        )

    async def make_text(self, text, message):
        guild = message.guild
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

        # bot辞書
        for key, value in message_dict.items():
            text = text.replace(key, value)

        # 名前
        if self.bot.voice_hooks[message.channel.id].before_user_id != message.author.id:
            name = message.author.nick or message.author.name
            if self.bot.guild_setting[guild.id]['name']:
                text = name + "、" + text

        # ユーザー辞書
        d = await self.bot.db.get_user_dict(guild.id)
        del d['__id']
        for key, value in d.items():
            text = text.replace(key, value)

        # 以下略
        if len(text) > self.bot.guild_setting[guild.id]['limit']:
            text = text[:self.bot.guild_setting[guild.id]['limit']] + '、以下略'

        return text


def setup(bot):
    return bot.add_cog(TTS(bot))
