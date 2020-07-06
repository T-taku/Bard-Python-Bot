from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.author.id != 212513828641046529:
            return False
        return True

    @commands.command(name='exit')
    async def exit(self, ctx):
        for key in list(self.bot.voice_hooks):
            try:
                await self.bot.voice_hooks[key].close(force=True)
            except Exception:
                pass


def setup(bot):
    return bot.add_cog(Admin(bot))
