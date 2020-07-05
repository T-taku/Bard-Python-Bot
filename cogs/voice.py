from discord.ext import commands
from .utils.voiceserver import VoiceServer
import discord


voice_setting = """
`voice <音声の種類(A,B,C,Dのいずれか)>` で音声の種類を変更できます。
`speed <スピード>` でスピードの変更ができます。デフォルトは1.0です。
`pitch <ピッチ>` でピッチの変更ができます。デフォルトは0.0です。
"""


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.guild is None:
            await ctx.send("ギルド専用コマンドです。")
            return

        voice_state = ctx.author.voice

        if (not voice_state) or (not voice_state.channel):
            await ctx.send("ボイスチャンネルに接続した状態で動かしてください。")
            return

        channel = voice_state.channel
        try:
            voice_client = await channel.connect()
        except discord.errors.ClientException:
            await ctx.send('すでに接続されています。')
            return

        server = VoiceServer(self.bot, voice_client, channel, ctx.channel)
        await server.setup()
        self.bot.voice_hooks[ctx.channel.id] = server
        await ctx.send("接続しました。")

    @commands.command()
    async def leave(self, ctx):
        if ctx.guild is None:
            await ctx.send("ギルド専用コマンドです。")
            return

        voice_state = ctx.author.voice

        if (not voice_state) or (not voice_state.channel):
            await ctx.channel.send("ボイスチャンネルに接続している状態で実行してください。")
            return

        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            await ctx.send("ボイスチャンネルに接続していません。")
            return

        if ctx.channel.id not in self.bot.voice_hooks.keys():
            await ctx.send("このテキストチャンネルは接続されていません。")
            return

        await self.bot.voice_hooks[ctx.channel.id].close()
        del self.bot.voice_hooks[ctx.channel.id]

        await voice_client.disconnect()
        await ctx.send("切断しました。")

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
        if -20.0 <= pitch <= 20.0:
            await self.bot.db.set_user_setting(ctx.author.id, pitch=pitch)
            await ctx.send(f"ピッチの設定を{pitch}に変更しました。")
            return
        await ctx.send('ピッチは-20.0から20.0の間で設定してください。')


def setup(bot):
    return bot.add_cog(Voice(bot))
