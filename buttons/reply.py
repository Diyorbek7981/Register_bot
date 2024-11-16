from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Referal havola'),
            KeyboardButton(text='Mening ballarim'),
        ],
        [
            KeyboardButton(text='SignUP'),
        ],
        [
            KeyboardButton(text='Contact', request_contact=True),
            KeyboardButton(text='location', request_location=True),
        ],
    ],
    resize_keyboard=True,
    # is_persistent=True
    one_time_keyboard=True,
    input_field_placeholder='Kerakli bo\'limni tanlang'
)

check = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ha'),
        ],
        [
            KeyboardButton(text='/new'),
        ]
    ],
    resize_keyboard=True,
)
