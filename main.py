import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
import datetime
from completed import Ui_finished as finished
from pathlib import Path
from OKVED import OKVEDload
from load106 import load106
from proba import load107

okvedl = OKVEDload()
l106 = load106()
proba = load107()



class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, OKVEDload):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.browse_folder)
        self.load106.clicked.connect(self.showDialog)
        
        

    def browse_folder(self): # Событие загрузки файлов ОКВЭД
        okvedl.loadInSite()
        # self.infoBlok.setText('Вывести возможные ошибки') 
        self.on_finished()

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