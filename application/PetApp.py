from domain.service.APIService import APIService
from util.config import GlobalConfig
from util.tools import *
from common.LanguageType import LanguageTypeEnum
from common.AIDrawType import AIDrawStyleEnum,AIDrawRadioEnum
from PyQt6.QtCore import pyqtSignal,QObject

class PetApplication(QObject):
    getInfoFromImageSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.service = APIService()

    def getMusicToFile(self,keyword):
        musicID = self.service.getMusicID(keyword)
        musicURL = self.service.getMusicURL(musicID.id)
        data = downloadURLRes(musicURL.url)
        saveTofile(data,GlobalConfig().TempMusic)

    def getRandomPicToFile(self):
        data = self.service.getRandomPicture()
        saveTofile(data.content,GlobalConfig().TempPic)

    def getWiki(self,keyword) -> str:
        contents = self.service.getWikiSearch(keyword)
        id = contents.contents[0].pageid
        context = self.service.getWikiDetail(id)
        return f"{context.content}"

    def getHistoryOnToday(self) -> (str,str):
        data = self.service.getHistoryOnToday()
        # 随机取一条
        content = chooseRandomElement(data.contents)
        return content.day, content.content

    def getRandomMusic(self) -> (str,str):
        musicData = self.service.getRandomMusic()
        url = self.service.getMusicURL(musicData.id)
        data = downloadURLRes(url.url)
        saveTofile(data,GlobalConfig().TempMusic)
        return musicData.title,musicData.author

    def getTr(self,msg,to) -> str:
        if len(msg) < 5:
            return "文本过短，无法翻译"
        data = self.service.getTr(msg,LanguageTypeEnum(to))
        return data.msg

    def drawAI(self,content,style,radio) -> str:
        url = self.service.getAIDraw(content,AIDrawStyleEnum(style),AIDrawRadioEnum(radio))
        data = downloadURLRes(url.url)
        saveTofile(data,GlobalConfig().TempPic)

    async def getInfoFromImage(self,filePath) -> str:
        data = await self.service.getInfoFromImage(filePath)
        self.getInfoFromImageSignal.emit(f"这是{data.work}的{data.name}")

    def getGPT(self,msg) -> str:
        return self.service.getGPT(msg).ans




