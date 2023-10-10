from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import json
from util.config import GlobalConfig
from presentation.view.window import MainWindow


if __name__ == "__main__":

    # 这个配置的初始化要在很多操作之前，比如数据库的初始化就要用到全局配置
    with open("config.json") as file:
        file_content = file.read()
        configData = json.loads(file_content)
    config = GlobalConfig(**configData)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("同济软院2023秋MSA课设多功能桌宠_2151641_王佳垚")
    w.show()
    app.exec()
