from aiogram import Router
from aiogram import types
from aiogram.filters import Filter
from aiogram import F
from aiogram.types import (Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument,
                           ContentType as CT)

# Список администраторов
ADMINS = [632260351]

# Инициализация роутера для администраторов
admin_router = Router()


# Фильтр для проверки, является ли пользователь администратором
class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        # Проверка, является ли отправитель администратором
        return message.from_user.id in self.admins


# Обработчик для отправки медиагруппы (альбома)
@admin_router.message(AdminProtect(), F.content_type.in_([CT.PHOTO, CT.VIDEO, CT.AUDIO, CT.DOCUMENT]))
async def handle_albums(message: Message, album: list[Message]):
    # Создание списка для медиагруппы
    media_group = []
    for msg in album:
        if msg.photo:
            # Добавление фото в медиагруппу
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.video:
            # Добавление видео в медиагруппу
            file_id = msg.video.file_id
            media_group.append(InputMediaVideo(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.audio:
            # Добавление аудио в медиагруппу
            file_id = msg.audio.file_id
            media_group.append(InputMediaAudio(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.document:
            # Добавление документа в медиагруппу
            file_id = msg.document.file_id
            media_group.append(InputMediaDocument(media=file_id, caption=msg.caption,
                                                 caption_entities=msg.caption_entities))
        else:
            pass

    # Отправка медиагруппы, если она не пуста
    if media_group:
        await message.answer_media_group(media_group)
    else:
        await message.answer("Альбом пуст.")


# Обработчик для копирования сообщения
@admin_router.message(AdminProtect())
async def photo_handler(message: Message):
    # Копирование сообщения в тот же чат с сохранением описания и сущностей
    await (message.copy_to(chat_id=message.chat.id, caption=message.caption, caption_entities=message.caption_entities))
