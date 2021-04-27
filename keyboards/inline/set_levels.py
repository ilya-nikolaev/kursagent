from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.orm import Session

from utils.db_api.models import User, Level

__all__ = ['levels_keyboard', 'level_data']
level_data = CallbackData('level', 'action', 'level_id')


async def levels_keyboard(db: Session, user: User):
    kb = InlineKeyboardMarkup()
    
    levels = db.query(Level).all()
    if not levels:
        raise LookupError
    
    for level in levels:
        if level in user.levels:
            kb.add(InlineKeyboardButton(
                text='✅ ' + level.name,
                callback_data=level_data.new(action='unsub', level_id=level.id)
            ))
        else:
            kb.add(InlineKeyboardButton(
                text=level.name,
                callback_data=level_data.new(action='sub', level_id=level.id)
            ))
    
    kb.add(InlineKeyboardButton(text='🔵 Готово! 🔵', callback_data='ready'))
    
    return kb
