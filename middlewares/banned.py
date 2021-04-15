from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api.models import User


class BannedMiddleware(BaseMiddleware):
    # noinspection PyMethodMayBeStatic
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            if data['db'].query(User.banned).filter(User.user_id == message.from_user.id).first()[0]:
                raise CancelHandler()
        except TypeError:
            pass

    # noinspection PyMethodMayBeStatic
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        try:
            if data['db'].query(User.banned).filter(User.user_id == cq.from_user.id).first()[0]:
                raise CancelHandler()
        except TypeError:
            pass
