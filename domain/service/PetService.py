from domain.model.optionLogAgg import OptionLogAgg
from domain.model.exceptionLogAgg import ExceptionLogAgg
from common.OptionType import OptionTypeEnum
from do.PetDto import *
from util.tools import fromDateTimeToStr

class PetService():
    def __init__(self):
        pass

    def writeGPTLog(self,q,a):
        """
        写入GPT日志
        """
        gptLog = {
            "question":q,
            "ans":a
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.GPT,gptLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def getGPTLogs(self,n) -> list[GptLogItem]:
        """
        获取GPT日志
        """
        aggs = OptionLogAgg.getGptLogs(n)
        logs = []
        for agg in aggs:
            dt = fromDateTimeToStr(agg.time)
            log = GptLogItem(agg.content["question"],agg.content["ans"],dt)
            logs.append(log)
        return list(reversed(logs))

    def writeMusicLog(self,content):
        musicLog = {
            "info":content,
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.MUSIC,musicLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeRandomMusicLog(self,title,author):
        musicLog = {
            "title":title,
            "author":author
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.RANDOM_MUSIC,musicLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeRandomPicLog(self,url):
        picLog = {
            "url":url
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.RANDOM_PIC,picLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeInfoFromImageLog(self,path,name,work):
        infoLog = {
            "path":path,
            "name":name,
            "work":work
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.INFO_FROM_IMAGE,infoLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeAIDrawLog(self,content,style,radio,url):
        aiDrawLog = {
            "content":content,
            "style":style,
            "radio":radio,
            "url":url
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.AI_DRAW,aiDrawLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeTrLog(self,msg,ans,to):
        trLog = {
            "msg":msg,
            "ans":ans,
            "to":to
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.TR,trLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeWikiLog(self,keyword,title,content):
        wikiLog = {
            "keyword":keyword,
            "title":title,
            "content":content
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.WIKI,wikiLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeHistoryLog(self,day,content):
        historyLog = {
            "day":day,
            "content":content
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.HISTORY,historyLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeExceptionLog(self,exception):
        optionLogAgg = ExceptionLogAgg(exception)
        optionLogAgg.writeExceptionLog()

    def writeSingleLog(self,content,where,who):
        singleLog = {
            "content":content,
            "where":where,
            "who":who
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.SINGLE,singleLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeTimeAndWeatherLog(self,year,month,day,weekday,weather,temp,humidity,windPower):
        timeAndWeatherLog = {
            "year":year,
            "month":month,
            "day":day,
            "weekday":weekday,
            "weather":weather,
            "temp":temp,
            "humidity":humidity,
            "windPower":windPower
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.TIME_AND_WEATHER,timeAndWeatherLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeMusicSearchLog(self,keyword):
        musicListLog = {
            "keyword":keyword
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.MUSIC_LIST,musicListLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)

    def writeWikiSearchLog(self,keyword):
        wikiListLog = {
            "keyword":keyword
        }
        optionLogAgg = OptionLogAgg(OptionTypeEnum.WIKI_LIST,wikiListLog)
        optionLogAgg.writeOptionLog()
        return str(optionLogAgg)
