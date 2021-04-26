from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


SET_SUBJECTS = "Настроить предметы"
SET_LEVELS = "Настроить уровни"
SET_TIME = "Настроить время рассылки"
GET_HELP = "Помощь"
GET_TIMETABLE = "Отправить расписание на сегодня"


menu_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text=SET_SUBJECTS),
            KeyboardButton(text=SET_LEVELS)
        ],
        [
            KeyboardButton(text=SET_TIME),
            KeyboardButton(text=GET_TIMETABLE)
        ]
    ],
    resize_keyboard=True
)
