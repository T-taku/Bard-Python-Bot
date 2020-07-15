import asyncio
import discord
import audioop
import io


class VoiceServer:
    def __init__(self, bot, vclient, vchannel, tchannel):
        self.bot = bot
        self.queue = asyncio.Queue(200, loop=bot.loop)
        self.voice_client = vclient
        self.voice_channel = vchannel
        self.text_channel = tchannel
        self.reader = None
        self.writer = None
        self.task = self.bot.loop.create_task(self.loop())
        self.before_user_id = None

    async def close(self, force=False):
        self.voice_client.stop()
        if self.writer is not None:
            self.writer.close()
        if force:
            await self.voice_client.disconnect(force=True)
            del self.bot.voice_hooks[self.text_channel.id]
        self.task.cancel()

    async def put(self, item):
        await self.queue.put(item)

    async def setup(self):
        try:
            self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 4445,
                                                                     loop=self.bot.loop)
            return True
        except ConnectionRefusedError:
            await self.text_channel.send("音声を合成するサーバーがダウンしているようです。しばらくお待ちください。")
            await self.close(True)
            return False

    async def loop(self):
        try:
            while not self.bot.is_closed():
                item = await self.queue.get()
                await asyncio.sleep(0.3)
                text = item[1]
                user = item[2]
                guild = user.guild
                name = user.nick or user.name
                if self.before_user_id != user.id:
                    if self.bot.guild_setting[guild.id]['name']:
                        text = name+"、" + text
                self.before_user_id = user.id

                # user dict
                d = await self.bot.db.get_user_dict(guild.id)
                del d['__id']
                for key, value in d.items():
                    text = text.replace(key, value)

                text = text + "。"
                if len(text) > self.bot.guild_setting[guild.id]['limit']:
                    text = text[:self.bot.guild_setting[guild.id]['limit']] + "、以下略。"
                if not await self.bot.firestore.spend_char(guild.id, len(text)):
                    await self.text_channel.send("申し訳ございません。今月の利用可能文字数を超えてしまいました。"
                                                 "\nまだご利用になりたい場合は、公式サイトより文字数を購入してください。")
                    await self.close(force=True)
                    return

                self.writer.write(item[0])
                await self.writer.drain()
                self.writer.write(item[3].encode())
                await self.writer.drain()
                self.writer.write(text.encode())
                await self.writer.drain()
                data = b''  # TODO: 一気に読み込ませる
                while True:
                    i = await self.reader.read(1024)
                    l = len(i)
                    data += i
                    if l != 1024:
                        break

                while self.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                await asyncio.sleep(0.2)

                source = discord.PCMAudio(io.BytesIO(audioop.tostereo(data, 2, 1, 1)))
                self.voice_client.play(source)

        except asyncio.exceptions.CancelledError:
            pass

        except audioop.error:
            import traceback
            traceback.print_exc()
            await self.text_channel.send('内部エラーが発生しました。再接続してください。')
            await self.close(force=True)

        except Exception:
            import traceback
            traceback.print_exc()
            await self.text_channel.send('内部エラーが発生しました。再接続してください。')
            await self.close(force=True)

