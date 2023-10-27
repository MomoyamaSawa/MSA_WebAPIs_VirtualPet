from PyQt6.QtWidgets import QApplication
import sys
from presentation.view.window import MainWindow
from util.databaseCreate import checkDatabase
from util.tools import cmdErrStr

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("同济软院2023秋MSA课设多功能桌宠_2151641_王佳垚")
    w.show()
    w.initLive2d()
    checkDatabase()

    app.exec()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        err = "PyQt6: " + e.__class__.__name__ + " " + str(e)
        print(cmdErrStr(err))
        sys.exit(-1)
