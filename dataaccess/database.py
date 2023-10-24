from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.config import GlobalConfig
from common.singleton import singleton
import sys

@singleton
class DatabaseRepository():
    """
    本地数据库操作
    TODO 之后写错误try
    """
    def __init__(self):
        self.engine = create_engine(GlobalConfig().Database)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def adds(self, entities):
        self.session.add_all(entities)
        self.session.commit()



# 饿汉模式
if not hasattr(sys, 'isInitializedDatabase'):
    database = DatabaseRepository()
