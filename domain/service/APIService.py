from util.config import GlobalConfig
from datetime import datetime
from do.dto.APIDto import *
import requests,io,httpx,json
from exception import WebAPIException
from common.LanguageType import LanguageTypeEnum
from common.AIDrawType import AIDrawStyleEnum,AIDrawRadioEnum
from common.RankingImgType import RankingImgType,RankingImgMode
from datetime import datetime,timedelta

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
        if (response.status_code != 200 or data['status'] != "1" or data['infocode'] != '10000'):
            raise WebAPIException(response.status_code, response.text)
        return WeatherDto(data['lives'][0]['weather'], data['lives'][0]['temperature'], data['lives'][0]['winddirection'], data['lives'][0]['windpower'], data['lives'][0]['humidity'], data['lives'][0]['reporttime'])

    def getMusicID(self,keyword) -> MusicIDDto:
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
        return  MusicIDDto(data['result']['songs'][0]['id'])

    def getMusicURL(self,id) -> MusicURLDto:
        getURL = self.config.WebAPI["Music"]["Get"]["URL"]
        getParams = self.config.WebAPI["Music"]["Get"]["Params"]
        getParams['id'] = id
        response = requests.get(getURL, params=getParams)
        data = response.json()
        if (response.status_code != 200):
            raise WebAPIException(response.status_code, response.text)
        musicURL = data['data'][0]['url']
        audioType = data['data'][0]['type']
        return MusicURLDto(musicURL,audioType)

    def getRandomPicture(self) -> PictureDataDto:
        """
        获得随机图片的数据
        """
        url = self.config.WebAPI["Picture"]["URL"]
        response = requests.get(url)
        return PictureDataDto(response.content)
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

    def getSearchImages(self,type:RankingImgType,mode:RankingImgMode):
        """
        获得搜索图片
        BUG 还未写好
        """
        url = self.config.WebAPI["Image"]["Ranking"]["URL"]
        params = self.config.WebAPI["Image"]["Ranking"]["Params"]
        params['ranking_type'] = type.value
        params['mode'] = mode.value
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=2)
        formatted_date = previous_date.strftime("%Y-%m-%d")
        params['date'] = formatted_date
        response = requests.get(url, params=params)
        data = response.json()
        nextPage = data["next_url"]
        # TODO 这边他一次最少返回30个好象，要处理一下
        num =  self.config.WebAPI["Image"]["Ranking"]["Params"]["per_page"]
        data = data["illusts"]
        results = []

        # 遍历前num个元素
        for item in data[:num]:
            title = item["title"]
            username = item["user"]["name"]
            id = item["id"]
            caption = item["caption"]

            imageURL = item["image_urls"]["large"]

            # 创建包含所需字段的字典
            result = SearchImagesItem(id,title,username,imageURL,caption)

            # 将字典添加到结果列表中
            results.append(result)

        return SearchImagesDto(results,nextPage)

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
            contents.append(HistoryOnTodayItem(item["date"],item["title"]))

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
        name = data["data"][0]['name']
        wrok = data["data"][0]['cartoonname']
        return InfoFromImageDto(name,wrok)

    def getRandomMusic(self):
        """
        随机音乐，然后调用播放的接口
        """
        url = self.config.WebAPI["Music"]["Random"]["URL"]
        params = self.config.WebAPI["Music"]["Random"]["Params"]
        response = requests.get(url, params=params)
        data = response.json()
        return RandomMusicDto(data['id'],data['title'],data['artist'],data['cover'])

    def getTr(self,msg,to:LanguageTypeEnum) -> TrDto:
        """"
        翻译　
        INFO　好像是翻译出来的文本太短和被翻译的文本太短都不行欸，还有翻译成中文有点bug
        """
        url = self.config.WebAPI["Translation"]["URL"]
        params = self.config.WebAPI["Translation"]["Params"]
        params['msg'] = msg
        params['to'] = to.value
        response = requests.get(url, params=params)
        data = response.json()
        return TrDto(data["msg"])

    def getWikiSearch(self,keyword) -> WikiSearchDto:
        """
        维基百科搜索
        """
        url = self.config.WebAPI["Wiki"]["URL"]
        params = self.config.WebAPI["Wiki"]["Params"]
        params.update(self.config.WebAPI["Wiki"]["SearchParams"])
        params['srsearch'] = keyword
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
        return WikiDetailDto(data['query']['pages'][f'{id}']['title'],data['query']['pages'][f'{id}']['extract'])

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
        response = requests.post(url, data=json.dumps(params),headers=headers)
        data = response.json()
        return GPTAnsDto(data['choices'][0]['message']['content'])

    def getAIDraw(self,txt,style: AIDrawStyleEnum,radio: AIDrawRadioEnum) -> AIDrawDto:
        """
        AI画画
        """
        url = self.config.WebAPI["AIDraw"]["URL"]
        params = self.config.WebAPI["AIDraw"]["Params"]
        params['imgTxt'] = txt
        params['style'] = style.value
        params['ratio'] = radio.value
        response = requests.post(url, data=params)
        data = response.json()
        return AIDrawDto(data['data']['result']['img'])
