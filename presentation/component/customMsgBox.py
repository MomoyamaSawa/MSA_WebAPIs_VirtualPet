from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit,ComboBox,PrimaryPushButton,PushButton,FlowLayout
from PyQt6.QtWidgets import *
from util.config import GlobalConfig
from PyQt6.QtCore import *
from PyQt6.QtGui import QFont

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, fa,title,content):
        super().__init__(fa)
        self.titleLabel = SubtitleLabel(title, self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText(content)
        self.urlLineEdit.setClearButtonEnabled(True)

        self.type = None
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.urlLineEdit.textChanged.connect(self._check)

        # self.hideYesButton()

    def _check(self, text):
        if text != "":
            self.yesButton.setEnabled(True)

    def _get(self,type):
        self.type = type

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


# TODO 这边之后搞继承来增加多选框吧
class AIDrawMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, fa,title,content):
        super().__init__(fa)
        self.titleLabel = SubtitleLabel(title, self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText(content)
        self.urlLineEdit.setClearButtonEnabled(True)

        optionsStyle = [
            '探索无限',
            '古风',
            '二次元',
            '写实风格',
            '浮世绘',
            'low poly',
            '未来主义',
            '像素风格',
            '概念艺术',
            '赛博朋克',
            '洛丽塔风格',
            '巴洛克风格',
            '超现实主义',
            '水彩画',
            '蒸汽波艺术',
            '油画',
            '卡通画'
        ]
        self.styleAI = optionsStyle[0]
        self.comboBoxStyle = ComboBox(self)
        self.comboBoxStyle.addItems(optionsStyle)
        self.comboBoxStyle.setCurrentIndex(0)
        self.comboBoxStyle.currentTextChanged.connect(self._getStyle)

        optionsRadio = [
            '1:1',
            '3:2',
            '2:3'
        ]
        self.radio = optionsRadio[0]
        self.comboBoxRadio = ComboBox(self)
        self.comboBoxRadio.addItems(optionsRadio)
        self.comboBoxRadio.setCurrentIndex(0)
        self.comboBoxRadio.currentTextChanged.connect(self._getRadio)

        # add widget to view layout
        self.hBoxLayout = QHBoxLayout()
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.hBoxLayout.addWidget(self.comboBoxRadio)
        self.hBoxLayout.addWidget(self.comboBoxStyle)
        self.viewLayout.addLayout(self.hBoxLayout)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.urlLineEdit.textChanged.connect(self._check)

        # self.hideYesButton()

    def _check(self, text):
        if text != "":
            self.yesButton.setEnabled(True)

    def _getStyle(self,type):
        self.styleAI = type

    def _getRadio(self,type):
        self.radio = type
