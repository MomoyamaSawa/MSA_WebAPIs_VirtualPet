from io import BytesIO

class KeyWordDto():
    """
    关键词的dto
    """
    def __init__(self,keyword):
        self.keyword = keyword

class WeatherDto():
    """
    天气信息的dto
    """
    def __init__(self,weather,temperature,windDirection,windPower,humidity,reportTime):
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
        self.content:bytes = content

class SentanceDataDto():
    """
    句子数据的dto
    """
    def __init__(self,where,who,content):
        self.where = where
        self.who = who
        self.content = content

class HistoryOnTodayItem():
    """
    历史上的今天的item
    """
    def __init__(self,day,content):
        self.day = day
        self.content = content

class HistoryOnTodayDto():
    """
    历史上的今天的dto
    """
    def __init__(self,day,contents:list[HistoryOnTodayItem]):
        self.day = day
        self.contents = contents

class InfoFromImageDto():
    """
    从图片中提取的信息的dto
    """
    def __init__(self,name,work):
        self.name = name
        self.work = work

class RandomMusicDto():
    """
    随机音乐的dto
    """
    def __init__(self,id,title,author,cover):
        self.id = id
        self.title = title
        self.author = author
        self.cover = cover

class TrDto():
    """
    翻译的dto
    """
    def __init__(self,msg):
        self.msg = msg

class WikiSearchItem():
    """
    wiki模糊搜索的item
    """
    def __init__(self,title,pageid,snippet):
        self.title = title
        self.pageid = pageid
        self.snippet = snippet

class WikiSearchDto():
    """
    wiki模糊搜索的dto
    """
    def __init__(self,contents:list[WikiSearchItem]):
        self.contents = contents

class WikiDetailDto():
    """
    wiki详情的dto
    """
    def __init__(self,title,content):
        self.title = title
        self.content = content

class SearchImagesItem():
    """
    搜索图片的item
    """
    def __init__(self,id,title,username,url,caption):
        self.title = title
        self.username = username
        self.id= id
        self.imgURL = url
        self.caption = caption

class SearchImagesDto():
    """
    搜索图片的dto
    """
    def __init__(self,contents:list[SearchImagesItem],nextPageURL):
        self.contents = contents
        self.nextPageURL = nextPageURL

class AIDrawDto():
    """
    AI画画的dto
    """
    def __init__(self,url):
        self.url = url

class MusicListItemDto():
    def __init__(self,id,name,author):
        self.id = id
        self.name = name
        self.author = author
