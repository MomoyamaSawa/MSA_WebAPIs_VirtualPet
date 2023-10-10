from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from util.config import GlobalConfig
from qfluentwidgets import (PushButton, TeachingTip, TeachingTipTailPosition, InfoBarIcon, setTheme, Theme,
                            TeachingTipView, FlyoutViewBase, BodyLabel, PrimaryPushButton, PopupTeachingTip)

class Panel(QFrame):
    """
    桌宠程序的仪表盘
    """

    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.hBoxLayout = QHBoxLayout(self)

        self._initUI()
        self._initQss()
        self._initLayout()

    def _initUI(self):
        self.button1 = PushButton('test1', self)
        self.button1.clicked.connect(self.showTip)
        self.button2 = PushButton('test2', self)
        self.button3 = PushButton('test3', self)

    def _initLayout(self):
        self.setLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignmentFlag.AlignHCenter)
        self.hBoxLayout.addWidget(self.button3, 0, Qt.AlignmentFlag.AlignHCenter)

    def showTip(self):
        position = TeachingTipTailPosition.BOTTOM
        view = TeachingTipView(
            icon=None,
            title='Lesson 5',
            content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
            image='resource/test.jpg',
            isClosable=True,
            tailPosition=position,
        )

        # add widget to view
        button = PushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        tip = TeachingTip.make(
            view, target=self.button1, duration=-1, tailPosition=position, parent=self)
        view.closed.connect(tip.close)

    def _initQss(self):
        self.setStyleSheet(f"""
            Panel {{
                background: {self.config.Panel['Background']};
                border: {self.config.Panel['Border']};
                border-radius: {self.config.Panel['BorderRadius']};
            }}
        """)
