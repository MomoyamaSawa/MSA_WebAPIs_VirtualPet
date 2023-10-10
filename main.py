from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import json
from util.config import GlobalConfig
from presentation.view.window import MainWindow


if __name__ == "__main__":

    # 读取配置文件，初始化一个全局配置单例对象

    with open("config.json") as file:
        file_content = file.read()
        configData = json.loads(file_content)

    config = GlobalConfig(**configData)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("同济软院2023秋MSA课设多功能桌宠_2151641_王佳垚")
    w.show()
    app.exec()
