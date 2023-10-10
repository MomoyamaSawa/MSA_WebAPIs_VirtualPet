from util.config import GlobalConfig
from datetime import datetime
from do.dto.APIDto import TimeDto,WeatherDto
import requests
from exception import WebAPIException

class APIService:
    """
    提供调用各种 web/sys API 的服务
    """
    def __init__(self):
        self.config = GlobalConfig()

    def getTime(self) -> TimeDto:
        """
        获得日期时间
        """
        currentTime = datetime.now()
        return TimeDto(currentTime.year, currentTime.month, currentTime.day, currentTime.hour, currentTime.weekday())

    def getWeather(self) -> WeatherDto:
        """
        获得天气
        """
        url = self.config.WebAPI["Weather"]["URL"]
        params = self.config.WebAPI["Weather"]["Params"]
        response = requests.get(url, params=params)
        data = response.json()
        if (response.status_code != 200 | data['status'] != 0 | data['infocode'] != '10000'):
            raise WebAPIException(response.status_code, response.text)
        return WeatherDto(data['lives'][0]['weather'], data['lives'][0]['temperature'], data['lives'][0]['winddirection'], data['lives'][0]['windpower'], data['lives'][0]['humidity'], data['lives'][0]['reporttime'])
