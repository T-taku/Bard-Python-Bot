import discord
from discord.ext import commands

bot_invite = "https://discord.com/api/oauth2/authorize?client_id=727687910643466271&permissions=3230720&scope=bot"
guild_invite = "https://discord.gg/QmCmMtp"
website = "https://bardbot.net/"
fields = [
    ["課金方法", f"[こちらのサイト]({website})に登録し、サーバーを選択してからサブスクリプションに登録してください。"],
    ["特殊機能", "`en::`を先頭につけると、英語で読み上げてくれます。"]
]
cmds = [
    ["::join", "ボイスチャンネルに接続します。"],
    ["::leave", "ボイスチャンネルから切断します。"],
    ["::word", "カスタム辞書の一覧を表示します。"],
    ["::word add <キー> <変換先の値>", "ユーザー辞書を設定します。設定した場合、キーを変換先の値として読みます。"],
    ["::word remove <キー>", "ユーザー辞書を削除します。"],
    ["::pref", "読み上げの設定を表示します。"],
    ["::pref bot", "botの投稿も読み上げるかどうかを設定します。オンの時に実行するとオフに、オフの時に実行するとオンになります。"],
    ["::pref name", "名前を読み上げるかどうかを設定します。オンの時に実行するとオフに、オフの時に実行するとオンになります。"],
    ["::pref emoji", "絵文字を読み上げるかどうかを設定します。オンの時に実行するとオフに、オフの時に実行するとオンになります。"],
    ["::pref limit <読み上げ上限文字数>", "最大読み上げ文字数を設定します。デフォルトは100です。"],
    ["::pref keep-alive", "ラグなどで切断された際に、再接続するか設定します。強制終了した際も再接続します。オンの時に実行するとオフに、オフの時に実行するとオンになります。"],
    ["::voice", "音声の設定を表示します。"],
    ["::voice [A, B, C, D]", "声の種類の設定を変更します。A, Bが女性の声、C, Dが男性の声です。デフォルトはAです。"],
    ["::speed < 0.25~4.0 >", "音声の速さを設定します。デフォルトは1です。"],
    ["::pitch < -20.0~20.0 >", "音声のピッチを設定します。デフォルトは0です。"],
]


def get_help_embeds():
    embed = discord.Embed(
        title='Bard - 読み上げBot',
        description=f"[**` Botの導入URL `**]({bot_invite}) [**` 公式サーバー `**]({guild_invite}) [**` website `**]({website})"
    )
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=False)

    embed2 = discord.Embed(
        title="コマンド一覧", description="プレフィックスは`::`もしくは`bard::`です。"
    )

    for cmd in cmds:
        embed2.add_field(name=cmd[0], value=cmd[1], inline=False)

    return embed, embed2


def get_do_subscribe_embed():
    embed = discord.Embed(
                title='サブスクリプションに登録しませんか？',
                description='サブスクリプションに登録することで機能を使用可能になります。まず無料の3000文字を試してから、サブスクリプションに登録しましょう。0文字になると、使用できなくなります。'
            )
    embed.add_field(
        name='サブスクリプションの登録方法',
        value='まず、[Webサイト](https://bardbot.net)に飛び、ユーザー登録をしましょう。\n'
              '次に、[ギルド一覧](https://bardbot.net/guilds)からサブスクリプションを設定したいギルドを選択します。\n'
              'その後、カード情報などを入力すれば、登録完了です。'
    )
    return embed


class Helping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        e1, e2 = get_help_embeds()
        await ctx.send(embed=e1)
        await ctx.send(embed=e2)
        db_guild = await self.bot.firestore.get_guild(ctx.guild.id)
        if db_guild['subscribe'] == 0:
            await ctx.send(embed=get_do_subscribe_embed())


def setup(bot):
    return bot.add_cog(Helping(bot))
