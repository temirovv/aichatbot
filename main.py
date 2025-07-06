import asyncio
import logging
import sys

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from loader import dp, bot, db

from user_handling import admin
from user_handling import user


async def main() -> None:
    db.create_table_users()
    db.create_user_history_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())