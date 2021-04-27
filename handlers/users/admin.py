import asyncio

from aiogram import types
from aiogram.dispatcher.filters import IDFilter
from sqlalchemy.orm import Session

from data.config import ADMINS
from loader import dp
from utils.db_api.models import User, Level, Subject


@dp.message_handler(IDFilter(ADMINS), commands=['users'])
async def admin_menu(message: types.Message, db: Session):
    await message.delete()
    
    msg = await message.answer(f'Количество пользователей бота: {db.query(User).count()}')
    await asyncio.sleep(5)
    await msg.delete()


@dp.message_handler(IDFilter(ADMINS), commands=['add_level'])
async def add_level(message: types.Message, db: Session):
    db.add(Level(name=message.get_args().replace(' ', '_')))
    db.commit()
    
    msg = await message.answer('Принято!')
    await asyncio.sleep(5)
    await msg.delete()


@dp.message_handler(IDFilter(ADMINS), commands=['add_subject'])
async def add_subject(message: types.Message, db: Session):
    db.add(Subject(name=message.get_args().replace(' ', '_')))
    db.commit()

    msg = await message.answer('Принято!')
    await asyncio.sleep(5)
    await msg.delete()
