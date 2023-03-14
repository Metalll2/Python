import logging
import asyncio
from aiogram import Bot, Dispatcher
import differens_types
import group_games

async def main():
    try:
        __FILE = open('setting.txt', 'r')
        __TOKEN =__FILE.read().split()
        __TOKEN = "".join(__TOKEN)
    except Exception as err:
        print(err)
    finally:
        __FILE.close()

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token = __TOKEN)
    dp = Dispatcher()

    
   
    dp.include_router(group_games.router)
    dp.include_router(differens_types.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
