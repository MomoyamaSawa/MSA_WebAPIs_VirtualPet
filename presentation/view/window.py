from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from util.config import GlobalConfig
from presentation.component.panel import Panel

class MainWindow(QWidget):
    """
    桌宠程序的主界面
    """

    def __init__(self):
        super().__init__()
        self.config = GlobalConfig()
        self.resize(self.config.MainWindow["Weight"], self.config.MainWindow["Height"])
        self.hboxLayout = QHBoxLayout(self)

        self._initUI()
        self._initQss()
        self._initLayout()


    def _initUI(self):
        self.panel = Panel()
        self.panel.hide()

    def _initLayout(self):
        self.setLayout(self.hboxLayout)
        self.hboxLayout.addWidget(self.panel, 0, Qt.AlignmentFlag.AlignBottom)

    def _initQss(self):
        self.setStyleSheet(f"MainWindow{{background: {self.config.MainWindow['Background']}}}")

    def contextMenuEvent(self, event):
        """
        自定义鼠标右键事件，调出控制仪表盘
        """
        if not self.panel.isVisible():
            self.panel.show()
            self.panel.setFocus(Qt.FocusReason.MouseFocusReason)
        else:
            self.panel.hide()
