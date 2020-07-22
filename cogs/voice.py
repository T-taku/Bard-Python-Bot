from discord.ext import commands
from .utils.voiceserver import VoiceServer
import discord
import asyncio


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.bot.firestore.get_guild(guild.id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.bot.user.id:
            return
        if before.channel and not after.channel:
            t = None
            for key, server in self.bot.voice_hooks.items():
                if server.voice_channel.id == before.channel.id:
                    t = server
                    break
            if t is None:
                return
            await t.close(True)
            await t.text_channel.send('強制的に落とされたため、終了します。')

    @commands.command()
    async def join(self, ctx):
        if ctx.guild is None:
            await ctx.send("ギルド専用コマンドです。")
            return

        voice_state = ctx.author.voice

        if (not voice_state) or (not voice_state.channel):
            await ctx.send("ボイスチャンネルに接続した状態で実行してください。")
            return

        channel = voice_state.channel
        try:
            voice_client = await channel.connect()
        except discord.errors.ClientException:
            await ctx.send('すでに接続されています。')
            return
        except asyncio.exceptions.TimeoutError:
            await ctx.send('接続できませんでした。ユーザー数が埋まっている可能性があります。再度接続してください。')
            return
        except Exception as e:
            await ctx.send('予期せぬエラーが発生しました。再度接続してください。')
            return

        g = await self.bot.firestore.get_guild(ctx.guild.id)
        if g['count'] == 0:
            await ctx.send("申し訳ございません。今月の利用可能文字数を超えてしまいました。"
                           "\nまだご利用になりたい場合は、公式サイトより文字数を購入してください。")
            return

        server = VoiceServer(self.bot, voice_client, channel, ctx.channel)
        self.bot.voice_hooks[ctx.channel.id] = server
        r = await server.setup()
        if r:
            await self.bot.update_guild_setting(ctx.guild.id)
            await ctx.send("接続しました。")
            try:
                await ctx.guild.me.edit(deafen=True)
            except Exception:
                pass

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


def setup(bot):
    return bot.add_cog(Voice(bot))
