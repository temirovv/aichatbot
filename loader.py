from environs import Env

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db_handling.db_user import User


env = Env()
env.read_env()
TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list('ADMINS')
for i in range(len(ADMINS)):
    ADMINS[i] = int(ADMINS[i])

GEMINI_API_KEY = env.str('GEMINI_API_KEY')
print(f'{ADMINS=}')

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = User('data/main.db')

