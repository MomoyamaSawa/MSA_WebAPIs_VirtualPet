from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from dataaccess.database import DatabaseRepository

Base = declarative_base()
database = DatabaseRepository()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# 创建表格
Base.metadata.create_all(database.engine)
