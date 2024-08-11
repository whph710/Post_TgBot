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
    # Загрузка переменных окружения из .env файла
    load_dotenv()

    # Инициализация бота с токеном из переменных окружения
    bot = Bot(token=os.getenv('TOKEN'))

    # Инициализация диспетчера
    dp = Dispatcher()

    # Добавление middleware
    dp.message.middleware(SomeMiddleware())

    # Включение маршрутизаторов
    dp.include_routers(user_router, admin_router)

    # Удаление вебхука и очистка очереди обновлений
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск опроса обновлений
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Время начала работы бота
    time_start = datetime.now()

    # Настройка логирования
    logging.basicConfig(level=logging.INFO,
                        filename='app.log',
                        filemode='w')

    try:
        # Запуск бота
        print(indent + 'Bot started!')
        asyncio.run(main())
    except KeyboardInterrupt:
        # Обработка прерывания по Ctrl+C
        print(indent + 'Bot was working for ', datetime.now() - time_start)
        print(indent + 'Bot stopped!\n' + indent)
