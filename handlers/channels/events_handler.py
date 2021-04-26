import logging

from sqlalchemy.orm import Session

from loader import dp
from aiogram import types

from utils.db_api.models import Event, Subject, Level


@dp.channel_post_handler()
async def get_event(message: types.Message, db: Session):
    fields = dict()
    
    for line in message.text.split('\n'):
        key = line.split(':')[0]
        val = ':'.join(line.split(':')[1:])
        
        fields[key] = val
        
    logging.info(f'Принят пост "{fields["post_title"]}"')
    
    event = Event(
        title=fields['post_title'],
        subtitle=fields['subtitle'],
        date=fields['date'],
        time=fields['time'],
        url=fields['url']
    )
    
    subjects = fields['event_type'].split(' ')
    levels = fields['event_type_2'].split(' ')
    
    for subject in subjects:
        obj = db.query(Subject).filter(Subject.name == subject.lstrip('#')).first()
        
        if obj is None:
            obj = Subject(name=subject.lstrip('#'))
            
            db.add(obj)
            db.commit()
        
        event.subjects.append(obj)
    
    for level in levels:
        obj = db.query(Level).filter(Level.name == level.lstrip('#')).first()

        if obj is None:
            obj = Level(name=level.lstrip('#'))
    
            db.add(obj)
            db.commit()
        
        event.levels.append(obj)
    
    db.add(event)
    db.commit()

    logging.info(f'Пост "{fields["post_title"]}" успешно загружен в БД')
