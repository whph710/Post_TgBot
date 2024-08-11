import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


# Middleware для обработки медиагрупп (альбомов)
class SomeMiddleware(BaseMiddleware):
    # Словарь для хранения данных альбомов
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        # Инициализация middleware с задержкой
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        # Проверка, является ли сообщение частью медиагруппы
        if not message.media_group_id:
            pass
        try:
            # Добавление сообщения в существующий альбом
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            # Создание нового альбома, если он еще не существует
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            # Установка флага, что это последнее сообщение в альбоме
            data['_is_last'] = True
            # Добавление альбома в данные
            data["album"] = self.album_data[message.media_group_id]
            # Вызов обработчика с данными
            await handler(message, data)

        # Удаление данных альбома после обработки последнего сообщения
        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']
