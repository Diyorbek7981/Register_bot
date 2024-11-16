from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData


class TgFilter(Filter):
    def __init__(self, text_list: list):
        self.text_list = text_list

    async def __call__(self, message: Message):
        return message.text in self.text_list


class MyCallFilter(CallbackData, prefix='my'):
    chat_id: str
    user_id: str
