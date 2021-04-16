from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import notify


async def on_startup(dispatcher):
    await notify(dispatcher, 'Бот запущен')


async def on_shutdown(dispatcher):
    await notify(dispatcher, 'Бот остановлен')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
