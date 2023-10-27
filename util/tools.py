from do.APIDto import *
import httpx, random, datetime
from PyQt6.QtCore import QRunnable

def downloadURLRes(url) -> bytes:
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
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

class FunctionRunnable(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        # 在这里执行函数任务
        self.function(*self.args, **self.kwargs)
