import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import false
from sqlalchemy.orm import Session

from data.config import ADMINS
from keyboards.inline.admin import get_broadcaster_keyboard
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


@dp.message_handler(IDFilter(ADMINS), commands=['shutdown'])
async def shutdown(message: types.Message):
    await message.delete()
    exit(0)


@dp.message_handler(IDFilter(ADMINS), commands=['my_user'])
async def my_user(message: types.Message, user: User):
    await message.delete()
    msg = await message.answer(f'ID: {user.user_id}, username: {user.user_name}, mailing_time: {user.mailing_time}')
    await asyncio.sleep(5)
    await msg.delete()


async def broadcast(message: types.Message, db: Session, keyboard=None):
    users: list[User] = db.query(User).filter(User.banned == false()).all()
    
    if keyboard is None:
        keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='✖️ Скрыть сообщение', callback_data='hide'))
    
    for user in users:
        try:
            await message.send_copy(user.user_id, reply_markup=keyboard)
        except Exception as e:
            logging.exception(e)


@dp.message_handler(IDFilter(ADMINS), commands=['broadcast'])
async def broadcaster(message: types.Message, state: FSMContext):
    await message.delete()
    
    msg = await message.answer('Отправьте сообщение которое хотите разослать')
    await state.set_state('catch_message')
    
    await asyncio.sleep(3)
    await msg.delete()


@dp.message_handler(IDFilter(ADMINS), state='catch_message', content_types=types.ContentTypes.ANY)
async def catch_message(message: types.Message, state: FSMContext):
    await message.delete()
    
    await state.update_data(message=message)
    await message.send_copy(message.chat.id, reply_markup=get_broadcaster_keyboard())


@dp.callback_query_handler(IDFilter(ADMINS), state='catch_message', text='do_not_send')
async def do_not_send(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.delete()
    await cq.answer('Ввод отменён')
    
    await state.reset_state()


@dp.callback_query_handler(IDFilter(ADMINS), state='catch_message', text='send_wo_buttons')
async def send_wo_buttons(cq: types.CallbackQuery, state: FSMContext, db: Session):
    data = await state.get_data()
    
    await cq.message.delete()
    await cq.answer('Сообщение в рассылке')
    
    await broadcast(data.get('message'), db)

    await state.reset_state()


@dp.callback_query_handler(IDFilter(ADMINS), state='catch_message', text='send_with_buttons')
async def send_with_buttons(cq: types.CallbackQuery, state: FSMContext):
    await cq.answer('Отправьте кнопки в формате "url - text", каждую с новой строки', show_alert=True)
    await cq.message.delete()
    
    await state.set_state('catch_buttons')


@dp.message_handler(IDFilter(ADMINS), state='catch_buttons')
async def send_with_buttons(message: types.Message, state: FSMContext, db: Session):
    await message.delete()
    
    data = await state.get_data()
    
    keyboard = InlineKeyboardMarkup()
    
    buttons = message.text.split('\n')
    for button in buttons:
        url, *text = button.split(' - ')
        text = ' - '.join(text)
        
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    
    await broadcast(data['message'], db, keyboard=keyboard)
    await state.reset_state()
