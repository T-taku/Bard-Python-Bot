import os
from os.path import join, dirname
from dotenv import load_dotenv
from cogs.utils.db import DB
from bot import Bard
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot = Bard()


extensions = [
    'cogs.voice',
    'cogs.tts',
    'cogs.admin',
    'cogs.userdict',
    'cogs.helping'
]

for extension in extensions:
    bot.load_extension(extension)

bot.db = DB()

bot.run(os.environ.get("token"))
