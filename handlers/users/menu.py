import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.orm import Session

from keyboards.default.menu import SET_LEVELS, SET_SUBJECTS, SET_TIME, GET_TIMETABLE, menu_keyboard
from keyboards.inline import levels_keyboard
from keyboards.inline import subjects_keyboard
from loader import dp
from states.set_time import SetTime
from utils.db_api.models import User

from datetime import datetime, timedelta
from utils.worker import send_mailing


timezone_callback_data = CallbackData('timezone', 'delta')
time_callback_data = CallbackData('time', 'time', sep='-')


@dp.message_handler(text=SET_LEVELS)
async def set_levels(message: types.Message, db: Session, user: User):
    await message.delete()
    
    try:
        keyboard = await levels_keyboard(db, user)
        await message.answer('Выберите варианты из списка ниже', reply_markup=keyboard)
    except LookupError:
        message = await message.answer('Уровней пока что нет')
        await asyncio.sleep(5)
        await message.delete()


@dp.message_handler(text=SET_SUBJECTS)
async def set_subjects(message: types.Message, db: Session, user: User):
    await message.delete()
    
    try:
        keyboard = await subjects_keyboard(db, user)
        await message.answer('Выберите предметы из списка ниже', reply_markup=keyboard)
    except LookupError:
        message = await message.answer('Предметов пока что нет')
        await asyncio.sleep(5)
        await message.delete()


@dp.message_handler(text=GET_TIMETABLE)
async def get_timetable(message: types.Message):
    await message.delete()
    await send_mailing(message.from_user.id)


@dp.callback_query_handler(text='hide')
async def hide(cq: types.CallbackQuery):
    await cq.message.delete()


@dp.message_handler(text=SET_TIME)
async def set_subjects(message: types.Message, state: FSMContext):
    await message.delete()
    
    deltas = ['-1', '0', '+1', '+2', '+4', '+5', '+6', '+7', '+8', '+9']
    
    timezone_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'{deltas[n]}', callback_data=timezone_callback_data.new(delta=deltas[n])),
                InlineKeyboardButton(text=f'{deltas[n + 1]}', callback_data=timezone_callback_data.new(delta=deltas[n + 1]))
            ] for n in range(0, len(deltas), 2)
        ]
    )
    
    await state.set_state(SetTime.zone)
    await message.answer('Укажите ваш часовой пояс <b>относительно Москвы</b>', reply_markup=timezone_keyboard)


@dp.callback_query_handler(timezone_callback_data.filter(), state=SetTime.zone)
async def set_zone(cq: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await cq.answer()

    time_variants = ['07:00', '08:00', '09:00', '10:00', '11:00',
                     '12:00', '13:00', '14:00', '15:00', '16:00']

    time_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'{time_variants[n]}', callback_data=time_callback_data.new(time=time_variants[n])),
                InlineKeyboardButton(text=f'{time_variants[n + 1]}', callback_data=time_callback_data.new(time=time_variants[n + 1]))
            ] for n in range(0, len(time_variants), 2)
        ]
    )
    
    await state.update_data(zone=callback_data['delta'])
    await cq.message.edit_text('Отлично, теперь выберите время в которое хотите получать уведомления из списка ниже',
                               reply_markup=time_keyboard)
    await state.set_state(SetTime.time)


@dp.callback_query_handler(time_callback_data.filter(), state=SetTime.time)
async def set_time(cq: types.CallbackQuery, state: FSMContext, user: User, db: Session, callback_data: dict):
    user_time = datetime.strptime(callback_data["time"], '%H:%M')

    state_data = await state.get_data()
    zone = state_data['zone']
    delta = timedelta(hours=int(zone))
    
    user_msk_time = user_time - delta
    
    user.mailing_time = f'{user_msk_time.hour}:00'
    db.commit()
    
    await state.reset_state()
    await cq.answer(text=f'Отлично! Время рассылки изменено на {user_time.hour}:00')
    await cq.message.delete()
