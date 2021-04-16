import logging
import asyncio

from aiogram import Dispatcher

from data.config import ADMINS


async def notify(dp: Dispatcher, msg: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, msg)
            await asyncio.sleep(.25)

        except Exception as err:
            logging.exception(err)
