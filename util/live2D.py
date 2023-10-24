import ctypes,threading
from util.config import GlobalConfig

def startAsync(dll,x,y):
    # 异步调用 start 函数并传递参数 x 和 y
    dll.startLive2d(x, y)

def createLive2D(x,y):
    # 加载 DLL 文件
    dll = ctypes.WinDLL(GlobalConfig().Live2dPath)
    # 定义函数参数和返回值类型
    dll.startLive2d.argtypes = [ctypes.c_int, ctypes.c_int]
    dll.startLive2d.restype = None
    # 异步调用 start 函数
    startThread = threading.Thread(target=startAsync,args=(dll,x,y))
    startThread.start()
    return dll,startThread

# 定义返回结构体的类型
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

def getPos(dll):

    # 设置函数参数类型和返回类型
    dll.getPos.argtypes = ()
    dll.getPos.restype = Point

    pos = dll.getPos()

    return pos.x,pos.y

def live2dClose(dll):
    # 定义函数参数和返回值类型
    dll.closeLive2d.argtypes = None
    dll.closeLive2d.restype = None
    dll.closeLive2d()

def isLeftTouched(dll):
    # 定义函数参数和返回值类型
    dll.isLeftTouch.argtypes = None
    dll.isLeftTouch.restype = ctypes.c_bool
    return dll.isLeftTouch()

def isRightTouched(dll):
    # 定义函数参数和返回值类型
    dll.isRightTouch.argtypes = None
    dll.isRightTouch.restype = ctypes.c_bool
    return dll.isRightTouch()

def isOK(dll):
    # 定义函数参数和返回值类型
    dll.isOK.argtypes = None
    dll.isOK.restype = ctypes.c_bool
    return dll.isOK()
