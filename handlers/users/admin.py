from aiogram import types
from sqlalchemy.orm import Session

from loader import dp
from utils.db_api.models import User


@dp.message_handler(commands=['users'])
async def admin_menu(message: types.Message, db: Session):
    await message.delete()
    
    await message.answer(f'Количество пользователей бота: {db.query(User).count()}')
