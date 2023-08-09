from aiogram import Bot
import settings

bot = Bot(settings.get('TG_BOT_TOKEN'))
chat_id = settings.get('TG_CHAT_ID')


async def send_message(actor: str, msg: str) -> None:
    session = await bot.get_session()
    message = f'{actor}: {msg}'
    await bot.send_message(chat_id, message)
    await session.close()
