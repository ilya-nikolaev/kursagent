import asyncio
from utils.worker import db_worker, send_mailing
from loader import loop


if __name__ == '__main__':
    loop.run_until_complete(send_mailing(289330540))
