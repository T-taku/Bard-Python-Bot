import asyncio
import discord
import audioop
import io
import aiohttp
from cogs.utils.request import request_tts


class VoiceServer:
    def __init__(self, bot, vclient, vchannel, tchannel):
        self.bot = bot
        self.queue = asyncio.Queue(200, loop=bot.loop)
        self.voice_client = vclient
        self.voice_channel = vchannel
        self.text_channel = tchannel
        self.session = None
        self.task = self.bot.loop.create_task(self.loop())
        self.before_user_id = None

    async def close(self, force=False):
        self.voice_client.stop()
        await self.session.close()
        if force:
            await self.voice_client.disconnect(force=True)
            del self.bot.voice_hooks[self.text_channel.id]
        self.task.cancel()

    async def put(self, item):
        await self.queue.put(item)

    async def setup(self):
        self.session = aiohttp.ClientSession()
        return True

    async def reconnect(self, channel):
        try:
            state = await channel.connect(timeout=5)
            self.voice_channel = channel
            self.voice_client = state
        except discord.ClientException:
            await asyncio.sleep(5)
            await self.reconnect(channel)

    async def loop(self):
        try:
            while not self.bot.is_closed():
                req = await self.queue.get()

                if not await self.bot.firestore.spend_char(req.guild.id, len(req.text)):
                    await self.text_channel.send("申し訳ございません。今月の利用可能文字数を超えてしまいました。"
                                                 "\nまだご利用になりたい場合は、公式サイトより文字数を購入してください。")
                    await self.close(force=True)
                    return

                await req.convert_username(self.before_user_id)
                data = await request_tts(self.bot.access_token, self.session, req)
                self.before_user_id = req.message.author.id
                while self.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                await asyncio.sleep(0.2)

                source = discord.PCMAudio(io.BytesIO(audioop.tostereo(data, 2, 1, 1)))
                self.voice_client.play(source)

        except asyncio.exceptions.CancelledError:
            pass

        except audioop.error as e:
            import traceback
            traceback.print_exc()
            await self.bot.error(e)
            await self.text_channel.send('内部エラーが発生しました。再接続してください。')
            await self.close(force=True)

        except Exception as e:
            import traceback
            traceback.print_exc()
            await self.bot.error(e)
            await self.text_channel.send('内部エラーが発生しました。再接続してください。')
            await self.close(force=True)

