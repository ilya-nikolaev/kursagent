from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.models import User


def get_mailing_keyboard(user: User):
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text='📅 Календарь на все дни', url="https://kursagent.ru/webs/"))
    
    if user.subscribed:
        keyboard.add(InlineKeyboardButton(text='❌ Отказаться от рассылки', callback_data='cancel_mailing'))
    else:
        keyboard.add(InlineKeyboardButton(text='✅ Подписаться на рассылку', callback_data='return_mailing'))

    keyboard.add(InlineKeyboardButton(text='✖️ Скрыть сообщение', callback_data='hide'))
    
    return keyboard
