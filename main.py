import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
# from PyQt5 import QtCore, QtGui
import design  # Это наш конвертированный файл дизайна
from completed import Ui_finished as finished
from pathlib import Path
from OKVEDmanual import OKVEDmanual
from load106 import load106
from VScomp import VScomp

vs = VScomp()

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        VScomp.__init__(self)

        
        
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.on_radio_button_clicked)
        self.load106.clicked.connect(self.showDialog)
        self.checkManual.toggled.connect(self.on_radio_zagruzka)
        self.chekUpdate.toggled.connect(self.on_radio_Data)

# ------------------------------------------------------------------------------------------------------- ОКВЭД

    def on_radio_Data(self): # Выбор обновления дат данных ОКВЭД
        if self.chekUpdate.isChecked(): 
            self.dateEnd.setReadOnly(False)
            self.dateStart.setReadOnly(False)
            self.dateEnd.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.dateStart.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.checkManual.setEnabled(False)
        else:
            self.dateEnd.setReadOnly(True)
            self.dateStart.setReadOnly(True)
            self.dateEnd.setStyleSheet("background-color: rgb(229, 229, 229)")
            self.dateStart.setStyleSheet("background-color: rgb(229, 229, 229)")
            self.checkManual.setEnabled(True)

    def on_radio_zagruzka(self):
        if self.checkManual.isChecked(): 
            self.chekUpdate.setEnabled(False)
        else:
            self.chekUpdate.setEnabled(True)

    def on_radio_button_clicked(self): # Выбирает загрузку ОКВЭД вручную или с сайта
        if self.checkManual.isChecked():   
            self.OKVEDhand()
        else:
            # self.OKVEDsait()
            print('В работе')
           

    # def OKVEDsait(self):
    #     okvedm = OKVEDmanual()
    #     okvedm.loadSite()
    #     self.on_finished()

    def OKVEDhand(self): # Событие загрузки файлов ОКВЭД с автоматическим вводом строк
        self.showDialog()
        for x in range(len(self.nameDialogs[0])):
            okvedm = OKVEDmanual(self.myBDokved)
            okvedm.loadSite(str(self.nameDialogs[0][x]))
        self.on_finished()
        
    
    # def OKVEDupdate(self):
    #     temp_varStart = self.dateStart.date() 
    #     var_nameStart = temp_varStart.toPyDate()
    #     temp_varEnd = self.dateEnd.date() 
    #     var_nameEnd = temp_varEnd.toPyDate()
    #     if var_nameEnd < var_nameStart:
    #         var_End = var_nameStart
    #         self.dateEnd.setDate(temp_varStart)
    #     else:
    #         var_End = temp_varEnd.toPyDate()
    #     table = [self.tablemsp, self.tablenp]
    #     for x in table:
    #         orm.SQLOkved(orm.DeleteWhere(x, 'datelikedale', var_nameStart, var_End))
    #     print("Обновляемый период с {} по {}".format(var_nameStart, var_End))

# ------------------------------------------------------------------------------------------------------- Техническая часть

    def showDialog(self): # Открыть окно выбора файла
        pathhome = Path.home()
        self.nameDialogs = QtWidgets.QFileDialog.getOpenFileNames(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),) #QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if self.sender().objectName() == 'load106':
            l106 = load106(self.myBD)
            l106.opencsv(self.nameDialogs[0][0])
            self.on_finished()
        else:
            pass

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