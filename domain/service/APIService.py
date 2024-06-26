from util.config import GlobalConfig
from datetime import datetime
from do.APIDto import *
import httpx,json,random
from common.LanguageType import LanguageTypeEnum
from common.AIDrawType import *
from common.hitohotoType import HitokotoTypeEnum
from datetime import datetime
from do.PetDto import *
import winreg

class APIService:
    """
    提供调用各种 web/sys API 的服务
    """
    def __init__(self):
        self.config = GlobalConfig()
        self.proxies = self.get_windows_proxy()

    def get_windows_proxy(self):
        try:
            internet_settings = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            )
            proxy_enabled = winreg.QueryValueEx(internet_settings, "ProxyEnable")[0]
            if proxy_enabled:
                proxy_server = winreg.QueryValueEx(internet_settings, "ProxyServer")[0]
                proxies = {}
                if "=" in proxy_server:
                    # Different proxy for different protocols
                    for part in proxy_server.split(";"):
                        protocol, address = part.split("=")
                        proxies[protocol] = f"{protocol}://{address}"
                else:
                    # Same proxy for all protocols
                    proxies["http://"] = f"http://{proxy_server}"
                    proxies["https://"] = f"http://{proxy_server}"
                return proxies
            else:
                return None
        except Exception as e:
            print(f"Error accessing registry: {e}")
            return None

    def getTime(self) -> TimeDto:
        """
        获得日期时间
        """
        currentTime = datetime.now()
        return TimeDto(currentTime.year, currentTime.month, currentTime.day, currentTime.hour, currentTime.weekday())

    def getWeather(self) -> WeatherDto:
        """
        获得天气
        https://lbs.amap.com/api/webservice/guide/api/weatherinfo
        """
        url = GlobalConfig().WebAPI["GetWeather"]["URL"]
        params =  GlobalConfig().WebAPI["GetWeather"]["Params"]
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return WeatherDto(data['lives'][0]['weather'], data['lives'][0]['temperature'], data['lives'][0]['winddirection'], data['lives'][0]['windpower'], data['lives'][0]['humidity'], data['lives'][0]['reporttime'])

    def getMusicID(self,keyword) -> str:
        """
        取得一首歌的下载 url

        TODO 暂未测试无版权的时候是否可用，这边之后拆一下
        """
        searchURL = self.config.WebAPI["Music"]["Search"]["URL"]
        searchParams = self.config.WebAPI["Music"]["Search"]["Params"]
        searchParams['keywords'] = keyword
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(searchURL, params=searchParams,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return data['result']['songs'][0]['id'],data['result']['songs'][0]['name']

    def getMusicList(self,keyword) -> list[MusicListItemDto]:
        searchURL = GlobalConfig().WebAPI["Music"]["Search"]["URL"]
        searchParams = GlobalConfig().WebAPI["Music"]["Search"]["Params"]
        searchParams['keywords'] = keyword
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(searchURL, params=searchParams,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        results = []
        for item in data['result']['songs']:
            results.append(MusicListItemDto(item['id'],item['name'],item['ar'][0]['name']))
        return results

    def getMusicURL(self,id) -> (str,type):
        getURL =  GlobalConfig().WebAPI["Music"]["Get"]["URL"]
        getParams =  GlobalConfig().WebAPI["Music"]["Get"]["Params"]
        getParams['id'] = id
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(getURL, params=getParams,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        musicURL = data['data'][0]['url']
        return musicURL

    def getRandomPicture(self) -> (str,bytes):
        """
        获得随机图片的数据
        """
        url = self.config.WebAPI["Picture"]["URL"]
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        return url,response.content

    def getSingleSentance(self) -> SentanceDataDto:
        """
        获得随机的语句
        https://developer.hitokoto.cn/sentence/
        """
        url = self.config.WebAPI["Sentance"]["URL"]
        value = random.sample(list(HitokotoTypeEnum), 1)
        # 随机来一个分类
        params = {'c': value[0].value}
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return SentanceDataDto(data['from'], data['from_who'], data['hitokoto'])

    # region
    # def getSearchImages(self,type:RankingImgType,mode:RankingImgMode):
    #     """
    #     获得搜索图片
    #     BUG 还未写好
    #     """
    #     url = self.config.WebAPI["Image"]["Ranking"]["URL"]
    #     params = self.config.WebAPI["Image"]["Ranking"]["Params"]
    #     params['ranking_type'] = type.value
    #     params['mode'] = mode.value
    #     current_date = datetime.now()
    #     previous_date = current_date - timedelta(days=2)
    #     formatted_date = previous_date.strftime("%Y-%m-%d")
    #     params['date'] = formatted_date
    #     response = requests.get(url, params=params)
    #     data = response.json()
    #     nextPage = data["next_url"]
    #     # TODO 这边他一次最少返回30个好象，要处理一下
    #     num =  self.config.WebAPI["Image"]["Ranking"]["Params"]["per_page"]
    #     data = data["illusts"]
    #     results = []

    #     # 遍历前num个元素
    #     for item in data[:num]:
    #         title = item["title"]
    #         username = item["user"]["name"]
    #         id = item["id"]
    #         caption = item["caption"]

    #         imageURL = item["image_urls"]["large"]

    #         # 创建包含所需字段的字典
    #         result = SearchImagesItem(id,title,username,imageURL,caption)

    #         # 将字典添加到结果列表中
    #         results.append(result)

    #     return SearchImagesDto(results,nextPage)
    # endregion

    def getHistoryOnToday(self) -> HistoryOnTodayDto:
        """
        获得历史上的今天
        """
        url = self.config.WebAPI["History"]["URL"]
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        day = data['day']
        contents:list[HistoryOnTodayItem] = []
        for item in data['result']:
            contents.append(HistoryOnTodayItem(item["date"],item["title"]))
        return HistoryOnTodayDto(day,contents)

    def getInfoFromImage(self,filePath) -> (str,str):
        """
        TODO 图像识别出动漫，之后加一点识别是否为AI图，还有识别的是动漫还是gal的参数进去吧
        """
        url = self.config.WebAPI["InfoFromImage"]["URL"]
        files = {'image': open(filePath, 'rb')}
        params = self.config.WebAPI["InfoFromImage"]["Params"]
        with httpx.Client(proxies=self.proxies) as client:
            # only httpx 不知道为什么用request防火墙会拦
            response = client.post(url, files=files, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return data["data"][0]['name'],data["data"][0]['cartoonname']

    def getRandomMusic(self) -> RandomMusicDto:
        """
        随机音乐，然后调用播放的接口
        TODO 有没有办法把封面也展示一下
        """
        url = self.config.WebAPI["Music"]["Random"]["URL"]
        params = self.config.WebAPI["Music"]["Random"]["Params"]
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return RandomMusicDto(data['id'],data['title'],data['artist'],data['cover'])

    def getTr(self,msg,to:LanguageTypeEnum):
        """"
        翻译　
        INFO　好像是翻译出来的文本太短和被翻译的文本太短都不行欸，还有翻译成中文有点bug
        """
        url = self.config.WebAPI["Translation"]["URL"]
        params = self.config.WebAPI["Translation"]["Params"]
        params['msg'] = msg
        params['to'] = to.value
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return data["msg"]

    def getWikiSearch(self,keyword) -> WikiSearchDto:
        """
        维基百科搜索
        """
        url = self.config.WebAPI["Wiki"]["URL"]
        params = self.config.WebAPI["Wiki"]["Params"]
        params.update(self.config.WebAPI["Wiki"]["SearchParams"])
        params['srsearch'] = keyword
        # 打印最终访问的URL
        full_url = httpx.URL(url, params=params)
        print(f"Final URL: {full_url}")
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
            print(f"Response: {response}")
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
        with httpx.Client(proxies=self.proxies) as client:
            response = client.get(url, params=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return WikiDetailDto(data['query']['pages'][f'{id}']['title'],data['query']['pages'][f'{id}']['extract'])

    def getGPT(self,msg,logs:list[GptLogsDto]) -> str :
        """
        GPT-3.5
        https://chatanywhere.apifox.cn/
        """
        url = GlobalConfig().WebAPI["GPT"]["URL"]
        params = GlobalConfig().WebAPI["GPT"]["Data"]
        sysRole = GlobalConfig().WebAPI["GPT"]["SysRole"]
        params['messages'] = []
        params['messages'].append(sysRole)
        for log in logs:
            q = {
                "content":log.question,
                "role":"user"
            }
            a = {
                "content":log.answer,
                "role":"assistant"
            }
            params['messages'].append(q)
            params['messages'].append(a)
        now = {
            "content":msg,
            "role":"user"
        }
        params['messages'].append(now)
        headers = GlobalConfig().WebAPI["GPT"]["Headers"]
        with httpx.Client(proxies=self.proxies) as client:
            response = client.post(url, data=json.dumps(params),headers=headers,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

    def getAIDraw(self,txt,style: AIDrawStyleEnum,radio: AIDrawRatioEnum):
        """
        AI画画
        """
        url = self.config.WebAPI["AIDraw"]["URL"]
        params = self.config.WebAPI["AIDraw"]["Params"]
        params['imgTxt'] = txt
        params['style'] = style.value
        params['ratio'] = radio.value
        with httpx.Client(proxies=self.proxies) as client:
            response = client.post(url, data=params,timeout=GlobalConfig().Timeout)
            response.raise_for_status()
        data = response.json()
        return data['data']['result']['img']
