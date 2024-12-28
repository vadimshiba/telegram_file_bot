from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    command_id = Column(String, unique=True)
    files = relationship('File', back_populates='command')

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_id = Column(String, unique=True)
    command_id = Column(Integer, ForeignKey('commands.id'))
    command = relationship('Command', back_populates='files')

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)

# Создаем базу данных
engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
