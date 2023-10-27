from domain.service.APIService import APIService
from domain.service.PetService import PetService
from util.config import GlobalConfig
from util.tools import *
from common.LanguageType import LanguageTypeEnum
from common.AIDrawType import *
from PyQt6.QtCore import pyqtSignal,QObject
from do.APIDto import *
from common.weekdayType import WeekDayEnumArr
from common.OptionType import OptionTypeEnum
import os

class PetApplication(QObject):
    getInfoFromImageSignal = pyqtSignal(str)
    singleSentanceSignal = pyqtSignal(str)
    wheatherSignal = pyqtSignal(str)
    gptSignal = pyqtSignal(str)
    musicToFileSignal = pyqtSignal(str)
    randomMusicSiganl = pyqtSignal(str,str)
    randomPicSignal = pyqtSignal()
    drawAISiganl = pyqtSignal()
    trSignal = pyqtSignal(str)
    searchWikiSignal = pyqtSignal(list)
    wikiSignal = pyqtSignal(str)
    historyTodaySignal = pyqtSignal(str)
    musicListSignal = pyqtSignal(list)
    badSignal = pyqtSignal()
    restartSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.service = APIService()
        self.petService = PetService()

    def getMusicList(self,keyword):
        try:
            list = self.service.getMusicList(keyword)
            self.musicListSignal.emit(list)
            info = self.petService.writeMusicSearchLog(keyword)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.MUSIC)

    def getMusicToFile(self,id,content):
        try:
            musicURL = self.service.getMusicURL(id)
            data = downloadURLRes(musicURL)
            saveTofile(data,GlobalConfig().TempMusic)
            self.musicToFileSignal.emit(content)
            info = self.petService.writeMusicLog(content)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.MUSIC)

    def getRandomPicToFile(self):
        try:
            url,data = self.service.getRandomPicture()
            saveTofile(data,GlobalConfig().TempPic)
            self.randomPicSignal.emit()
            info = self.petService.writeRandomPicLog(url)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.RANDOM_PIC)

    def searchWiki(self,keyword):
        try:
            contents = self.service.getWikiSearch(keyword)
            self.searchWikiSignal.emit(contents.contents)
            info = self.petService.writeWikiSearchLog(keyword)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.WIKI)

    def getWikiDetail(self,id):
        try:
            context = self.service.getWikiDetail(id)
            self.wikiSignal.emit(context.content)
            info = self.petService.writeWikiLog(id,context.title,context.content)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.WIKI)

    def getHistoryOnToday(self):
        try:
            data = self.service.getHistoryOnToday()
            # 随机取一条
            content = chooseRandomElement(data.contents)
            self.historyTodaySignal.emit(f"{content.day}: {content.content}")
            info = self.petService.writeHistoryLog(content.day,content.content)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.HISTORY)

    def getRandomMusic(self):
        try:
            musicData = self.service.getRandomMusic()
            url = self.service.getMusicURL(musicData.id)
            data = downloadURLRes(url)
            saveTofile(data,GlobalConfig().TempMusic)
            self.randomMusicSiganl.emit(musicData.title,musicData.author)
            info = self.petService.writeRandomMusicLog(musicData.title,musicData.author)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.RANDOM_MUSIC)

    def getTr(self,msg,to):
        try:
            if len(msg) < 5:
                return "文本过短，无法翻译"
            ans = self.service.getTr(msg,LanguageTypeEnum(to))
            self.trSignal.emit(ans)
            info = self.petService.writeTrLog(msg,ans,to)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.TR)

    def drawAI(self,content,style,radio):
        try:
            url = self.service.getAIDraw(content,AIDrawStyleEnum(style),AIDrawRatioEnum(radio))
            data = downloadURLRes(url)
            saveTofile(data,GlobalConfig().TempPic)
            self.drawAISiganl.emit()
            info = self.petService.writeAIDrawLog(content,style,radio,url)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.AI_DRAW)

    def getInfoFromImage(self,filePath):
        try:
            if not os.path.exists(filePath):
                self.badSignal.emit()
                return
            name,work = self.service.getInfoFromImage(filePath)
            self.getInfoFromImageSignal.emit(f"这是{work}的{name}")
            log = self.petService.writeInfoFromImageLog(filePath,name,work)
            self.infoSolve(log)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.INFO_FROM_IMAGE)

    def getGPT(self,msg) -> str:
        try:
            # 得到之前的n个前置
            logs = self.petService.getGPTLogs(GlobalConfig().WebAPI["GPT"]["Num"])
            ans =  self.service.getGPT(msg,logs)
            self.gptSignal.emit(ans)
            info = self.petService.writeGPTLog(msg,ans)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.GPT)

    def getSingle(self):
        try:
            dto = self.service.getSingleSentance()
            if dto.who:
                self.singleSentanceSignal.emit(f"{dto.content}        ----{dto.where}（{dto.who}）")
            else:
                self.singleSentanceSignal.emit(f"{dto.content}        ----{dto.where}")
            info = self.petService.writeSingleLog(dto.content,dto.where,dto.who)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.SINGLE)

    def getTimeAndWeather(self):
        try:
            # TODO 这边是直接获取本地时间了，有精力再改改把
            timeDTO = self.service.getTime()
            wheatherDTO = self.service.getWeather()
            self.wheatherSignal.emit(f"今天是{timeDTO.year}年{timeDTO.month}月{timeDTO.day}日{WeekDayEnumArr[int(timeDTO.weekDay)]}，天气为{wheatherDTO.weather}，温度{wheatherDTO.temperature}℃，湿度{wheatherDTO.humidity}%，风速{wheatherDTO.windPower}m/s")
            info = self.petService.writeTimeAndWeatherLog(timeDTO.year,timeDTO.month,timeDTO.day,WeekDayEnumArr[int(timeDTO.weekDay)],wheatherDTO.weather,wheatherDTO.temperature,wheatherDTO.humidity,wheatherDTO.windPower)
            self.infoSolve(info)
        except Exception as e:
            self.exceptionSolve(e,OptionTypeEnum.TIME_AND_WEATHER)

    def exceptionSolve(self,e,type:OptionTypeEnum):
        err = type.value+": " + e.__class__.__name__ +" "+ str(e)
        print(cmdErrStr(err))
        self.petService.writeExceptionLog(err)
        self.restartSignal.emit()

    def infoSolve(self,info):
        print(cmdInfoStr(info))
