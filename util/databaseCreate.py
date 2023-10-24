from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.config import GlobalConfig
from dataaccess.models import *
from common.OptionType import OptionTypeEnum
import os

def checkDatabase():
    path = GlobalConfig().Database
    # 提取文件路径
    fileDir = path.replace("sqlite:///", "")
    # 检查文件是否存在
    if not os.path.exists(fileDir):

        # 创建数据库引擎和会话
        engine = create_engine(path)
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
        datas = []

        # 遍历枚举类型的所有值
        for option in OptionTypeEnum.__members__.values():
            datas.append(OptionType(name=option.value))


        session.add_all(datas)
        session.commit()

        # # 查询数据
        # query = session.query(MyTable).all()
        # for data in query:
        #     print(data.column1, data.column2)

        # 关闭会话
        session.close()
