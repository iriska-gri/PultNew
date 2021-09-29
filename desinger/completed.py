# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'completed.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_finished(object):
    def setupUi(self, finished):
        finished.setObjectName("finished")
        finished.resize(685, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(finished.sizePolicy().hasHeightForWidth())
        finished.setSizePolicy(sizePolicy)
        finished.setMinimumSize(QtCore.QSize(685, 300))
        finished.setMaximumSize(QtCore.QSize(685, 300))
        self.pushButton = QtWidgets.QPushButton(finished)
        self.pushButton.setGeometry(QtCore.QRect(280, 260, 141, 23))
        self.pushButton.setObjectName("pushButton")
        self.messagefinish = QtWidgets.QLabel(finished)
        self.messagefinish.setGeometry(QtCore.QRect(70, 50, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.messagefinish.setFont(font)
        self.messagefinish.setText("")
        self.messagefinish.setObjectName("messagefinish")
        self.line = QtWidgets.QFrame(finished)
        self.line.setGeometry(QtCore.QRect(0, 130, 691, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(finished)
        self.label.setGeometry(QtCore.QRect(210, 30, 281, 91))
        self.label.setObjectName("label")

        self.retranslateUi(finished)
        QtCore.QMetaObject.connectSlotsByName(finished)

    def retranslateUi(self, finished):
        _translate = QtCore.QCoreApplication.translate
        finished.setWindowTitle(_translate("finished", "Операция завершена"))
        self.pushButton.setText(_translate("finished", "OK"))
        self.label.setText(_translate("finished", "Загрузка ОКВЭД выполнена успешно. Давай еще раз"))
