from qfluentwidgets import LineEdit,ComboBox,PrimaryPushButton,PushButton,FlowLayout
from PyQt6.QtWidgets import *
from util.config import GlobalConfig
from PyQt6.QtCore import *
from PyQt6.QtGui import QFont

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


# class OptionsFromBox(FromBox):
#     def __init__(self,title,content,options):
#         super.__init__(title,content)

#         for option in options:
#             ComboBox(self).addItems(option)
#             self.viewLayout.addWidget(option)

