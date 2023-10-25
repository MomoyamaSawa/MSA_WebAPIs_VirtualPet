from do.APIDto import *
import requests, random, datetime
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
    except Exception as e:
        print('保存文件时发生错误:', str(e))

def chooseRandomElement(array):
    if len(array) > 0:
        random_element = random.choice(array)
        return random_element
    else:
        return None

def fromDateTimeToStr(dateTime:datetime):
    return dateTime.strftime("%Y-%m-%d %H:%M:%S")

def cmdErrStr(msg):
    return f"\033[31m[error] {msg}\033[0m"

def cmdInfoStr(msg):
    return f"[info] {msg}"

def cmdMainInfoStr(msg):
    return f"\033[94m[info] {msg}\033[0m"
