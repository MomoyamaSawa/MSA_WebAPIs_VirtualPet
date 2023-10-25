from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys,argparse
from presentation.view.window import MainWindow
from util.databaseCreate import checkDatabase
from util.tools import cmdErrStr

def main(args):
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("同济软院2023秋MSA课设多功能桌宠_2151641_王佳垚")
    w.show()
    w.initLive2d()
    checkDatabase()

    if args.open_cmd:
        w.open_cmd()

    app.exec()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--open-cmd", action="store_true", help="打开 cmd")
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        err = "PyQt6: " + e.__class__.__name__ + " " + str(e)
        print(cmdErrStr(err))
        sys.exit(-1)
