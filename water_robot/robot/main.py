import socket
import traceback
import cv2
import psutil
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import *
from WaterRobot_ui import Ui_Form


class Window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.resize(500, 500)
        self.setupUi(self)
        self.all_init()

    def all_init(self):
        # self.t1 = threading.Thread(target=self.cam_init,name='t1')
        # self.t2 = threading.Thread(target=self.draw_init,name='t2')
        # self.t3 = threading.Thread(target=self.timer_sensor_init,name='t3')
        # self.t1.start()
        # self.t2.start()
        # self.t3.start()

        self.cam_init()
        self.draw_init()
        self.timer_sensor_init()

    def draw_init(self):
        self.graphicsView_waterdepth.showGrid(x=True,y=True)
        self.graphicsView_waterdepth.setYRange(min=0,max=100)
        self.datalist = []

    def timer_sensor_init(self):
        print('初始化定时器')
        self.timer_sensor= QtCore.QTimer()
        self.timer_sensor.timeout.connect(self.get_sensor_info)

        # self.timer_sensor.start(300)
        print('定时器启动')

    def get_sensor_info(self):
        # print('获取传感器数据')
        #因为暂时还没接传感器，所以使用cpu的数据来显示
        try:
            cpu = psutil.cpu_percent(interval=0.3) #每隔0.3秒获取一次数据和定时器设置的时间相同
            self.datalist.append(float(cpu))
            self.graphicsView_waterdepth.plot().setData(self.datalist, pen='g')
        except Exception as e:
            print(traceback.print_exc())

    def open_sensor(self):
        if self.timer_sensor.isActive():
            self.timer_sensor.stop()
            self.btn_sensor.setText('打开传感器')
        else:
            self.btn_sensor.setText('关闭传感器')
            self.timer_sensor.start(300)

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
            # self.btn_cam1.setText('打开前摄')

    def show_camera(self):
        size = str(self.label_cam1.size())
        self.cam_width = int(size[-9:-6])
        self.cam_height = int(size[-4:-1])
        flag, self.image = self.cap.read()  # 从视频流中读取一帧图像
        show = cv2.resize(self.image, (self.cam_width, self.cam_height))  # 把读到的帧的大小重新设置为 640x480
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
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client)
        self.client.connect((self.ip_addr, int(self.port)))  #进程会阻塞在这里,所以希望使用多线程解决这个问题
        print('已连接')

    def font(self):
        self.data = self.btn_font.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def back(self):
        self.data = self.btn_back.text()
        self.client.send(self.data.encode('utf-8'))
        self.data = self.client.recv(1024)

    def left(self):
        self.data = self.btn_left.text()
        self.client.send(self.data.encode('utf-8'))
        self.data = self.client.recv(1024)

    def right(self):
        self.data = self.btn_right.text()
        self.client.send(self.data.encode('utf-8'))
        self.data = self.client.recv(1024)

    def float(self):
        self.data = self.btn_float.text()
        self.client.send(self.data.encode('utf-8'))
        self.data = self.client.recv(1024)

    def dive(self):
        self.data = self.btn_dive.text()
        self.client.send(self.data.encode('utf-8'))
        self.data = self.client.recv(1024)


class Sensor(QObject):
    pass


if __name__ == '__main__':

# 创建一个应用程序对象
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())







