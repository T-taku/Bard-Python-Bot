import motor.motor_asyncio


class DB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient()
        self.db = self.client['bard_test']
        self.users = self.db['users']
        self.user_dict = self.db['user_dict']
        self.char_count = self.db['char_count']
        self.guild_emoji = self.db['guild_emoji']
        self.guild_bot = self.db['guild_bot']
        self.guild_name = self.db['guild_name']
        self.guild_limit = self.db['guild_limit']

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
            {'__id': str(guild_id)}
        )

    async def get_user_dict(self, guild_id):
        r = await self.user_dict.find_one({'__id': str(guild_id)})
        if r is None:
            await self.register_user_dict(str(guild_id))
            return {'__id': str(guild_id)}
        del r['_id']
        return r

    async def set_user_dict(self, guild_id, key, value):
        r = await self.get_user_dict(guild_id)
        r[key] = value
        await self.user_dict.replace_one(
            {'__id': str(guild_id)},
            r
        )

    async def remove_user_dict(self, guild_id, key):
        r = await self.get_user_dict(guild_id)
        if key not in r.keys():
            return False
        del r[key]
        await self.user_dict.replace_one(
            {'__id': str(guild_id)},
            r
        )
        return True

    async def get_guild_setting(self, name, guild_id):
        doc = getattr(self, f'guild_{name}')
        r = await doc.find_one({'id': str(guild_id)})
        if r is None:
            if name == 'emoji':
                return True
            elif name == 'name':
                return True
            return False

        return r['value']

    async def set_guild_setting(self, name, guild_id, value):
        doc = getattr(self, f'guild_{name}')
        r = await doc.find_one({'id': str(guild_id)})
        if r is None:
            await doc.insert_one({'id': str(guild_id), 'value': value})
            return
        await doc.replace_one(
            {'id': str(guild_id)},
            {'id': str(guild_id), 'value': value}
        )

    async def get_limit(self, guild_id):
        r = await self.guild_limit.find_one({'id': str(guild_id)})
        if r is None:
            await self.guild_limit.insert_one({'id': str(guild_id), 'limit': 100})
            return 100
        return r['limit']

    async def set_limit(self, guild_id, limit):
        r = await self.get_limit(guild_id)
        await self.guild_limit.replace_one(
            {'id': str(guild_id)},
            {'id': str(guild_id), 'limit': limit}
        )
        return r
