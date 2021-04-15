from sqlalchemy import Table, Column, TEXT, INTEGER, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from data.config import DB_IP, DB_NAME, DB_PASS, DB_USER
# engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_IP}/{DB_NAME}")

engine = create_engine(f"sqlite:///db.db")
pool = sessionmaker(bind=engine)
Base = declarative_base()


user_level = Table(
    'user_level', Base.metadata,
    Column('user_id', INTEGER, ForeignKey('users.id')),
    Column('level_id', INTEGER, ForeignKey('levels.id'))
)

user_subject = Table(
    'user_subject', Base.metadata,
    Column('user_id', INTEGER, ForeignKey('users.id')),
    Column('subject_id', INTEGER, ForeignKey('subjects.id'))
)

event_level = Table(
    'event_level', Base.metadata,
    Column('event_id', INTEGER, ForeignKey('events.id')),
    Column('level_id', INTEGER, ForeignKey('levels.id'))
)

event_subject = Table(
    'event_subject', Base.metadata,
    Column('event_id', INTEGER, ForeignKey('users.id')),
    Column('subject_id', INTEGER, ForeignKey('subjects.id'))
)


class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(INTEGER, primary_key=True)  # BIGINT
    
    user_id: int = Column(INTEGER, nullable=False, unique=True)  # BIGINT
    
    user_name: str = Column(TEXT, nullable=False, unique=True)  # TEXT
    
    banned: int = Column(INTEGER, nullable=False, default=0)  # BOOLEAN


class Event(Base):
    __tablename__ = 'events'
    
    id: int = Column(INTEGER, primary_key=True)  # BIGINT
    
    title: str = Column(TEXT, nullable=False)  # TEXT
    subtitle: str = Column(TEXT, nullable=False)  # TEXT
    
    date: str = Column(TEXT, nullable=False)  # TEXT
    time: str = Column(TEXT, nullable=False)  # TEXT
    
    url: str = Column(TEXT, nullable=False)  # TEXT


class Level(Base):
    __tablename__ = 'levels'
    
    id: int = Column(INTEGER, primary_key=True)  # BIGINT
    
    name: str = Column(TEXT, nullable=False, unique=True)  # TEXT


class Subject(Base):
    __tablename__ = 'subjects'
    
    id: int = Column(INTEGER, primary_key=True)  # BIGINT
    
    name: str = Column(TEXT, nullable=False, unique=True)  # TEXT


Base.metadata.create_all(engine)
