from sqlalchemy import Column, String,TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OptionType(Base):
    __tablename__ = 'OPTION_TYPE'
    name = Column(String,primary_key=True)

class OptionLog(Base):
    __tablename__ = 'OPTION_LOG'
    id = Column(String, primary_key=True)
    time = Column(TIMESTAMP)
    type = Column(String,ForeignKey('OPTION_TYPE.name'))
    content = Column(String)

class ExceptionLog(Base):
    __tablename__ = 'EXCEPTION_LOG'
    id = Column(String, primary_key=True)
    time = Column(TIMESTAMP)
    content = Column(String)

