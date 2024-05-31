from aiogram.types import *
from aiogram.utils.media_group import MediaGroupBuilder
from typing import *


async def createMediaGroup1(album: List[Message]) -> MediaGroupBuilder:
    mediaGroup = MediaGroupBuilder()

    for m_id in album:
        m = await bot.get_api().get_message(chat_id=chat_id, message_id=m_id)

        match m.content_type:
            case ContentType.PHOTO:
                mediaGroup.add_photo(
                    media=m.photo[-1].file_id,
                    caption=m.caption,
                    caption_entities=m.caption_entities,
                )

            case ContentType.VIDEO:
                mediaGroup.add_video(
                    media=m.video.file_id,
                    caption=m.caption,
                    caption_entities=m.caption_entities,
                )

            case ContentType.DOCUMENT:
                mediaGroup.add_document(
                    media=m.document.file_id,
                    caption=m.caption,
                    caption_entities=m.caption_entities,
                )

    return mediaGroup
