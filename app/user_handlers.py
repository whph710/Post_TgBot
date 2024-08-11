import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction

# Инициализация роутера для пользователей
user_router = Router()


# Обработчик команды /start
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    # Отправка действия "печатает" в чат
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    # Задержка на 2 секунды
    await asyncio.sleep(2)
    # Отправка приветственного сообщения с именем пользователя и его ID
    await message.answer(f'Hi, {message.from_user.username}!\nYou are {message.from_user.id}')
