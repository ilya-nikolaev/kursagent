from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.default import menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.delete()
    
    HELLO_TEXT = '\n'.join([
        f'Добро пожаловать в телеграм-бота <b>Курсагент</b>, {message.from_user.first_name}!\n',
        'Этот бот будет присылать вам напоминания о вебинарах '
        'для подготовки к экзаменам или олимпиадам в удобное для вас время!\n',
        'По умолчанию время рассылки настроено на 12:00МСК, но вы можете изменить его ниже. '
        'Чтобы подписаться на рассылку, просто выберите в меню ваши предметы и уровни.\n',
        'Также в меню можно в любой момент посмотреть расписание ваших предметов на сегодня!\n',
        'Приятного использования бота! По всем вопросам, предложениям или замечаниям обращаться к @rnurnu'
    ])
        
    await message.answer(HELLO_TEXT, reply_markup=menu)
