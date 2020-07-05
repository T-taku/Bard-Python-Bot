import motor.motor_asyncio


class DB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient()
        self.db = self.client['bard_test']
        self.users = self.db['users']
        self.user_dict = self.db['user_dict']

    async def get_user_setting(self, user_id):
        user_id = str(user_id)
        r = await self.users.find_one({'id': user_id})
        if r is None:
            await self.set_user_setting(user_id, f=True)
            return await self.users.find_one({'id': user_id})
        return r

    async def set_user_setting(self, user_id, voice=None, speed=None, pitch=None, f=False):
        """もしある場合、updateする"""
        user_id = str(user_id)
        if f:
            await self.users.insert_one(
                {'id': str(user_id), 'voice': voice or "A", "speed": speed or 1.0, "pitch": pitch or 0.0}
            )
            return True
        d = await self.get_user_setting(user_id)
        if d is None:
            await self.users.insert_one(
                {'id': str(user_id), 'voice': voice or "A", "speed": speed or 1.0, "pitch": pitch or 0.0}
            )
            return True
        await self.users.replace_one(
            {'id': str(user_id)},
            {'id': str(user_id), 'voice': voice or d["voice"], "speed": speed or d["speed"], "pitch": pitch or d["pitch"]}
        )
        return True

    async def register_user_dict(self, guild_id):
        await self.user_dict.insert_one(
            {'id': str(guild_id)}
        )

    async def get_user_dict(self, guild_id):
        r = await self.user_dict.find_one({'id': guild_id})
        if r is None:
            await self.register_user_dict(guild_id)
            return {}
        return r

    async def set_user_dict(self, guild_id, key, value):
        r = await self.get_user_dict(guild_id)
        r[key] = value
        await self.users.replace_one(
            {'id': str(guild_id)},
            r
        )
