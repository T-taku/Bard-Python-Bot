import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import concurrent.futures


cred = credentials.Certificate("bard-bot-firestore.json")
firebase_admin.initialize_app(cred)


class FireStore:
    def __init__(self, bot):
        """
        プランと残り文字数、プランへお金を出した人を保存する
        :param bot: discord.ext.commands.Bot
        """
        self.bot = bot
        self.db = firestore.client()
        self.collection = self.db.collection('guilds')
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=40)

    def get_document(self, guild_id):
        return self.collection.document(str(guild_id))

    async def get_guild(self, guild_id):
        """
        ギルドのdictを取得する。もしなければ自動生成する。
        :param guild_id: string or int
        :return: dict
        """
        guild = self.get_document(guild_id)
        r = await self.bot.loop.run_in_executor(self.executor, guild.get)
        d = r.to_dict()
        if d is None:
            await self.bot.loop.run_in_executor(self.executor, guild.set, {'count': 3000})
            return {'count': 3000}
        return d

    async def update_guild(self, guild_id, data):
        guild = self.get_document(guild_id)
        await self.bot.loop.run_in_executor(self.executor, guild.update, data)

    async def spend_char(self, guild_id, count):
        guild = await self.get_guild(guild_id)
        if guild['count'] - count < 0:
            guild['count'] = 0
            await self.update_guild(guild_id, guild)
            return False

        guild['count'] -= count
        await self.update_guild(guild_id, guild)
        return True
