from aiogram import Bot
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())
bot = Bot(os.getenv('TG_BOT_TOKEN'))


async def send_message(actor: str, msg: str) -> None:
    session = await bot.get_session()
    message = f'{actor}: {msg}'
    await bot.send_message(os.getenv('TG_CHAT_ID'), message)
    await session.close()
