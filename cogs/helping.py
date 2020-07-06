import discord
from discord.ext import commands
fields = [
    ["課金方法", "[こちらのサイト]()に登録し、サーバーを選択してからサブスクリプションに登録してください。"],
]
bot_invite = "https://discord.com/api/oauth2/authorize?client_id=727687910643466271&permissions=3230720&scope=bot"
cmds = [
    ["join", "ボイスチャンネルに接続します。"],
    ["leave", "ボイスチャンネルから切断します。"],
    ["dict", "カスタム辞書の一覧を表示します。"],
    ["dict add <キー> <変換先の値>", "ユーザー辞書を設定します。設定した場合、キーを変換先の値として読みます。"],
    ["dict remove <キー>", "ユーザー辞書を削除します。"],
]


def get_help_embeds():
    embed = discord.Embed(
        title='Bard - 読み上げBot',
        description=f"サーバーへは、[こちら]({bot_invite})から導入してください。"
    )
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=False)

    embed2 = discord.Embed(
        title="コマンド一覧"
    )

    for cmd in cmds:
        embed2.add_field(name=cmd[0], value=cmd[1], inline=False)

    return embed, embed2


class Helping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        e1, e2 = get_help_embeds()
        await ctx.send(embed=e1)
        await ctx.send(embed=e2)


def setup(bot):
    return bot.add_cog(Helping(bot))
