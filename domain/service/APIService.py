from util.config import GlobalConfig
from datetime import datetime
from do.dto.APIDto import *
import requests,io,httpx,json
from exception import WebAPIException
from common.LanguageType import LanguageTypeEnum

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
        url = self.config.WebAPI["GetWeather"]["URL"]
        params = self.config.WebAPI["GetWeather"]["Params"]
        response = requests.get(url, params=params)
        data = response.json()
        if (response.status_code != 200 | data['status'] != 0 | data['infocode'] != '10000'):
            raise WebAPIException(response.status_code, response.text)
        return WeatherDto(data['lives'][0]['weather'], data['lives'][0]['temperature'], data['lives'][0]['winddirection'], data['lives'][0]['windpower'], data['lives'][0]['humidity'], data['lives'][0]['reporttime'])

    def getMusicData(self,keyword) -> MusicDataDto:
        """
        取得一首歌的下载 url
        TODO 暂未测试无版权的时候是否可用，这边之后拆一下
        """
        searchURL = self.config.WebAPI["Music"]["Search"]["URL"]
        searchParams = self.config.WebAPI["Music"]["Search"]["Params"]
        searchParams['keywords'] = keyword
        response = requests.get(searchURL, params=searchParams)
        data = response.json()
        if (response.status_code != 200):
            raise WebAPIException(response.status_code, response.text)
        musicID = data['result']['songs'][0]['id']

        getURL = self.config.WebAPI["Music"]["Get"]["URL"]
        getParams = self.config.WebAPI["Music"]["Get"]["Params"]
        getParams['id'] = musicID
        response = requests.get(getURL, params=getParams)
        data = response.json()
        if (response.status_code != 200):
            raise WebAPIException(response.status_code, response.text)
        musicURL = data['data'][0]['url']
        audioType = data['data'][0]['type']

        # 下载音频文件
        response = requests.get(musicURL)
        if (response.status_code != 200):
            raise WebAPIException(response.status_code, response.text)
        musicURL = data['data'][0]['url']
        audioContent = io.BytesIO(response.content)

        return MusicDataDto(audioType,audioContent)
        # INFO 使用例
        # a = test()
        # data = a.getMusicData("neo")

        # audio = AudioSegment.from_file(data.content, format=data.type)
        # play(audio)

    def getRandomPicture(self) -> PictureDataDto:
        """
        获得随机图片的数据
        """
        url = self.config.WebAPI["Picture"]["URL"]
        response = requests.get(url)
        return PictureDataDto(io.BytesIO(response.content))
        # INFO 使用例
        # url = GlobalConfig().WebAPI["Picture"]["URL"]
        # response = requests.get(url)
        # image_data = response.content
        # # 使用PIL库加载二进制数据为图像
        # image = Image.open(io.BytesIO(image_data))

        # # 显示图像
        # image.show()

    def getSingleSentance(self) -> SentanceDataDto:
        """
        获得随机的语句
        TODO 之后可以扩充一下参数。我看那个参数蛮多的
        """
        url = self.config.WebAPI["Sentance"]["URL"]
        response = requests.get(url)
        data = response.json()
        return SentanceDataDto(data['from'], data['from_who'], data['hitokoto'])

    def getSearchImages(self,keyword):
        """
        获得搜索图片
        BUG 还未写好
        """
        url = self.config.WebAPI["Image"]["Search"]["URL"]
        params = self.config.WebAPI["Image"]["Search"]["Params"]
        params['q'] = keyword
        response = requests.get(url, params=params)
        data = response.json()
        data = data.illusts
        results = []

        # 遍历前五个元素
        num = self.config.WebAPI["Image"]["Search"]["Num"]
        for item in data[:num]:
            title = item["title"]
            username = item["user"]["name"]
            item_id = item["id"]

            if "meta_single_page" in item and "original_image_url" in item["meta_single_page"]:
                image_url = item["meta_single_page"]["original_image_url"]
            elif "meta_pages" in item and item["meta_pages"]:
                image_url = item["meta_pages"][0]
            else:
                image_url = None

            # 创建包含所需字段的字典
            result = {
                "title": title,
                "username": username,
                "id": item_id,
                "image_url": image_url
            }

            # 将字典添加到结果列表中
            results.append(result)

        return results

    def getHistoryOnToday(self) -> HistoryOnTodayDto:
        """
        获得历史上的今天
        """
        url = self.config.WebAPI["History"]["URL"]
        response = requests.get(url)
        if (response.status_code != 200):
            raise WebAPIException(response.status_code, response.text)
        data = response.json()
        day = data['day']
        contents:list[HistoryOnTodayItem] = []
        for item in data['result']:
            contents.append(HistoryOnTodayItem(item["day"],item["itle"]))

        return HistoryOnTodayDto(day,contents)

    async def getInfoFromImage(self,filePath) -> InfoFromImageDto:
        """
        TODO 图像识别出动漫，之后加一点识别是否为AI图，还有识别的是动漫还是gal的参数进去吧
        """
        url = self.config.WebAPI["InfoFromImage"]["URL"]
        files = {'image': open(filePath, 'rb')}
        params = self.config.WebAPI["InfoFromImage"]["Params"]
        async with httpx.AsyncClient() as client:
            # only httpx 不知道为什么用request防火墙会拦
            response = await client.post(url, files=files, params=params)
            response.raise_for_status()
            data = response.json()
        name = data["data"][0]['char'][0]['name']
        wrok = data["data"][0]['char'][0]['cartoonname']
        return InfoFromImageDto(name,wrok)

    def getRandomMusic(self):
        """
        随机音乐，然后调用播放的接口
        """
        url = self.config.WebAPI["Music"]["RandomMusic"]["URL"]
        params = self.config.WebAPI["Music"]["RandomMusic"]["Params"]
        response = requests.get(url, params=params)
        data = response.json()
        return RandomMusicDto(data['id'],data['title'],data['artist'],data['cover'])

    def getTr(self,msg,to:LanguageTypeEnum) -> TrDto:
        """"
        翻译　
        INFO　要求翻译文本大于2个字符，在APP里写一下吧
        """
        url = self.config.WebAPI["Translation"]["URL"]
        params = self.config.WebAPI["Translation"]["Params"]
        params['msg'] = msg
        params['to'] = to.value
        response = requests.get(url, params=params)
        data = response.json()
        return TrDto(data["msg"])

    def getWikiSearch(self,keyword):
        """
        维基百科搜索
        """
        url = self.config.WebAPI["Wiki"]["URL"]
        params = self.config.WebAPI["Wiki"]["Params"]
        params.update(self.config.WebAPI["Wiki"]["SearchParams"])
        params['lsrsearch'] = keyword
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        for item in data['query']['search']:
            results.append(WikiSearchItem(item['title'],item["pageid"],item['snippet']))
        return WikiSearchDto(results)

    def getWikiDetail(self,id):
        """
        维基百科条目
        """
        url = self.config.WebAPI["Wiki"]["URL"]
        params = self.config.WebAPI["Wiki"]["Params"]
        params.update(self.config.WebAPI["Wiki"]["GetParams"])
        params['pageids'] = id
        response = requests.get(url, params=params)
        data = response.json()
        return WikiDetailDto(data['query']['pages'][id]['title'],data['query']['pages'][id]['extract'])

    def getGPT(self,msg) -> GPTAnsDto :
        """
        GPT-3.5
        TODO 之后多研究一下参数，还有从数据库里读出之前的对话做记忆化
        """
        url = self.config.WebAPI["GPT"]["URL"]
        params = self.config.WebAPI["GPT"]["Data"]
        params['messages'] = [{}]
        params['messages'][0]['content'] = msg
        params['messages'][0]['role'] = "user"
        headers = self.config.WebAPI["GPT"]["Headers"]
        response = requests.get(url, data=json.dumps(params),headers=headers)
        data = response.json()
        return GPTAnsDto(data['choices'][0]['message']['content'])
