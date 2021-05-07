from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_broadcaster_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton('Отправить сообщение без кнопок', callback_data='send_wo_buttons'))
    keyboard.add(InlineKeyboardButton('Добавить кнопки с ссылками', callback_data='send_with_buttons'))
    keyboard.add(InlineKeyboardButton('Отмена', callback_data='do_not_send'))
    
    return keyboard
