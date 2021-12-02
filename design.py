# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(598, 301)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.load106 = QtWidgets.QPushButton(self.centralwidget)
        self.load106.setGeometry(QtCore.QRect(10, 100, 75, 31))
        self.load106.setObjectName("load106")
        self.OKVED = QtWidgets.QPushButton(self.centralwidget)
        self.OKVED.setGeometry(QtCore.QRect(10, 30, 75, 51))
        self.OKVED.setObjectName("OKVED")
        self.dateStart = QtWidgets.QDateEdit(self.centralwidget)
        self.dateStart.setGeometry(QtCore.QRect(320, 50, 111, 31))
        self.dateStart.setStyleSheet("background-color: rgb(229, 229, 229)")
        self.dateStart.setReadOnly(True)
        self.dateStart.setDateTime(QtCore.QDateTime(QtCore.QDate(2021, 10, 12), QtCore.QTime(0, 0, 0)))
        self.dateStart.setDate(QtCore.QDate(2021, 10, 12))
        self.dateStart.setObjectName("dateStart")
        self.dateEnd = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEnd.setGeometry(QtCore.QRect(460, 50, 111, 31))
        self.dateEnd.setStyleSheet("background-color: rgb(229, 229, 229)")
        self.dateEnd.setReadOnly(True)
        self.dateEnd.setDate(QtCore.QDate(2021, 1, 1))
        self.dateEnd.setObjectName("dateEnd")
        self.chekUpdate = QtWidgets.QCheckBox(self.centralwidget)
        self.chekUpdate.setEnabled(True)
        self.chekUpdate.setGeometry(QtCore.QRect(90, 61, 211, 20))
        self.chekUpdate.setIconSize(QtCore.QSize(1, 1))
        self.chekUpdate.setCheckable(True)
        self.chekUpdate.setChecked(False)
        self.chekUpdate.setAutoRepeat(False)
        self.chekUpdate.setObjectName("chekUpdate")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(445, 50, 21, 31))
        self.label.setObjectName("label")
        self.checkManual = QtWidgets.QCheckBox(self.centralwidget)
        self.checkManual.setEnabled(True)
        self.checkManual.setGeometry(QtCore.QRect(90, 30, 242, 17))
        self.checkManual.setStyleSheet("")
        self.checkManual.setObjectName("checkManual")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 80, 581, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 10, 581, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_All_bez_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_All_bez_back.setGeometry(QtCore.QRect(90, 100, 81, 31))
        self.pushButton_All_bez_back.setStyleSheet("background-color: rgb(200, 169, 96)")
        self.pushButton_All_bez_back.setObjectName("pushButton_All_bez_back")
        self.pushButton_Sroki_svod = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Sroki_svod.setGeometry(QtCore.QRect(180, 100, 81, 31))
        self.pushButton_Sroki_svod.setStyleSheet("background-color: rgb(200, 169, 96)")
        self.pushButton_Sroki_svod.setObjectName("pushButton_Sroki_svod")
        self.pushButton_Daschbord_Sroki_svod = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Daschbord_Sroki_svod.setGeometry(QtCore.QRect(270, 100, 141, 31))
        self.pushButton_Daschbord_Sroki_svod.setStyleSheet("background-color: rgb(85, 170, 127)")
        self.pushButton_Daschbord_Sroki_svod.setObjectName("pushButton_Daschbord_Sroki_svod")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load106.setText(_translate("MainWindow", "106"))
        self.OKVED.setText(_translate("MainWindow", "OKVED"))
        self.chekUpdate.setText(_translate("MainWindow", "Обновить данные ОКВЕД за период"))
        self.label.setText(_translate("MainWindow", "-"))
        self.checkManual.setText(_translate("MainWindow", "Загрузка файлов вручную"))
        self.pushButton_All_bez_back.setText(_translate("MainWindow", "All_bez_back"))
        self.pushButton_Sroki_svod.setText(_translate("MainWindow", "Sroki_svod"))
        self.pushButton_Daschbord_Sroki_svod.setText(_translate("MainWindow", "Дашборд Sroki_svod"))
