import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction


user_router = Router()


# Команда "start"
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(2)
    await message.answer(f'Hi, {message.from_user.username}!\nYou are {message.from_user.id}')