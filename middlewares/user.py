from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api.models import User


class UserMiddleware(BaseMiddleware):
    # noinspection PyMethodMayBeStatic
    async def on_process_message(self, message: types.Message, data: dict):
        user = data['db'].query(User).filter(User.user_id == message.from_user.id).first()
        
        if user is None:
            user = User(user_id=message.from_user.id, user_name=message.from_user.username)
        
            data['db'].add(user)
            data['db'].commit()
        
        data['user'] = user

    # noinspection PyMethodMayBeStatic
    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user = data['db'].query(User).filter(User.user_id == cq.from_user.id).first()
        
        if user is None:
            user = User(user_id=cq.from_user.id, user_name=cq.from_user.username)
        
            data['db'].add(user)
            data['db'].commit()
        
        data['user'] = user
