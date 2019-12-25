from PyQt5.Qt import *
from WaterRobot_ui import Ui_Form
import socket
import threading
import cv2
from PyQt5 import QtCore, QtGui

class Window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.resize(500, 500)
        self.setupUi(self)
        self.cam_init()

    def cam_init(self):
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.timer_camera.timeout.connect(self.show_camera)
        self.CAM_NUM = 0

    def font_cam(self):
        print('打开前摄')
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                print('fail to open')
            else:
                self.timer_camera.start(30)
                self.btn_cma1.setText('关闭前摄')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_cam1.clear()
            self.btn_cam1.setText('打开前摄')
    def back_cam(self):
        print('后摄')
    def show_camera(self):
        flag, self.image = self.cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (446, 268))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label_cam1.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def open_light(self):
        print('打开灯光')
        self.data = self.btn_light.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def link_to_pi(self):
        print('连接到树莓派')
        self.ip_addr = self.lineEdit_ip.text()
        self.port = self.lineEdit_pwd.text()
        # print(self.ip_addr,type(self.port))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client)
        self.client.connect((self.ip_addr, int(self.port)))  #进程会阻塞在这里,所以希望使用多线程解决这个问题
        print('已连接')

    def font(self):
        print('前')
        self.data = self.btn_font.text()
        print(self.data, '1')
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        print(self.data, '2')
        self.data = self.client.recv(1024)  # 接收数据

    def back(self):
        print('后')
        self.data = self.btn_back.text()
        print(self.data, '1')
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        print(self.data, '2')
        self.data = self.client.recv(1024)  # 接收数据

    def left(self):
        print('左')
        self.data = self.btn_left.text()
        print(self.data, '1')
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        print(self.data, '2')
        self.data = self.client.recv(1024)  # 接收数据

    def right(self):
        print('右')
        self.data = self.btn_right.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def float(self):
        print('上浮')
        self.data = self.btn_float.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def dive(self):
        print('下潜')
        self.data = self.btn_dive.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据
if __name__ == '__main__':
# 创建一个应用程序对象
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())







