from dataaccess.database import DatabaseRepository
from common.OptionType import OptionTypeEnum
from dataaccess.models import OptionLog
import uuid, time, json, datetime
from util.tools import fromDateTimeToStr


class OptionLogAgg:
    def __init__(self, type: OptionTypeEnum, content: object, _make=True):
        if _make:
            # TODO 这边之后的操作最好也是检查一下 ismake，用装饰器模式吧
            self.type = type
            # TODO 还要检查content能不能拆成对象
            self.content = content
            self.id = uuid.uuid1()
            self.time = datetime.datetime.fromtimestamp(time.time())
            self.isMake = True
        else:
            self.isMake = False

    def writeOptionLog(self):
        """
        写入操作日志
        """
        database = DatabaseRepository()
        optionlog = OptionLog(
            id=str(self.id),
            time=self.time,
            type=self.type.value,
            content=json.dumps(self.content),
        )
        database.add(optionlog)

    def __str__(self) -> str:
        return (
            fromDateTimeToStr(self.time)
            + " "
            + self.type.name
            + " "
            + str(self.content)
        )

    @staticmethod
    def getGptLogs(n):
        """
        获取GPT日志
        """
        database = DatabaseRepository()
        optionlogs = (
            database.session.query(OptionLog)
            .filter(OptionLog.type == OptionTypeEnum.GPT.value)
            .order_by(OptionLog.time.desc())
            .limit(n)
            .all()
        )
        aggs = []
        for item in optionlogs:
            content = json.loads(item.content)
            agg = OptionLogAgg(None, None, False)
            agg.id = item.id
            agg.time = item.time
            agg.type = OptionTypeEnum(item.type)
            agg.content = content
            aggs.append(agg)
        return aggs
