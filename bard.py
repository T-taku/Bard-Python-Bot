import os
from os.path import join, dirname
from dotenv import load_dotenv
from bot import Bard
from cogs.utils.request import request_tts
import aiohttp
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot = Bard()


extensions = [
    'cogs.voice',
    'cogs.tts',
    'cogs.admin',
    'cogs.userdict',
    'cogs.helping',
    'cogs.setting',
]

for extension in extensions:
    bot.load_extension(extension)


@bot.command()
async def test(ctx):
    async with aiohttp.ClientSession() as session:
        await request_tts(session, 'ハローワールド', 1, 0, "ja-JP", "ja-JP-Wavenet-A")


bot.run(os.environ.get("token"))
