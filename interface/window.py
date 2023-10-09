from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from config import GlobalConfig

class MainWindow(QWidget):
    """
    桌宠程序的主界面
    """

    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.resize(self.config.MainWindow["Weight"], self.config.MainWindow["Height"])

        self._initQss()
        self._initLayout()

    def _initLayout(self):
        pass
        # self.setLayout(self.vBoxLayout)

        # self.vBoxLayout.addWidget(self.pivot)
        # self.vBoxLayout.addWidget(self.stackedWidget)
        # self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

    def _initQss(self):
        self.setStyleSheet(f"MainWindow{{background: {self.config.MainWindow['Background']}}}")
