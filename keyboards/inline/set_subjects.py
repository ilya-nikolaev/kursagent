from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.orm import Session

from utils.db_api.models import User, Subject

__all__ = ['subjects_keyboard', 'subject_data']
subject_data = CallbackData('subject', 'action', 'subject_id')


async def subjects_keyboard(db: Session, user: User):
    kb = InlineKeyboardMarkup()
    
    subjects = db.query(Subject).all()
    if not subjects:
        raise LookupError
    
    for subject in subjects:
        if subject in user.subjects:
            kb.add(InlineKeyboardButton(
                text='✅ ' + subject.name,
                callback_data=subject_data.new(action='unsub', subject_id=subject.id)
            ))
        else:
            kb.add(InlineKeyboardButton(
                text=subject.name,
                callback_data=subject_data.new(action='sub', subject_id=subject.id)
            ))
    
    kb.add(InlineKeyboardButton(text='🔵 Готово! 🔵', callback_data='ready'))
    
    return kb
