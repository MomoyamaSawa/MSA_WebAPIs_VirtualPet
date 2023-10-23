from do.dto.APIDto import *
import requests,io, random
from exception import WebAPIException

def downloadURLRes(url) -> bytes:
    response = requests.get(url)
    if (response.status_code != 200):
        raise WebAPIException(response.status_code, response.text)
    return response.content

def saveTofile(data:bytes, filename):
    try:
        with open(filename, 'wb') as file:
            file.write(data)
        print('已保存到文件:', filename)
    except Exception as e:
        print('保存文件时发生错误:', str(e))

def chooseRandomElement(array):
    if len(array) > 0:
        random_element = random.choice(array)
        return random_element
    else:
        return None
