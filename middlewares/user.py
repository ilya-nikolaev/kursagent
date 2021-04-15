from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api.models import User


class UserMiddleware(BaseMiddleware):
    # noinspection PyMethodMayBeStatic
    async def on_process_message(self, message: types.Message, data: dict):
        data['user'] = data['db'].query(User).filter(User.user_id == message.from_user.id).first()

    # noinspection PyMethodMayBeStatic
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        data['user'] = data['db'].query(User).filter(User.user_id == cq.from_user.id).first()
