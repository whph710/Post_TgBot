from aiogram import Router
from aiogram import types
from aiogram.filters import Filter
from aiogram import F
from aiogram.types import (Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument,
                           ContentType as CT)


ADMINS = [632260351]

admin_router = Router()


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


# Пример отправки тех же данных в виде медиагруппы
@admin_router.message(AdminProtect(), F.content_type.in_([CT.PHOTO, CT.VIDEO, CT.AUDIO, CT.DOCUMENT]))
async def handle_albums(message: Message, album: list[Message]):
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.video:
            file_id = msg.video.file_id
            media_group.append(InputMediaVideo(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.audio:
            file_id = msg.audio.file_id
            media_group.append(InputMediaAudio(media=file_id, caption=msg.caption,
                                               caption_entities=msg.caption_entities))
        elif msg.document:
            file_id = msg.document.file_id
            media_group.append(InputMediaDocument(media=file_id, caption=msg.caption,
                                                  caption_entities=msg.caption_entities))
        else:
            pass

    if media_group:
        await message.answer_media_group(media_group)
    else:
        await message.answer("Альбом пуст.")


@admin_router.message(AdminProtect(), F.photo)
async def photo_handler(message: Message):
    await message.answer_photo(message.photo[-1].file_id, caption=message.caption,
                               caption_entities=message.caption_entities)


@admin_router.message(AdminProtect(), F.video)
async def video_handler(message: Message):
    await message.answer_video(message.video.file_id, caption=message.caption,
                               caption_entities=message.caption_entities)


@admin_router.message(AdminProtect(), F.audio)
async def audio_handler(message: Message):
    await message.answer_audio(message.audio.file_id, caption=message.caption,
                               caption_entities=message.caption_entities)


@admin_router.message(AdminProtect(), F.document)
async def document_handler(message: Message):
    await message.answer_document(message.document.file_id, caption=message.caption,
                                  caption_entities=message.caption_entities)


