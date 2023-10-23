from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys, threading
from presentation.view.window import MainWindow
from util.live2D import createLive2D


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("同济软院2023秋MSA课设多功能桌宠_2151641_王佳垚")
    w.show()
    w.initLive2d()
    app.exec()
