from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


SET_SUBJECTS = "Настроить предметы"
SET_LEVELS = "Настроить уровни"
GET_HELP = "Помощь"


menu_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text=SET_SUBJECTS),
            KeyboardButton(text=SET_LEVELS)
        ],
        [
            KeyboardButton(text=GET_HELP)
        ]
    ],
    resize_keyboard=True
)
