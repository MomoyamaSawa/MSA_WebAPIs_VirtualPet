from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.config import GlobalConfig
from dataaccess.models import *

def createDatabase():
    # 创建数据库引擎和会话
    engine = create_engine(GlobalConfig().Database)
    Session = sessionmaker(bind=engine)
    session = Session()

    # # 定义数据模型
    # Base = declarative_base()

    # class MyTable(Base):
    #     __tablename__ = 'test'
    #     id = Column(Integer, primary_key=True)
    #     column1 = Column(String)
    #     column2 = Column(Integer)

    # 创建表格
    Base.metadata.create_all(engine)

    # 插入数据
    data1 = OptionType(name="gpt")

    session.add_all([data1])
    session.commit()

    # # 查询数据
    # query = session.query(MyTable).all()
    # for data in query:
    #     print(data.column1, data.column2)

    # 关闭会话
    session.close()
