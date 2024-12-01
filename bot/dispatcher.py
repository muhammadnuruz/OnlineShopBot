from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('TOKEN')
    # BOT_TOKEN_2 = os.getenv('TOKEN_2')


bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# bot_2 = Bot(Config.BOT_TOKEN_2)
# dp_2 = Dispatcher(bot=bot, storage=MemoryStorage())
