# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'socket.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(695, 502)
        self.pushButton_font = QtWidgets.QPushButton(Form)
        self.pushButton_font.setGeometry(QtCore.QRect(230, 280, 93, 71))
        self.pushButton_font.setObjectName("pushButton_font")
        self.pushButton_back = QtWidgets.QPushButton(Form)
        self.pushButton_back.setGeometry(QtCore.QRect(240, 390, 93, 71))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_right = QtWidgets.QPushButton(Form)
        self.pushButton_right.setGeometry(QtCore.QRect(370, 390, 93, 71))
        self.pushButton_right.setObjectName("pushButton_right")
        self.pushButton_left = QtWidgets.QPushButton(Form)
        self.pushButton_left.setGeometry(QtCore.QRect(100, 390, 93, 71))
        self.pushButton_left.setObjectName("pushButton_left")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(135, 41, 281, 211))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        self.pushButton_font.clicked.connect(Form.font)
        self.pushButton_left.clicked.connect(Form.left)
        self.pushButton_back.clicked.connect(Form.back)
        self.pushButton_right.clicked.connect(Form.right)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_font.setText(_translate("Form", "前"))
        self.pushButton_back.setText(_translate("Form", "后"))
        self.pushButton_right.setText(_translate("Form", "右"))
        self.pushButton_left.setText(_translate("Form", "左"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
