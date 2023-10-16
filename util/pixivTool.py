from util.config import GlobalConfig
import requests

def getPixivImgData(imgURL) -> bytes:
    config = GlobalConfig()
    url = config.WebAPI["Image"]["Get"]["URL"]
    params = config.WebAPI["Image"]["Get"]["Params"]
    params["url"] = imgURL
    response = requests.get(url, params=params)
    return response.content
