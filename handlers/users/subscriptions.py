from sqlalchemy.orm import Session

from loader import dp
from aiogram import types

from utils.db_api.models import User, Level, Subject
from keyboards.inline.set_levels import level_data, levels_keyboard
from keyboards.inline.set_subjects import subject_data, subjects_keyboard


@dp.callback_query_handler(text='ready')
async def ready(cq: types.CallbackQuery):
    await cq.answer()
    await cq.message.delete()


@dp.callback_query_handler(level_data.filter(action='sub'))
async def sub_level(cq: types.CallbackQuery, db: Session, user: User, callback_data: dict):
    level = db.query(Level).filter(Level.id == callback_data["level_id"]).first()
    
    user.levels.append(level)
    db.commit()
    
    await cq.answer(f'Вы успешно подписаны на уровень {level.name}!')
    
    keyboard = await levels_keyboard(db, user)
    await cq.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(level_data.filter(action='unsub'))
async def unsub_level(cq: types.CallbackQuery, db: Session, user: User, callback_data: dict):
    level = db.query(Level).filter(Level.id == callback_data["level_id"]).first()
    
    user.levels.remove(level)
    db.commit()
    
    await cq.answer(f'Вы успешно отписаны от уровня {level.name}!')
    
    keyboard = await levels_keyboard(db, user)
    await cq.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(subject_data.filter(action='sub'))
async def sub_subject(cq: types.CallbackQuery, db: Session, user: User, callback_data: dict):
    subject = db.query(Subject).filter(Subject.id == callback_data["subject_id"]).first()
    
    user.subjects.append(subject)
    db.commit()

    await cq.answer(f'Вы успешно подписаны на предмет {subject.name}!')
    
    keyboard = await subjects_keyboard(db, user)
    await cq.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(subject_data.filter(action='unsub'))
async def unsub_subject(cq: types.CallbackQuery, db: Session, user: User, callback_data: dict):
    subject = db.query(Subject).filter(Subject.id == callback_data["subject_id"]).first()
    
    user.subjects.remove(subject)
    db.commit()

    await cq.answer(f'Вы успешно отписаны от предмета {subject.name}!')
    
    keyboard = await subjects_keyboard(db, user)
    await cq.message.edit_reply_markup(keyboard)
