import asyncio
from aiogram import executor

# noinspection PyUnresolvedReferences
import filters
# noinspection PyUnresolvedReferences
import handlers
# noinspection PyUnresolvedReferences
import middlewares
from loader import dp, scheduler
from utils.notify_admins import notify

from utils.worker import db_worker


async def job():
    scheduler.add_job(db_worker, 'cron', minute=0)


async def on_startup(dispatcher):
    await notify(dispatcher, 'Бот запущен')
    await asyncio.create_task(job())


async def on_shutdown(dispatcher):
    await notify(dispatcher, 'Бот остановлен')


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
