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


