from discord.ext import commands
import discord

voice_setting = """
`voice <音声の種類(A,B,C,Dのいずれか)>` で音声の種類を変更できます。
`speed <スピード>` でスピードの変更ができます。デフォルトは1.0です。
`pitch <ピッチ>` でピッチの変更ができます。デフォルトは0.0です。
"""


def yomiage(a): return '読み上げる' if a else '読み上げない'


class VoiceSetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def voice(self, ctx, voice_type=None):
        """現在の音声設定を表示 voice_typeを指定すると変更"""
        if voice_type is None:
            setting = await self.bot.db.get_user_setting(str(ctx.author.id))
            embed = discord.Embed(title="現在の音声設定")
            embed.add_field(name="音声の種類", value=f"{setting['voice']}")
            embed.add_field(name="スピード", value=f"{setting['speed']}")
            embed.add_field(name="ピッチ", value=f"{setting['pitch']}")
            embed.add_field(name="変更方法", value=voice_setting)
            await ctx.send(embed=embed)
            return

        if voice_type not in ["A", "B", "C", "D", "a", "b", "c", "d"]:
            await ctx.send("音声の種類はA,B,C,Dのいずれかで選択してください。")
            return

        # タイプ設定の処理
        await self.bot.db.set_user_setting(ctx.author.id, voice=voice_type.upper())
        await ctx.send(f'声の設定を{voice_type}に変更しました。')

    @commands.command()
    async def speed(self, ctx, speed: float):
        if 0.25 <= speed <= 4.0:
            await self.bot.db.set_user_setting(ctx.author.id, speed=speed)
            await ctx.send(f"スピードの設定を{speed}に変更しました。")
            return
        await ctx.send("スピードは0.5から4.0の間で設定してください。")

    @commands.command()
    async def pitch(self, ctx, pitch: float):
        if -6.5 <= pitch <= 6.5:
            await self.bot.db.set_user_setting(ctx.author.id, pitch=pitch)
            await ctx.send(f"ピッチの設定を{pitch}に変更しました。")
            return
        await ctx.send('ピッチは-6.5から6.5の間で設定してください。')

    @commands.group(invoke_without_command=True, aliases=['pref'])
    async def setting(self, ctx):
        await ctx.send(f"botのメッセージを読み上げるか: {self.bot.guild_setting[ctx.guild.id]['bot']}\n"
                       f"名前を読み上げるか: {self.bot.guild_setting[ctx.guild.id]['name']}\n"
                       f"絵文字を読み上げるか: {self.bot.guild_setting[ctx.guild.id]['emoji']}\n"
                       f"読み上げ上限文字数: {self.bot.guild_setting[ctx.guild.id]['limit']}文字")
        return

    @setting.command()
    async def bot(self, ctx):
        r = await self.bot.db.get_guild_setting('bot', ctx.guild.id)
        await self.bot.db.set_guild_setting('bot', ctx.guild.id, not r)
        await self.bot.update_guild_setting(ctx.guild.id)
        await ctx.send(f'botのメッセージを読み上げるかの設定を`{yomiage(r)}`から{yomiage(not r)}に変更しました。')

    @setting.command()
    async def name(self, ctx):
        r = await self.bot.db.get_guild_setting('name', ctx.guild.id)
        await self.bot.db.set_guild_setting('name', ctx.guild.id, not r)
        await self.bot.update_guild_setting(ctx.guild.id)
        await ctx.send(f'名前を読み上げるかの設定を`{yomiage(r)}`から{yomiage(not r)}に変更しました。')

    @setting.command()
    async def emoji(self, ctx):
        r = await self.bot.db.get_guild_setting('emoji', ctx.guild.id)
        await self.bot.db.set_guild_setting('emoji', ctx.guild.id, not r)
        await self.bot.update_guild_setting(ctx.guild.id)
        await ctx.send(f'絵文字を読み上げるかの設定を`{yomiage(r)}`から{yomiage(not r)}に変更しました。')

    @setting.command()
    async def limit(self, ctx, limit: int):
        if limit <= 0 or limit > 2000:
            await ctx.send('その値は指定できません。')
            return
        r = await self.bot.db.set_limit(ctx.guild.id, limit)
        await self.bot.update_guild_setting(ctx.guild.id)
        await ctx.send(f'最大読み上げ文字数を{r}から{limit}に変更しました。')


def setup(bot):
    return bot.add_cog(VoiceSetting(bot))
