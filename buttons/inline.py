from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from calendar import Calendar
from buttons.filters import MyCallFilter

inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Kalendar', callback_data='in'),
            InlineKeyboardButton(text='Inline button 2', callback_data='in1'),
        ],
        [
            InlineKeyboardButton(text='Inline button 2', callback_data='in2'),
        ]
    ]
)


def kalendar(yil, oy):
    inline_builder = InlineKeyboardBuilder()
    kalendar = Calendar().itermonthdays2(year=yil, month=oy)

    for i in ("MO", "TU", "WE", "TH", "FR", "SA", "SU"):
        inline_builder.button(text=i, callback_data=i)

    for i in kalendar:
        if i[0]:
            inline_builder.button(text=f"{str(i[0]).zfill(2)}", callback_data=f'{i[0]}')
        else:
            inline_builder.button(text=" ", callback_data=f'{i[0]}')

    inline_builder.adjust(7, repeat=True)
    return inline_builder.as_markup()


def click(chat_id, user_id):
    chat_id, user_id = str(chat_id), str(user_id)
    inline_builder = InlineKeyboardBuilder()
    inline_builder.button(text='click', callback_data=MyCallFilter(chat_id=chat_id, user_id=user_id).pack())
    return inline_builder.as_markup()


job = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Programmer', callback_data='Programmer'),
            InlineKeyboardButton(text='Teacher', callback_data='Teacher'),
        ],
        [
            InlineKeyboardButton(text='Programmer1', callback_data='Programmer1'),
            InlineKeyboardButton(text='Teacher1', callback_data='Teacher1'),
        ]
    ]
)
