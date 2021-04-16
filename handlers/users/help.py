from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from keyboards.default import GET_HELP


@dp.message_handler(text=GET_HELP)
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))
