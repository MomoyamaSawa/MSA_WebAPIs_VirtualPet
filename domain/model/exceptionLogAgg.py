from dataaccess.database import DatabaseRepository
from dataaccess.models import ExceptionLog
import uuid,time,datetime

class ExceptionLogAgg():
    def __init__(self,content:str,_make=True):
        if(_make):
            self.content = content
            self.id = uuid.uuid1()
            self.time =  datetime.datetime.fromtimestamp(time.time())
            self.isMake = True
        else:
            self.isMake = False

    def writeExceptionLog(self):
        """
        写入操作日志
        """
        database = DatabaseRepository()
        log = ExceptionLog(id=str(self.id),time=self.time,content=self.content)
        database.add(log)


