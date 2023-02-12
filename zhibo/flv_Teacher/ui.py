# from cgitb import handler
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from thread import *
import ViewPage


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(3000, 1800)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.channel = QWebChannel()
        handler = CallHandler()
        self.channel.registerObject('PyHandler', handler)
        self.view = WebEngine()
        self.view.page().setWebChannel(self.channel)
        self.view.show()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class CallHandler(QObject):

    def __init__(self):
        super(CallHandler, self).__init__()

    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def init_home(self, str_args):
        print('call received')
        print('resolving......init home..')
        print(str_args)  # 查看参数
        code, roomid, userid = str_args.split("|")
        code = int(code)
        if int(code) == 1:
            self.whiteboard()
        elif int(code) == 2:
            self.shareDesktop(roomid, userid)
        elif int(code) == 3:
            self.openMico(roomid, userid)
        elif int(code) == 4:
            self.sharevideo(roomid, userid)
        elif int(code) == 5:
            self.quitShareDesktop()
        elif int(code) == 6:
            self.closeMico()
        elif int(code) == 7:
            self.closeVideo()
        elif int(code) == 8:
            url_string = 'http://localhost:8888/live/userid='+userid+'/roomid='+roomid   # 加载本地html文件
            ViewPage.view1.load(QUrl(url_string))
            ViewPage.view1.show()
        return 'hello, Python'

    def shareDesktop(self, roomid, userid):
        roomidstr = "room"+roomid
        useridstr = "user"+userid
        self.thread_1 = shareDesktopThread(roomid=roomidstr, userid=useridstr)
        self.thread_1.start()

    def openMico(self, roomid, userid):
        roomidstr = "room"+roomid
        useridstr = "user"+userid
        self.thread_2 = openMicoThread(roomid=roomidstr, userid=useridstr)
        self.thread_2.start()

    def sharevideo(self, roomid, userid):
        roomidstr = "room"+roomid
        useridstr = "user"+userid
        self.thread_3 = shareVedioThread(roomid=roomidstr, userid=useridstr)
        self.thread_3.start()

    def whiteboard(self):
        # self.qwebengine.load(QUrl("http://127.0.0.1:8888/whiteboardIndex"))
        pass

    def quitShareDesktop(self):
        self.thread_1.stop()
        self.thread_1.terminate()

    def closeMico(self):
        self.thread_2.stop()
        self.thread_2.terminate()

    def closeVideo(self):
        self.thread_3.stop()
        self.thread_3.terminate()


class WebEngine(QWebEngineView):

    def __init__(self):
        super(WebEngine, self).__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 设置右键菜单规则为自定义右键菜单

        self.setWindowTitle('直播间·教师端')
        self.resize(1750, 1100)

    def closeEvent(self, evt):
        self.page().profile().clearHttpCache()  # 清除QWebEngineView的缓存
        super(WebEngine, self).closeEvent(evt)
