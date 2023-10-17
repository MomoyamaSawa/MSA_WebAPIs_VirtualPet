from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from util.config import GlobalConfig
from presentation.component.panel import Panel
from qfluentwidgets import (FluentIcon, TransparentDropDownPushButton, RoundMenu, CommandBar, Action,
                            setTheme, Theme, setFont, CommandBarView, Flyout, FlyoutAnimationType,
                            ImageLabel, ToolButton, PushButton)
from qfluentwidgets import FluentIcon as FIF

class MainWindow(QWidget):
    """
    桌宠程序的主界面
    """

    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.resize(self.config.MainWindow["Weight"], self.config.MainWindow["Height"])
        self.hboxLayout = QHBoxLayout(self)
        # 隐藏边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self._initQss()
        self._initLayout()


    def _initLayout(self):
        self.setLayout(self.hboxLayout)

    def _initQss(self):
        self.setStyleSheet(f"MainWindow{{background: {self.config.MainWindow['Background']}}}")

    def contextMenuEvent(self, e):
        """
        自定义鼠标右键事件，调出控制仪表盘
        """
        view = CommandBarView(self)

        test = Action(FIF.SHARE, 'Share')
        view.addAction(test)
        test.triggered.connect(lambda: print('分享'))
        view.addAction(Action(FIF.SAVE, 'Save'))
        view.addAction(Action(FIF.DELETE, 'Delete'))

        view.addHiddenAction(Action(FIF.SETTING, 'Settings', shortcut='Ctrl+S'))
        closeAction = Action(FIF.CLOSE, 'Close', shortcut='Ctrl+A')
        closeAction.triggered.connect(lambda: self.close())
        view.addHiddenAction(closeAction)
        view.resizeToSuitableWidth()

        Flyout.make(view, self, self, FlyoutAnimationType.FADE_IN)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 在鼠标按下时记录初始位置
            self.drag_start_position = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 在鼠标释放时清除初始位置
            self.drag_start_position = None

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            # 在鼠标按下并移动时执行拖拽操作
            if self.drag_start_position is not None:
                # 计算鼠标移动的偏移量
                offset = event.pos() - self.drag_start_position

                # 更新QWidget的位置
                new_position = self.pos() + offset
                self.move(new_position)
