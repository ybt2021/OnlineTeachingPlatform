from asyncio import subprocess
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import subprocess


class MyThread(QtCore.QThread):  # 定义一个工作线程，后面会调用和重写
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    my_str = pyqtSignal(int)
    ip = "192.168.223.128:1935"

    def run(self):  # 线程启动后会自动执行,这里是逻辑实现的代码
        self.finishSignal.emit(int)  # 发射信号


class shareDesktopThread(MyThread):
    ff_str = "ffmpeg -y -rtbufsize 20M -f gdigrab -i desktop -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv rtmp://"
    roomid = ""
    userid = ""
    live_video = ""

    def __init__(self, roomid, userid):
        super(MyThread, self).__init__()
        self.roomid = roomid
        self.userid = userid

    def buildStr(self):
        return self.ff_str+MyThread.ip+"/myapp/"+self.roomid+self.userid+"Screen"

    def run(self):
        appstr = self.buildStr()
        self.live_video = subprocess.Popen(
            appstr, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop(self):
        self.live_video.stdin.write('q'.encode("GBK"))
        self.live_video.communicate()


class openMicoThread(MyThread):
    ff_str = "ffmpeg -y -rtbufsize 20M -f dshow -i audio=\"麦克风阵列 (英特尔® 智音技术)\" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv rtmp://"
    roomid = ""
    userid = ""
    live_video = ""

    def __init__(self, roomid, userid):
        super(MyThread, self).__init__()
        self.roomid = roomid
        self.userid = userid

    def bulidStr(self):
        return self.ff_str+MyThread.ip+"/myapp/"+self.roomid+self.userid

    def run(self):
        appstr = self.bulidStr()
        self.live_video = subprocess.Popen(
            appstr, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop(self):
        self.live_video.stdin.write('q'.encode("GBK"))
        self.live_video.communicate()


class shareVedioThread(MyThread):
    ff_str = "ffmpeg  -y -rtbufsize 20M -f dshow -i video=\"FaceTime HD Camera (Built-in)\" -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -f flv rtmp://"
    roomid = ""
    userid = ""
    live_video = ""

    def __init__(self, roomid, userid):
        super(MyThread, self).__init__()
        self.roomid = roomid
        self.userid = userid

    def bulidStr(self):
        return self.ff_str+MyThread.ip+"/myapp/"+self.roomid+self.userid+"Video"

    def run(self):
        appstr = self.bulidStr()
        self.live_video = subprocess.Popen(
            appstr, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop(self):
        self.live_video.stdin.write('q'.encode("GBK"))
        self.live_video.communicate()
