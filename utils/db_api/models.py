from sqlalchemy import Table, Column, TEXT, ForeignKey, create_engine, BIGINT, BOOLEAN, false, true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from data.config import DB_IP, DB_NAME, DB_PASS, DB_USER
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_IP}/{DB_NAME}")
pool = sessionmaker(bind=engine)
Base = declarative_base()

user_level = Table(
    'user_level', Base.metadata,
    Column('user_id', BIGINT, ForeignKey('users.id')),
    Column('level_id', BIGINT, ForeignKey('levels.id'))
)

user_subject = Table(
    'user_subject', Base.metadata,
    Column('user_id', BIGINT, ForeignKey('users.id')),
    Column('subject_id', BIGINT, ForeignKey('subjects.id'))
)

event_level = Table(
    'event_level', Base.metadata,
    Column('event_id', BIGINT, ForeignKey('events.id')),
    Column('level_id', BIGINT, ForeignKey('levels.id'))
)

event_subject = Table(
    'event_subject', Base.metadata,
    Column('event_id', BIGINT, ForeignKey('events.id')),
    Column('subject_id', BIGINT, ForeignKey('subjects.id'))
)


class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(BIGINT, primary_key=True)  # BIGINT
    
    user_id: int = Column(BIGINT, nullable=False, unique=True)  # BIGINT
    
    user_name: str = Column(TEXT, unique=True, nullable=True)
    mailing_time: str = Column(TEXT, default='12:00')
    
    banned: int = Column(BOOLEAN, nullable=False, default=false())
    subscribed: int = Column(BOOLEAN, nullable=False, default=true())
    
    subjects = relationship('Subject', secondary=user_subject, backref='users')
    levels = relationship('Level', secondary=user_level, backref='users')
    
    def __repr__(self):
        return f'DB_ID: {self.id}. TG: ({self.user_id}, {self.user_name}). Banned {self.banned}'


class Event(Base):
    __tablename__ = 'events'
    
    id: int = Column(BIGINT, primary_key=True)
    
    title: str = Column(TEXT, nullable=False)
    subtitle: str = Column(TEXT, nullable=False)
    
    date: str = Column(TEXT, nullable=False)
    time: str = Column(TEXT, nullable=False)
    
    url: str = Column(TEXT, nullable=False)
    
    featured: bool = Column(BOOLEAN, nullable=True)

    subjects = relationship('Subject', secondary=event_subject, backref='events')
    levels = relationship('Level', secondary=event_level, backref='events')
    
    def __repr__(self):
        return f'{self.title} - {self.date} {self.time}'


class Level(Base):
    __tablename__ = 'levels'
    
    id: int = Column(BIGINT, primary_key=True)  # BIGINT
    
    name: str = Column(TEXT, nullable=False, unique=True)  # TEXT
    
    def __repr__(self):
        return f'{self.id}: {self.name}'


class Subject(Base):
    __tablename__ = 'subjects'
    
    id: int = Column(BIGINT, primary_key=True)  # BIGINT
    
    name: str = Column(TEXT, nullable=False, unique=True)  # TEXT
    
    def __repr__(self):
        return f'{self.id}: {self.name}'


Base.metadata.create_all(engine)
