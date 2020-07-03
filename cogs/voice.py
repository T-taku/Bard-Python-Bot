from discord.ext import commands
import discord

voice_setting = """
`voice <音声の種類(A,B,C,Dのいずれか)>` で音声の種類を変更できます。
`voice speed <スピード>` でスピードの変更ができます。
`voice pitch <ピッチ>` でピッチの変更ができます。
"""


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def voice(self, ctx, voice_type=None):
        """現在の音声設定を表示 voice_typeを指定すると変更"""
        if voice_type is None:
            embed = discord.Embed(title="現在の音声設定")
            embed.add_field(name="音声の種類", value="")
            embed.add_field(name="スピード", value="")
            embed.add_field(name="ピッチ", value="")
            embed.add_field(name="変更方法", value=voice_setting)
            await ctx.send(embed=embed)
            return

        if voice_type not in ["A", "B", "C", "D", "a", "b", "c", "d"]:
            await ctx.send("音声の種類はA,B,C,Dのいずれかで選択してください。")
            return

        # タイプ設定の処理


def setup(bot):
    return bot.add_cog(Voice(bot))
