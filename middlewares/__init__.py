from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .banned import BannedMiddleware
from .user import UserMiddleware
from .get_db import DBMiddleware

from utils.db_api import pool

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(DBMiddleware(pool))
    dp.middleware.setup(UserMiddleware())
    dp.middleware.setup(BannedMiddleware())
