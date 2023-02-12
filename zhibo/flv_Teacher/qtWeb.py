import sys
from tkinter.messagebox import showerror
from PyQt5 import QtWidgets
from ui import Ui_Form, CallHandler, WebEngine

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel
import ViewPage


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ViewPage.view1 = WebEngine()
    channel1 = QWebChannel()
    handler1 = CallHandler()
    channel1.registerObject('PyHandler', handler1)
    ViewPage.view1.page().setWebChannel(channel1)  # 挂载前端处理对象

    view2 = WebEngine()
    channel2 = QWebChannel()
    handler2 = CallHandler()
    channel2.registerObject('PyHandler', handler2)
    view2.page().setWebChannel(channel2)  # 挂载前端处理对象

    url_string = 'http://localhost:8888'   # 加载本地html文件
    view2.load(QUrl(url_string))
    view2.resize(1000, 500)
    view2.show()

    sys.exit(app.exec_())
