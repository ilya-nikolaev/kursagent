from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from sqlalchemy.orm import Session

from loader import dp
from utils.db_api.models import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, db: Session, user: User):
    if user:
        await message.answer('Вы уже в базе)')
    else:
        user = User(user_id=message.from_user.id, user_name=message.from_user.username)
        
        db.add(user)
        db.commit()
        
        await message.answer(f"Привет, {message.from_user.full_name}!")
