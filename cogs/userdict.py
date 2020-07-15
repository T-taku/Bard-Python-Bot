from discord.ext import commands
import discord
from dpybrew.service import Paginator


class MyPagenator(Paginator):
    def __init__(self, client, max_page, data):
        super().__init__(client, max_page)
        self.data = data
        self.tags = sorted(list(self.data.keys()))

    def get_embed(self, page):

        target_tags = self.tags[page * 15: page * 15 + 15]
        target = [f'{i}: {self.data[i]}' for i in target_tags]
        desc = "\n".join(target)

        embed = discord.Embed(title="ユーザー辞書一覧",
                              description=desc
                              )
        return embed


class UserDict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='dict', invoke_without_command=True)
    async def userdict(self, ctx):
        d = await self.bot.db.get_user_dict(ctx.guild.id)
        del d['__id']
        i = (len(d) // 15) + 1 if (len(d) - 1) % 15 else (len(d) - 1) // 15
        p = MyPagenator(self.bot, i, d)
        await p.start(ctx.message)

    @userdict.command()
    async def add(self, ctx, key, *, value):
        if key == "__id":
            await ctx.send('そのkeyは指定できません。')
            return False
        await self.bot.db.set_user_dict(ctx.guild.id, key, value)
        await ctx.send('{0}, {1}を{2}として設定しました。'.format(ctx.author.mention, key, value))

    @userdict.command()
    async def remove(self, ctx, *, key):
        if key == "__id":
            await ctx.send('そのkeyは指定できません。')
            return False
        if await self.bot.db.remove_user_dict(ctx.guild.id, key):
            await ctx.send('{0}, {1}の消去成功しました。'.format(ctx.author.mention, key))
            return
        await ctx.send('それは登録されていません。')


def setup(bot):
    return bot.add_cog(UserDict(bot))

