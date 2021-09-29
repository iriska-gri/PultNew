# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(229, 301)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.OKVED = QtWidgets.QPushButton(self.centralwidget)
        self.OKVED.setGeometry(QtCore.QRect(10, 110, 75, 23))
        self.OKVED.setObjectName("OKVED")
        self.infoBlok = QtWidgets.QTextBrowser(self.centralwidget)
        self.infoBlok.setGeometry(QtCore.QRect(10, 10, 201, 81))
        self.infoBlok.setObjectName("infoBlok")
        self.load106 = QtWidgets.QPushButton(self.centralwidget)
        self.load106.setGeometry(QtCore.QRect(10, 140, 75, 23))
        self.load106.setObjectName("load106")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.OKVED.setText(_translate("MainWindow", "OKVED"))
        self.load106.setText(_translate("MainWindow", "106"))
