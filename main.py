import asyncio
import logging
import sys

from bot import *
from db.config import Base, engine
from dispatcher import bot


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    Base.metadata.create_all(engine)
    asyncio.run(main())