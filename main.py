import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import desinger.design  # Это наш конвертированный файл дизайна
import datetime
from OKVED import OKVEDload
from desinger.completed import Ui_finished as finished
from pathlib import Path

okvedl = OKVEDload()



class ExampleApp(QtWidgets.QMainWindow, desinger.design.Ui_MainWindow, OKVEDload):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.browse_folder)
        self.load106.clicked.connect(self.showDialog)
        
        

    def browse_folder(self): # Событие загрузки файлов ОКВЭД
        okvedl.loadInSite()
        self.textBrowser.setText('Вывести возможные ошибки') 
        self.on_finished()

    def showDialog(self): # Открыть окно выбора файла
        pathhome = Path.home()
        name = QtWidgets.QFileDialog.getOpenFileName(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),) 
        # a = windoww.setText(str(name[0]))
        print(str(name[0]))


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