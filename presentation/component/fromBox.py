from qfluentwidgets import LineEdit,ComboBox,PrimaryPushButton,PushButton,FlowLayout
from PyQt6.QtWidgets import *
from util.config import GlobalConfig
from PyQt6.QtCore import *
from PyQt6.QtGui import QFont
from functools import partial

class FromBox(QFrame):

    fromContentSignal = pyqtSignal(str,list)

    def __init__(self,title,content,options:list[list]=None):
        super().__init__()
        self.setFixedWidth(GlobalConfig().Panel['Width'])
        self.label = QLabel(title)
        font = QFont("Arial", 21)
        self.label.setFont(font)
        self.boxlayout = QHBoxLayout()
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText(content)
        self.viewLayout = QVBoxLayout()
        self.yes = PrimaryPushButton("确定")
        self.yes.clicked.connect(self._yes)
        self.cancel = PushButton("取消")
        self.cancel.clicked.connect(self.hide)

        self.flowLayout = FlowLayout(needAni=True)
        self.flowLayout.setAnimation(250, QEasingCurve.Type.OutQuad)
        # self.flowLayout.setContentsMargins(30, 30, 30, 30)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        self.comboBoxs = []
        self.getArr = []
        num = -1
        if options is not None:
            for option in options:
                num = num + 1
                comboBox = ComboBox(self)
                comboBox.addItems(option)
                comboBox.setCurrentIndex(0)
                comboBox.currentTextChanged.connect(lambda :self._get(num,comboBox.currentIndex()))
                self.comboBoxs.append(comboBox)
            self.getArr = [0 for _ in range(len(options))]

        self._initLayout()
        self._initQSS()

    def _get(self,num,index):
        self.getArr[num] = index

    def _yes(self):
        self.fromContentSignal.emit(self.lineEdit.text(),self.getArr)
        self.hide()

    def _initLayout(self):
        self.setLayout(self.viewLayout)
        self.viewLayout.addWidget(self.label,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        for comboBox in self.comboBoxs:
            self.flowLayout.addWidget(comboBox)
        self.viewLayout.addLayout(self.flowLayout)
        self.boxlayout.addWidget(self.lineEdit)
        self.boxlayout.addWidget(self.yes)
        self.boxlayout.addWidget(self.cancel)
        self.viewLayout.addLayout(self.boxlayout)

    def _initQSS(self):
        self.setStyleSheet(f"""
            FromBox {{
                background: {GlobalConfig().Panel['Background']};
                border: {GlobalConfig().Panel['Border']};
                border-radius: {GlobalConfig().Panel['BorderRadius']};
            }}
        """)


class FromSelectBox(QFrame):

    fromSelectSignal = pyqtSignal(str,str)

    def __init__(self,title,indexs:list,contents:list[str]):
        super().__init__()
        self.setFixedWidth(GlobalConfig().Panel['Width'])
        self.label = QLabel(title)
        font = QFont("Arial", 21)
        self.label.setFont(font)
        self.contents = contents
        self.indexs = indexs
        self.labels = []

        self.viewLayout = QVBoxLayout()
        self.flowLayout = FlowLayout(needAni=True)
        self.flowLayout.setContentsMargins(10, 5, 10, 10)
        self.flowLayout.setAnimation(250, QEasingCurve.Type.OutQuad)
        self.flowLayout.setVerticalSpacing(10)
        self.flowLayout.setHorizontalSpacing(10)

        self._initLayout()
        self._initQSS()

    def _initLayout(self):
        self.setLayout(self.viewLayout)
        self.viewLayout.addWidget(self.label,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        i = -1
        for content in self.contents:
            i = i + 1
            label = PushButton(content)
            # 注意这里用partial
            label.clicked.connect(partial(self._yes, self.indexs[i],content))
            self.flowLayout.addWidget(label)
            self.labels.append(label)
        self.viewLayout.addLayout(self.flowLayout)


    def _yes(self,index,content):
        self.fromSelectSignal.emit(index,content)
        self.hide()

    def _initQSS(self):
        self.setStyleSheet(f"""
            FromSelectBox {{
                background: {GlobalConfig().Panel['Background']};
                border: {GlobalConfig().Panel['Border']};
                border-radius: {GlobalConfig().Panel['BorderRadius']};
            }}
        """)


