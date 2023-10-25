from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from util.config import GlobalConfig
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from application.PetApp import PetApplication
from presentation.component.fromBox import *
from presentation.component.dialogBox import CharacterDialogBox
import shutil,asyncio,random
from util.live2D import *
from common.AIDrawType import *
from common.LanguageType import *
from util.showCon import *
from util.tools import *

class MainWindow(QWidget):
    """
    桌宠程序的主操作界面
    """
    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.resize(self.config.MainWindow["Weight"], self.config.MainWindow["Height"])
        self.hboxLayout = QHBoxLayout(self)

        self.app = PetApplication()
        self.threadPool = QThreadPool()

        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(50)
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audioOutput)

        self.dialog = CharacterDialogBox(GlobalConfig().PetName)
        self.dialog.hide()
        self.frombox = None
        self.stateMa = ShowWinStateMachine(self)

        self.dll = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrom)
        self.timer.start(100)  # 每100毫秒更新一次

        self.isLeftTapOK = True
        self.leftTapTimer = QTimer(self)
        self.leftTapTimer.timeout.connect(lambda :self.setLeftTapOK(True))
        self.leftTapTimer.setInterval(10000)
        self.leftTapTimer.setSingleShot(True)

        # 隐藏边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._initQss()
        self._initLayout()
        self._initConnections()

    def _initConnections(self):
        self.app.getInfoFromImageSignal.connect(self.showMainMsg)
        self.app.singleSentanceSignal.connect(self.showMsg)
        self.app.wheatherSignal.connect(self.showMsg)
        self.app.gptSignal.connect(self.showMainMsg)
        self.app.musicToFileSignal.connect(self._playMusicFromFile)
        self.app.musicToFileSignal.connect(self.stopLoopMsg)
        self.app.randomMusicSiganl.connect(self._randomMusic)
        self.app.randomPicSignal.connect(self.showPicTip)
        self.app.randomPicSignal.connect(self.stopLoopMsg)
        self.app.drawAISiganl.connect(self.showPicTip)
        self.app.drawAISiganl.connect(self.stopLoopMsg)


    def _initLayout(self):
        self.setLayout(self.hboxLayout)
        self.hboxLayout.addWidget(self.dialog, 0, Qt.AlignmentFlag.AlignTop)

    def setLeftTapOK(self,flag):
        self.isLeftTapOK = flag
        if not flag:
            self.leftTapTimer.stop()
            self.leftTapTimer.start()

    @pyqtSlot()
    def initLive2d(self):
        globalPosition = self.geometry().center()
        self.dll,self.dllThread = createLive2D(globalPosition.x(),globalPosition.y())

    def updateFrom(self):
        if self.dll is not None and isOK(self.dll):
            x, y = getPos(self.dll)
            self.move(x - self.width() // 2, y - self.height() // 2)
            if isLeftTouched(self.dll) and self.isLeftTapOK:
                # 下面两句话顺序有要求
                self.setLeftTapOK(False)
                self.leftTap()
            if isRightTouched(self.dll):
                self.rightTap()

    def _initQss(self):
        self.setStyleSheet(f"""
            MainWindow {{
                background: {self.config.MainWindow['Background']};
            }}
        """)

    def leftTap(self):
        randomNumber = random.random()
        if randomNumber < 0.8 :
            f = FunctionRunnable(self.app.getSingle)
            self.threadPool.start(f)
        else:
            f = FunctionRunnable(self.app.getTimeAndWeather)
            self.threadPool.start(f)

    def rightTap(self):
        """
        自定义鼠标右键事件，调出控制仪表盘
        """
        view = CommandBarView(self)

        gpt = Action(FIF.MESSAGE, 'GPT猫娘')
        view.addAction(gpt)
        gpt.triggered.connect(self.gpt)

        music = Action(FIF.MUSIC, '播放音乐')
        view.addAction(music)
        music.triggered.connect(self.playMusic)

        randomMusic = Action(FIF.CALORIES, '随机二次元音乐')
        view.addAction(randomMusic)
        randomMusic.triggered.connect(self.randomMusic)

        pic = Action(FIF.PALETTE, '随机图片')
        view.addAction(pic)
        pic.triggered.connect(self.showRandomPic)

        search = Action(FIF.SEARCH_MIRROR, '二次元识别')
        view.addAction(search)
        search.triggered.connect(self.search)

        draw = Action(FIF.PENCIL_INK, 'AI绘画')
        view.addAction(draw)
        draw.triggered.connect(self.draw)

        tr = Action(FIF.LANGUAGE, '翻译')
        view.addAction(tr)
        tr.triggered.connect(self.tr)

        wiki = Action(FIF.BOOK_SHELF, '维基百科')
        view.addAction(wiki)
        wiki.triggered.connect(self.showWiki)

        history = Action(FIF.HISTORY, '历史上今天的事')
        view.addAction(history)
        history.triggered.connect(self.showHistoryOntoday)

        view.addHiddenAction(Action(FIF.SETTING, '设置'))
        closeAction = Action(FIF.CLOSE, '关闭')
        closeAction.triggered.connect(lambda: self.onClose())
        view.addHiddenAction(closeAction)
        view.resizeToSuitableWidth()

        left = self.geometry().left()
        h = self.geometry().height()
        pos = QPoint(left, self.geometry().top() + h * 0.7)
        Flyout.make(view, pos, self, FlyoutAnimationType.FADE_IN)

    def onClose(self):
        live2dClose(self.dll)
        self.dllThread.join()
        self.close()

    def draw(self):
        frombox = self.showFromBox("AI绘画","请输入图片关键字",[AIOptionsStyle,AIOptionsRatio])
        frombox.fromContentSignal.connect(self._draw)

    @pyqtSlot(str,list)
    def _draw(self,content,index):
        f = FunctionRunnable(self.app.drawAI,content,AIOptionsStyle[index[0]],AIOptionsRatio[index[1]])
        self.threadPool.start(f)

    def gpt(self):
        frombox = self.showFromBox("GPT猫娘","请输入对话内容")
        frombox.fromContentSignal.connect(self._gpt)

    @pyqtSlot(str)
    def _gpt(self,content):
        f = FunctionRunnable(self.app.getGPT,content)
        self.threadPool.start(f)
        self.showWaitMsg("思考中.....")

    def showFromBox(self,title,content,options=None):
        self.frombox = FromBox(title,content,options)
        self.stateMa.setState(FromBoxState(self.frombox))
        return self.frombox

    def viewLayAddShowW(self,view):
        self.hboxLayout.addWidget(view,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

    def randomMusic(self):
        f = FunctionRunnable(self.app.getRandomMusic)
        self.threadPool.start(f)
        self.showWaitMsg("挑选中.....")

    def _randomMusic(self,title,author):
        self._playMusicFromFile()
        self.showMainMsg(f"正在播放：{title}，作者：{author}")

    def search(self):
        # 打开文件选择对话框
        file, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.png *.jpg)")
        f = FunctionRunnable(self.app.getInfoFromImage,file)
        self.threadPool.start(f)
        self.showWaitMsg("识别中.....")

    def showMsg(self,msg):
        self.stateMa.setState(DialogState(self.dialog))
        self.dialog.printDialog(msg)

    def showMainMsg(self,msg):
        self.showMsg(msg)
        # 下面两句话的先后顺序有要求
        self.setLeftTapOK(False)
        self.leftTapTimer.stop()
        self.dialog.hideSignal.connect(self._setHideSlot)

    @pyqtSlot()
    def _setHideSlot(self):
        self.dialog.hideSignal.disconnect(self._setHideSlot)
        self.setLeftTapOK(True)

    def showWaitMsg(self,text):
        self.stateMa.setState(DialogState(self.dialog))
        self.dialog.printLoopDialog(GlobalConfig().PetName + text,GlobalConfig().Timeout)
        self.setLeftTapOK(False)
        self.leftTapTimer.stop()

    def tr(self):
        frombox = self.showFromBox("翻译","请输入要翻译的文本",[languageOptions])
        frombox.fromContentSignal.connect(self._tr)

    def _tr(self,keyword,index):
        # 去除“To ”
        msg = self.app.getTr(keyword,languageOptions[index[0]][3:])
        self.showMsg(msg)

    def showHistoryOntoday(self):
        day,content = self.app.getHistoryOnToday()
        self.showMsg(f"{day}，{content}")

    def showRandomPic(self):
        f = FunctionRunnable(self.app.getRandomPicToFile)
        self.threadPool.start(f)
        self.showWaitMsg("挑选中.....")

    def showWiki(self):
        frombox = self.showFromBox("wiki","请输入关键字")
        frombox.fromContentSignal.connect(self._showWiki)

    def _showWiki(self,keyword):
        msg = self.app.getWiki(keyword)
        self.showMsg(msg)

    def showPicTip(self):
        position = TeachingTipTailPosition.RIGHT
        view = TeachingTipView(
            icon=None,
            title='𝓖𝓪𝓵𝓵𝓪𝓻𝔂',
            content="𝑨𝒓𝒕 𝒊𝒔 𝒕𝒉𝒆 𝒍𝒊𝒆 𝒕𝒉𝒂𝒕 𝒆𝒏𝒂𝒃𝒍𝒆𝒔 𝒖𝒔 𝒕𝒐 𝒓𝒆𝒂𝒍𝒊𝒛𝒆 𝒕𝒉𝒆 𝒕𝒓𝒖𝒕𝒉.",
            image=GlobalConfig().TempPic,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
        )

        # add widget to view
        button = PushButton('下载到本地')
        button.clicked.connect(lambda :self.downloadToLocal(GlobalConfig().TempPic,type="jpg"))
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        tip = TeachingTip.make(
            view, target=self, duration=-1, tailPosition=position, parent=self)
        view.closed.connect(tip.close)

    def downloadToLocal(self,filePath,type):
        # 打开文件对话框，选择保存路径和文件名
        savePath, _ = QFileDialog.getSaveFileName(self, "保存文件", "", f"{type} Files (*.{type})")
        if savePath:
            try:
                # 复制源数据文件到选择的保存路径
                shutil.copyfile(filePath, savePath)
                print("文件保存成功:", savePath)
            except Exception as e:
                print("保存文件时出错:", str(e))
        else:
            print("未选择保存路径或文件名")

    def playMusic(self):
        frombox = self.showFromBox("播放音乐", "请输入歌曲关键字")
        frombox.fromContentSignal.connect(self._playMusic)

    @pyqtSlot(str)
    def _playMusic(self,keyWord):
        f = FunctionRunnable(self.app.getMusicToFile,keyWord)
        self.threadPool.start(f)
        self.showWaitMsg("查询中.....")

    @pyqtSlot()
    def _playMusicFromFile(self):
        self.player.setSource(QUrl.fromLocalFile(GlobalConfig().TempMusic))
        self.player.play()

    @pyqtSlot()
    def stopLoopMsg(self):
        self.setLeftTapOK(True)
        self.leftTapTimer.start()
        self.dialog.stopDialog()
