from PyQt5.Qt import *
from qt_client.socket_ui import Ui_Form
import socket
import threading


class Window(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.resize(500, 500)
        self.setupUi(self)
        self.socket_init()
        # self.thread1 = threading.Thread(target=self.socket_init,name='thread1')
        # self.thread1.start()

    def socket_init(self):
        self.ip_addr = 'localhost'
        self.port = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client)
        self.client.connect((self.ip_addr, self.port))

    def left(self):
        self.data = self.pushButton_left.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def back(self):
        self.data = self.pushButton_back.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def right(self):
        self.data = self.pushButton_right.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据

    def font(self):
        self.data = self.pushButton_font.text()
        self.client.send(self.data.encode('utf-8'))  # 发送数据
        self.data = self.client.recv(1024)  # 接收数据


if __name__ == '__main__':
# 创建一个应用程序对象
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())








