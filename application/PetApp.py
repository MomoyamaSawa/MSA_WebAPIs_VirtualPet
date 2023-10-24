from domain.service.APIService import APIService
from domain.service.PetService import PetService
from util.config import GlobalConfig
from util.tools import *
from common.LanguageType import LanguageTypeEnum
from common.AIDrawType import *
from PyQt6.QtCore import pyqtSignal,QObject
from do.dto.APIDto import *
from common.weekdayType import WeekDayEnumArr

class PetApplication(QObject):
    getInfoFromImageSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.service = APIService()
        self.petService = PetService()

    def getMusicToFile(self,keyword):
        # TODO 模糊搜索面板
        musicID,name = self.service.getMusicID(keyword)
        musicURL = self.service.getMusicURL(musicID)
        data = downloadURLRes(musicURL)
        saveTofile(data,GlobalConfig().TempMusic)
        self.petService.writeMusicLog(keyword,name)

    def getRandomPicToFile(self):
        url,data = self.service.getRandomPicture()
        saveTofile(data,GlobalConfig().TempPic)
        self.petService.writeRandomPicLog(url)

    def getWiki(self,keyword) -> str:
        contents = self.service.getWikiSearch(keyword)
        id = contents.contents[0].pageid
        context = self.service.getWikiDetail(id)
        self.petService.writeWikiLog(keyword,context.title,context.content)
        return f"{context.content}"

    def getHistoryOnToday(self) -> (str,str):
        data = self.service.getHistoryOnToday()
        # 随机取一条
        content = chooseRandomElement(data.contents)
        self.petService.writeHistoryLog(content.day,content.content)
        return content.day, content.content

    def getRandomMusic(self) -> (str,str):
        musicData = self.service.getRandomMusic()
        url = self.service.getMusicURL(musicData.id)
        data = downloadURLRes(url)
        saveTofile(data,GlobalConfig().TempMusic)
        self.petService.writeRandomMusicLog(musicData.title,musicData.author)
        return musicData.title,musicData.author

    def getTr(self,msg,to) -> str:
        if len(msg) < 5:
            return "文本过短，无法翻译"
        ans = self.service.getTr(msg,LanguageTypeEnum(to))
        self.petService.writeTrLog(msg,ans,to)
        return ans

    def drawAI(self,content,style,radio) -> str:
        url = self.service.getAIDraw(content,AIDrawStyleEnum(style),AIDrawRatioEnum(radio))
        data = downloadURLRes(url)
        saveTofile(data,GlobalConfig().TempPic)
        self.petService.writeAIDrawLog(content,style,radio,url)

    async def getInfoFromImage(self,filePath) -> str:
        name,work = await self.service.getInfoFromImage(filePath)
        self.getInfoFromImageSignal.emit(f"这是{work}的{name}")
        self.petService.writeInfoFromImageLog(filePath,name,work)

    def getGPT(self,msg) -> str:
        # 得到之前的n个前置
        logs = self.petService.getGPTLogs(GlobalConfig().WebAPI["GPT"]["Num"])
        ans =  self.service.getGPT(msg,logs)
        # 要存到数据库里
        self.petService.writeGPTLog(msg,ans)
        return ans

    def getSingle(self)->str:
        dto = self.service.getSingleSentance()
        return f"FROM {dto.where}({dto.who}): {dto.content}"

    def getTimeAndWeather(self) -> str:
        timeDTO = self.service.getTime()
        wheatherDTO = self.service.getWeather()
        return f"今天是{timeDTO.year}年{timeDTO.month}月{timeDTO.day}日{WeekDayEnumArr[int(timeDTO.weekDay)]}，天气为{wheatherDTO.weather}，温度{wheatherDTO.temperature}℃，湿度{wheatherDTO.humidity}%，风速{wheatherDTO.windPower}m/s"

