from aiogram.filters import Command, CommandObject
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Filter


ADMINS = [632260351]

admin_router = Router()


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


@admin_router.message(AdminProtect(), Command('admin_panel'))
async def admin_panel(message: types.Message):
    await message.answer('Это панель администратора')