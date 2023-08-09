import asyncio
from bot import send_message
import redis.asyncio as redis
import logging
import settings

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG
)


async def main():
    await send_message('trade reporter', 'Reporter operational')
    r = redis.from_url(settings.get('MESSAGES_URL'), decode_responses=True)
    while True:
        async with r as client:
            _, msg = await client.brpop('messages')
            logging.info(f'message received: {msg}')
            await send_message('trade reporter', msg)


if __name__ == '__main__':
    asyncio.run(main())
