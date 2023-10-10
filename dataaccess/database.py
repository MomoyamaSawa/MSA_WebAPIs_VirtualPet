from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.config import GlobalConfig
from common.singleton import singleton
import sys

@singleton
class DatabaseRepository():
    """
    本地数据库操作
    """
    def __init__(self):
        self.config = GlobalConfig()
        self.engine = create_engine(self.config.Database)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

# 饿汉模式
if not hasattr(sys, 'isInitializedDatabase'):
    database = DatabaseRepository()
