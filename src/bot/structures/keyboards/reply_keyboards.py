from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.structures.lexicon import lexicon_ru as text

continue_mp_1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.START_MESSAGE_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_2_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_3_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_4 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_4_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_5 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_5_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_6 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_6_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_7 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_7_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

continue_mp_8 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.MESSAGE_8_BTN_TEXT)],
    ],
    resize_keyboard=True,
)

admin_menu_mp = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Статистика"), KeyboardButton(text="Рассылка")],
    ],
    resize_keyboard=True,
)
