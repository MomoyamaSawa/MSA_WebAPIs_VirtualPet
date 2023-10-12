from io import BytesIO

class WeatherDto():
    """
    天气信息的dto
    """
    def __init__(self,province,city,weather,temperature,windDirection,windPower,humidity,reportTime):
        self.province = province
        self.city = city
        self.weather = weather
        self.temperature = temperature
        self.windDirection = windDirection
        self.windPower = windPower
        self.humidity = humidity
        self.reportTime = reportTime

class TimeDto():
    """
    日期时间的dto
    """

    def __init__(self, year, month, day, hour, weekDay):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.weekDay = weekDay


class MusicDataDto():
    """
    音乐数据的dto
    """
    def __init__(self,name,type,content):
        self.name = name
        self.type = type
        self.content:BytesIO = content

class PictureDataDto():
    """
    图片数据的dto
    """
    def __init__(self,content):
        self.content:BytesIO = content

class SentanceDataDto():
    """
    句子数据的dto
    """
    def __init__(self,where,who,content):
        self.where = where
        self.who = who
        self.content = content
