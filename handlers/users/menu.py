from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session

from keyboards.inline import subjects_keyboard
from loader import dp
from keyboards.default import SET_LEVELS, SET_SUBJECTS
from utils.db_api.models import Level, User
from utils.db_api.models import user_level
from keyboards.inline import levels_keyboard


@dp.message_handler(text=SET_LEVELS)
async def set_levels(message: types.Message, db: Session, user: User):
    await message.delete()
    
    try:
        keyboard = await levels_keyboard(db, user)
        await message.answer('Выберите предметы из списка ниже', reply_markup=keyboard)
    except LookupError:
        await message.answer('Уровни пока не настроены(')


@dp.message_handler(text=SET_SUBJECTS)
async def set_subjects(message: types.Message, db: Session, user: User):
    await message.delete()
    
    try:
        keyboard = await subjects_keyboard(db, user)
        await message.answer('Выберите предметы из списка ниже', reply_markup=keyboard)
    except LookupError:
        await message.answer('Предметы пока не настроены(')
