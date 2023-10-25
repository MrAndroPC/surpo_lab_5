import os
import asyncio
import logging
from sqlalchemy.engine import URL
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from commands import register_user_commands

from db import BaseModel, create_async_engin, get_session_maker, proceeed_schemas
async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))

    register_user_commands(dp)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        host="localhost",
        port=os.getenv("db_port"),
        username=os.getenv("db_user"),
        password=os.getenv("db_pass"),
        database=os.getenv("db_name"),

    )

    async_engin = create_async_engin(postgres_url)
    session_maker = get_session_maker(async_engin)

    await proceeed_schemas(async_engin, BaseModel.metadata)

    await dp.start_polling(bot, session_maker=session_maker)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')