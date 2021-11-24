import asyncio
import logging

from sqlalchemy import false, true
from sqlalchemy.orm import Session

from loader import dp

from .db_api import pool
from .db_api.models import Event, User
from keyboards.inline import get_mailing_keyboard
from data.config import WEB_TEMPLATE
from datetime import datetime


async def send_mailing(user_id: int, individual: bool = False):
    db = pool()
    user = db.query(User).filter(User.user_id == user_id).first()
    
    date = datetime.now().strftime('%d.%m.%Y')
    
    user_events: list[Event] = list()
    for event in db.query(Event).all():
        if event.date != date:
            continue
        if not any([level in event.levels for level in user.levels]):
            continue
        if not any([subject in event.subjects for subject in user.subjects]):
            continue
        
        user_events.append(event)
    
    user_events.sort(key=lambda x: x.featured, reverse=True)
    
    message = list()
    for user_event in user_events:
        subjects_string = ['#' + subject.name for subject in user_event.subjects]
        levels_string = ['#' + level.name for level in user_event.levels]
        base = WEB_TEMPLATE.format(
            title=user_event.title,
            subjects=' '.join(subjects_string),
            levels=' '.join(levels_string),
            date=user_event.date,
            time=user_event.time.split()[0],
            subtitle=user_event.subtitle,
            url=user_event.url
        )
        
        if user_event.featured:
            base = '⚡️ <b>Событие дня!</b> ⚡️\n' + base
        
        message.append(base)
    
    db.close()

    keyboard = get_mailing_keyboard(user)
    
    try:
        if not message and individual:
            await dp.bot.send_message(user_id, "К сожалению, на сегодня ничего нет")
            raise Exception

        await dp.bot.send_message(user_id, '\n'.join(message), disable_web_page_preview=True, reply_markup=keyboard)
        logging.info(f'Отправлено сообщение пользователю {user_id}')
    except Exception as e:
        logging.warning(f'Сообщение пользователю {user_id} не отправлено')
        print(e)


async def db_worker():
    logging.info('Идет работа с базой данных...')
    db: Session = pool()
    
    for event in db.query(Event).all():
        delta = datetime.now().date() - datetime.strptime(event.date, "%d.%m.%Y").date()
        
        if delta.days > 1:
            logging.info(f'Удалено событие {event.title}')
            db.delete(event)
            db.commit()
            continue
    
    hour = datetime.now().hour
    for user in db.query(User).filter(User.banned == false(), User.subscribed == true()).all():
        if user.mailing_time == f'{hour}:00':
            await send_mailing(user.user_id)
            await asyncio.sleep(.5)
    
    db.close()
