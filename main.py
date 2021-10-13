import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design  # Это наш конвертированный файл дизайна
import datetime
from completed import Ui_finished as finished
from pathlib import Path
from OKVED import OKVEDload
from okv import OKVEDmanual
from load106 import load106
from proba import load107

ol = OKVEDmanual()
okvedl = OKVEDload()
l106 = load106()
proba = load107()



class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, OKVEDload):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.on_radio_button_clicked)
        self.load106.clicked.connect(self.showDialog)
        self.textEdit.setReadOnly(True)
        # self.textEdit.setBackgroundVisible(QtGui.QColor(124, 124, 134))
        # self.textEdit.setBackgroundVisible(False)
        self.RadioManualInput.toggled.connect(self.on_radio_color) # Выбор заливки ОКВЕД в ручную или с сайта
        # self.textEdit.textChanged.connect(self.magik)

    def on_radio_color(self): # Выбирает цвет для ввода данных
        if self.RadioManualInput.isChecked(): 
            self.textEdit.setReadOnly(False)
            self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255)")
        else:
            self.textEdit.setStyleSheet("background-color: rgb(229, 229, 229)")
            self.textEdit.setReadOnly(True)

    def on_radio_button_clicked(self): # Выбирает загрузку ОКВЭД вручную или с сайта
        if self.RadioManualInput.isChecked():
            self.OKVEDmanual()
        else:
            self.OKVEDsait()
        
    def OKVEDsait(self):
        okvedl.loadInSite()
        self.on_finished()

    def OKVEDmanual(self): # Событие загрузки файлов ОКВЭД
        text = self.textEdit.toPlainText() 
        pathhome = Path.home()
        name = QtWidgets.QFileDialog.getOpenFileName(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),) 
        ol.loadSite(str(name[0]), int(text)-1)


    def showDialog(self): # Открыть окно выбора файла
        # pathhome = Path.home()
        # name = QtWidgets.QFileDialog.getOpenFileName(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),) 
        # l106.opencsv(str(name[0]))
        # self.on_finished()
        proba.opencsv()



    def on_finished(self): # Завершение дествия
        dialog = QtWidgets.QDialog()
        dialog.ui = finished()
        dialog.ui.setupUi(dialog)
        dialog.ui.pushButton.clicked.connect(dialog.close)
        dialog.exec_() 

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show() 
    app.exec_() 

if __name__ == '__main__':
    main()