from discord.ext import commands
import discord
import os
from os.path import join, dirname
from dotenv import load_dotenv
from cogs.utils.db import DB
bot_invite = "https://discord.com/api/oauth2/authorize?client_id=727687910643466271&permissions=3230720&scope=bot"
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
fields = [
    ["課金方法", "[こちらのサイト]()に登録し、サーバーを選択してからサブスクリプションに登録してください。"],
]
bot = commands.Bot(command_prefix=commands.when_mentioned_or("bard::"), help_command=None)
bot.voice_hooks = {}
cmds = [
    ["join", "ボイスチャンネルに接続します。"],
    ["leave", "ボイスチャンネルから切断します。"],
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


@bot.command(name='help')
async def help_command(ctx):

    e1, e2 = get_help_embeds()
    await ctx.send(embed=e1)
    await ctx.send(embed=e2)


@bot.command()
async def c(ctx):
    print(bot.voice_clients)

bot.load_extension('cogs.voice')
bot.load_extension('cogs.tts')

bot.db = DB()

bot.run(os.environ.get("token"))
