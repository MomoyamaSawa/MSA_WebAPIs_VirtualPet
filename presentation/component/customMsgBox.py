from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit,ComboBox
from PyQt6.QtWidgets import *

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, fa,title,content,options=None):
        super().__init__(fa)
        self.titleLabel = SubtitleLabel(title, self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText(content)
        self.urlLineEdit.setClearButtonEnabled(True)

        self.type = None
        if options is not None:
            self.type = options[0]
            self.comboBox = ComboBox(self)
            self.comboBox.addItems(options)
            self.comboBox.setCurrentIndex(0)
            self.comboBox.currentTextChanged.connect(self._get)
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        if options is not None:
            self.viewLayout.addWidget(self.comboBox)

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
