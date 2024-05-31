import os
import asyncio

from aiogram import Bot, Dispatcher
from datetime import datetime
from dotenv import load_dotenv
import logging

from app.user_handlers import user_router
from app.admin_handlers import admin_router
from app.middleware import SomeMiddleware
indent = '-' * 36 + '\n'


# Запуск бота
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('token'))
    dp = Dispatcher()
    dp.message.middleware(SomeMiddleware())
    dp.include_routers(user_router, admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    time_start = datetime.now()
    logging.basicConfig(level=logging.logMultiprocessing,
                        filename='app.log',
                        filemode='w')
    try:
        print(indent + 'Bot started!')
        asyncio.run(main())
    except KeyboardInterrupt:
        print(indent + 'Bot was working for ', datetime.now() - time_start)
        print(indent + 'Bot stopped!\n' + indent)
