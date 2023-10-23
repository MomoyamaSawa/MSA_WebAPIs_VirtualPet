from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from util.config import GlobalConfig
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from application.PetApp import PetApplication
from presentation.component.customMsgBox import *
from presentation.component.dialogBox import CharacterDialogBox
import shutil,asyncio
from util.live2D import *

class MainWindow(QWidget):
    """
    桌宠程序的主界面
    """

    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.resize(self.config.MainWindow["Weight"], self.config.MainWindow["Height"])
        self.hboxLayout = QHBoxLayout(self)
        self.app = PetApplication()
        self.app.getInfoFromImageSignal.connect(self.getSearchInfo)
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(100)
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audioOutput)
        self.dialog = CharacterDialogBox(GlobalConfig().PetName)
        self.dialog.hide()
        self.w = QWidget()
        self.dll = None
        self.once = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrom)
        self.timer.start(100)  # 每100毫秒更新一次位置

        # 隐藏边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setWindowOpacity(0.1)

        self._initQss()
        self._initLayout()

    def _initLayout(self):
        self.setLayout(self.hboxLayout)
        self.hboxLayout.addWidget(self.dialog, 0, Qt.AlignmentFlag.AlignTop)
        self.hboxLayout.addWidget(self.w)

    def initLive2d(self):
        globalPosition = self.geometry().center()
        self.dll,self.dllThread = createLive2D(globalPosition.x(),globalPosition.y())

    def updateFrom(self):
        if self.dll is not None and isOK(self.dll):
            # if not self.once:
            #     # 获取C++程序的窗口句柄
            #     cppWindow = win32gui.FindWindow(None, "VirtualPet")
            #     # 获取Python程序的窗口句柄
            #     pythonWindow = self.winId()
            #     # 将窗口A置于窗口B之上
            #     win32gui.SetWindowPos(pythonWindow, cppWindow, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            x, y = getPos(self.dll)
            width = self.width()
            height = self.height()
            self.move(x - width // 2, y - height // 2)
            self.activateWindow()
            if isLeftTouched(self.dll):
                self.dialog.show()
                self.dialog.printDialog("主人，我在这里呢~")
            if isRightTouched(self.dll):
                self.contextMenuEvent(None)

    def _initQss(self):
        self.setStyleSheet(f"""
            MainWindow {{
                background: {self.config.MainWindow['Background']};
            }}
        """)

    def contextMenuEvent(self, e):
        """
        自定义鼠标右键事件，调出控制仪表盘
        """
        view = CommandBarView(self)

        music = Action(FIF.MUSIC, '播放音乐')
        view.addAction(music)
        music.triggered.connect(self.playMusic)

        pic = Action(FIF.PALETTE, '随机图片')
        view.addAction(pic)
        pic.triggered.connect(self.showRandomPic)

        wiki = Action(FIF.BOOK_SHELF, '维基百科')
        view.addAction(wiki)
        wiki.triggered.connect(self.showWiki)

        history = Action(FIF.HISTORY, '历史上今天的事')
        view.addAction(history)
        history.triggered.connect(self.showHistoryOntoday)

        randomMusic = Action(FIF.CALORIES, '随机二次元音乐')
        view.addAction(randomMusic)
        randomMusic.triggered.connect(self.randomMusic)

        tr = Action(FIF.LANGUAGE, '中日翻译')
        view.addAction(tr)
        tr.triggered.connect(self.tr)

        search = Action(FIF.SEARCH_MIRROR, '二次元识别')
        view.addAction(search)
        search.triggered.connect(self.search)

        draw = Action(FIF.PENCIL_INK, 'AI绘画')
        view.addAction(draw)
        draw.triggered.connect(self.draw)

        gpt = Action(FIF.MESSAGE, 'GPT猫娘')
        view.addAction(gpt)
        gpt.triggered.connect(self.gpt)

        view.addHiddenAction(Action(FIF.SETTING, 'Settings', shortcut='Ctrl+S'))
        closeAction = Action(FIF.CLOSE, 'Close', shortcut='Ctrl+A')
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
        content,style,radio = self.showAIDialog("AI绘画","请输入图片关键字")
        if content is None:
            return
        self.app.drawAI(content,style,radio)
        self.showPicTip()

    def gpt(self):
        keyword,_ = self.showDialog("GPT猫娘", "请输入对话内容")
        if keyword is None:
            return
        msg = self.app.getGPT(keyword)
        self.dialog.show()
        self.dialog.printDialog(msg)

    def randomMusic(self):
        title,author = self.app.getRandomMusic()
        self.player.setSource(QUrl.fromLocalFile(GlobalConfig().TempMusic))
        self.player.play()
        self.dialog.show()
        self.dialog.printDialog(f"正在播放：{title}，作者：{author}")

    def search(self):
        # 打开文件选择对话框
        file, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.png *.jpg *.jpeg)")
        asyncio.run(self.app.getInfoFromImage(file))

    def getSearchInfo(self,info):
        self.dialog.show()
        self.dialog.printDialog(info)

    def tr(self):
        keyword,type = self.showDialog("翻译","请输入要翻译的文本",["日语","英语","中文"])
        if keyword is None:
            return
        msg = self.app.getTr(keyword,type)
        self.dialog.show()
        self.dialog.printDialog(f"{msg}")

    def showHistoryOntoday(self):
        day,content = self.app.getHistoryOnToday()
        self.dialog.show()
        self.dialog.printDialog(f"{day}，{content}")

    def showRandomPic(self):
        self.app.getRandomPicToFile()
        self.showPicTip()

    def showWiki(self):
        keyword,_ = self.showDialog("wiki","请输入关键字")
        if keyword is None:
            return
        msg = self.app.getWiki(keyword)
        self.dialog.show()
        self.dialog.printDialog(msg)

    def showPicTip(self):
        position = TeachingTipTailPosition.RIGHT
        view = TeachingTipView(
            icon=None,
            title='𝓖𝓪𝓵𝓵𝓪𝓻𝔂',
            content="𝑨𝒓𝒕 𝒊𝒔 𝒕𝒉𝒆 𝒍𝒊𝒆 𝒕𝒉𝒂𝒕 𝒆𝒏𝒂𝒃𝒍𝒆𝒔 𝒖𝒔 𝒕𝒐 𝒓𝒆𝒂𝒍𝒊𝒛𝒆 𝒕𝒉𝒆 𝒕𝒓𝒖𝒕𝒉.",
            image=GlobalConfig().TempPic,
            # image='resource/boqi.gif',
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
        keyword = self.showDialog("播放音乐", "请输入歌曲关键字")
        if keyword is None:
            return
        self.app.getMusicToFile(keyword)
        self.player.setSource(QUrl.fromLocalFile(GlobalConfig().TempMusic))
        self.player.play()

    def showDialog(self,title,content,options=None):
        w = CustomMessageBox(self,title,content,options)
        if w.exec():
            return w.urlLineEdit.text(),w.type

    def showAIDialog(self,title,content):
        w = AIDrawMessageBox(self,title,content)
        if w.exec():
            return w.urlLineEdit.text(),w.styleAI,w.radio

