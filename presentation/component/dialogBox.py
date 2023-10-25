from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from qfluentwidgets import ToolButton
from util.config import GlobalConfig
import sys
from qfluentwidgets import FluentIcon as FIF
from util.tools import cmdErrStr

class DialogBox(QFrame):
    """
    对话框的下面文字部分
    """
    hideSignal = pyqtSignal()

    def __init__(self, content):
        super().__init__()

        self.vBoxLayout = QVBoxLayout()
        self.setFixedWidth(375)
        self.timer = QTimer()
        self.timeTimer = QTimer()
        self.timeTimer.timeout.connect(self.timeoutFunc)
        self.state = 1

        self.label = QLabel(content)
        # 占据父组件的全部宽度
        self.label.setFixedWidth(320)
        self.label.setWordWrap(True)

        self._initLayout()
        self._initQss()

    def _initLayout(self):
        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.setContentsMargins(30, 20, 30, 20)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def printDialog(self, text,loop = False,time=0):
        if self.timer.isActive() or self.timeTimer.isActive():
            self.timer.stop()
            self.timeTimer.stop()
        self.timer = QTimer()
        self.state = 1
        self.currentIndex = 0
        self.label.setText("")
        self.index = 0
        self.text = text
        self.timer.timeout.connect(lambda: self.showNextCharacter(loop))
        self.timer.start(100)
        if time != 0:
            self.timeTimer.start(time*1000)

    def timeoutFunc(self):
        self.timer.stop()
        self.timeTimer.stop()
        self.label.setText("（[error] 响应超时，请检查错误日志）")

    def showNextCharacter(self,loop=False):
        if self.currentIndex >= len(self.text):
            if loop:
                self.currentIndex = 0
            else:
                self.timer.stop()
            return

        self.label.setText(self.text[self.index:self.currentIndex + 1])
        rowCount = self.getLabelRowCount()
        if rowCount >= 4:
            self.timer.stop()
            self.label.setText(self.text[self.index:self.currentIndex]+"    ......(点击继续)")
            self.update()
            self.state = 0
            return
        self.currentIndex += 1

    def getLabelRowCount(self):
        font_metrics = QFontMetrics(self.label.font())
        line_count = self.label.height() // font_metrics.lineSpacing()
        return line_count

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.state == 0:
            self.timer.start(100)
            self.index = self.currentIndex
            self.label.setText("")
            self.state = 1
        else:
            self.hideSignal.emit()

    def _initQss(self):
        self.setStyleSheet(f"""
            DialogBox {{
                background: {GlobalConfig().Panel['Background']};
                border: {GlobalConfig().Panel['Border']};
                border-radius: 50px;
            }}
        """)

class CharacterBox(QFrame):
    """
    对话框的角色名部分
    """
    def __init__(self,name):
        super().__init__()

        self.setFixedSize(200,40)
        self.hBoxLayout = QHBoxLayout()
        self.label = QLabel(name)
        font = QFont("Arial", 15)
        self.label.setFont(font)
        self.svg = QSvgWidget()
        self.svg.load("resource/slack.svg")

        self._initLayout()
        self._initQss()

    def _initLayout(self):
        self.setLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.svg, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addStretch(1)

    def _initQss(self):
        self.setStyleSheet(f"""
            CharacterBox {{
                background:rgb(103,102,136);
                border: 3px solid white;
                border-radius: 18px;
                margin-left: 20px;
            }}
        """)
        self.label.setStyleSheet("color: white;")

class CharacterDialogBox(QWidget):
    hideSignal = pyqtSignal()
    def __init__(self, name):
        super().__init__()

        self.setFixedSize(400, 150)
        self.vBoxlayout = QVBoxLayout()

        self.DialogBox = DialogBox("")
        self.characterBox = CharacterBox(name)
        self.DialogBox.hideSignal.connect(self.hide)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self._setLayout()

    def _setLayout(self):
        self.setLayout(self.vBoxlayout)
        self.vBoxlayout.addWidget(self.characterBox, 0, Qt.AlignmentFlag.AlignLeft)
        self.vBoxlayout.addSpacing(-20)
        self.vBoxlayout.addWidget(self.DialogBox, 0, Qt.AlignmentFlag.AlignLeft)
        # 改变图层，向上移动到最顶层
        self.characterBox.raise_()

    def printDialog(self,text):
        self.DialogBox.printDialog(text)

    def printLoopDialog(self,text,time):
        self.DialogBox.printDialog(text,True,time)

    def hideEvent(self, a0: QHideEvent) -> None:
        self.hideSignal.emit()
        return super().hideEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建对话框实例并传入角色姓名和说话内容
    dialog = CharacterDialogBox("草薙寧々")
    dialog.printDialog("我是草薙寧々，是一名来自日本的高中生.我是草薙寧々，是一名来自日本的高中生.我是草薙寧々，是一名来自日本的高中生.我是草薙寧々，是一名来自日本的高中生.我是草薙寧々，是一名来自日本的高中生.")
    dialog.show()

    sys.exit(app.exec())

