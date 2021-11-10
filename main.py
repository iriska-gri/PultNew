import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import design  # Это наш конвертированный файл дизайна
import datetime
from completed import Ui_finished as finished
from pathlib import Path
from OKVEDsait import OKVEDload
from OKVEDmanual import OKVEDmanual
from OKVEDmanualstroki import OKVEDmanualsrt
from load106 import load106
from proba import load107
from settings.conn import Orm
import time

orm = Orm()
okvedstr = OKVEDmanualsrt()
okvedm = OKVEDmanual()
okvedl = OKVEDload()
l106 = load106()
proba = load107()




class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow, OKVEDload):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.on_radio_button_clicked)
        self.load106.clicked.connect(self.showDialog1)
        # self.dateEnd.setReadOnly(True)
        # self.dateStart.setReadOnly(True)
        self.checkStroki.toggled.connect(self.on_radio_Stroki) # Активация окна ввода строк вручную
        self.chekUpdate.toggled.connect(self.on_radio_Data)
        self.pushButton.clicked.connect(self.delete)





        if self.usering == 'systemsupport':
            self.tablemsp = 'viruzka_msp'
            self.tablenp = 'viruzka_np'
            self.myBD = "okved"
        else:
            self.tablemsp = 'Viruzka_MSP'
            self.tablenp = 'Viruzka_NP'
            self.myBD = "OKVED"


# ------------------------------------------------------------------------------------------------------- ОКВЭД

    def on_radio_Stroki(self): # Выбирает цвет для ввода данных
        if self.checkStroki.isChecked(): 
            self.textEdit.setReadOnly(False)
            self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255)")
        else:
            self.textEdit.setReadOnly(True)
            self.textEdit.setStyleSheet("background-color: rgb(229, 229, 229)")
            

    def on_radio_Data(self): # Выбор обновления дат данных ОКВЭД
        if self.chekUpdate.isChecked(): 
            self.dateEnd.setReadOnly(False)
            self.dateStart.setReadOnly(False)
            self.dateEnd.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.dateStart.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.checkStroki.setEnabled(False)
            self.checkManual.setEnabled(False)
        else:
            self.dateEnd.setReadOnly(True)
            self.dateStart.setReadOnly(True)
            self.dateEnd.setStyleSheet("background-color: rgb(229, 229, 229)")
            self.dateStart.setStyleSheet("background-color: rgb(229, 229, 229)")
            self.checkStroki.setEnabled(True)
            self.checkManual.setEnabled(True)

    def delete(self):
        if (self.chekUpdate.isChecked()):
            self.OKVEDupdate()

    def on_radio_button_clicked(self): # Выбирает загрузку ОКВЭД вручную или с сайта
        # if (self.chekUpdate.isChecked()):
        #     self.OKVEDsait()
        if (self.checkManual.isChecked() and self.checkStroki.isChecked()):
            self.OKVEDmanualstroki() 
        elif self.checkManual.isChecked():   
            self.OKVEDmanual()
        else:
            self.OKVEDsait()


            

    def OKVEDsait(self):
        okvedl.loadInSite()
        self.on_finished()

    def OKVEDmanual(self): # Событие загрузки файлов ОКВЭД с автоматическим вводом строк
        self.showDialog1()
        for x in range(len(self.nameDialogs[0])):
            # print(self.nameDialogs[0][x])
            okvedm.loadSite(str(self.nameDialogs[0][x]))
        self.on_finished()

    def OKVEDmanualstroki(self): # Событие загрузки файлов ОКВЭД с ручныым вводом строк
        text = self.textEdit.toPlainText() 
        self.showDialog1()
        for x in range(len(self.nameDialogs[0])):
            # print(self.nameDialogs[0][x])
            okvedstr.loadSite(str(self.nameDialogs[0][x]), int(text)-1)
        self.on_finished()
    
    def OKVEDupdate(self):
        temp_varStart = self.dateStart.date() 
        var_nameStart = temp_varStart.toPyDate()
        temp_varEnd = self.dateEnd.date() 
        var_nameEnd = temp_varEnd.toPyDate()
        if var_nameEnd < var_nameStart:
            var_End = var_nameStart
            self.dateEnd.setDate(temp_varStart)
        else:
            var_End = temp_varEnd.toPyDate()
        table = [self.tablemsp, self.tablenp]
        for x in table:
            orm.DeleteWhere(x, 'datelikedale', var_nameStart, var_End)
        # orm.connclose()
        print("Обновляемый период с {} по {}".format(var_nameStart, var_End))
        

       

# ------------------------------------------------------------------------------------------------------- Техническая часть

    def showDialog1(self): # Открыть окно выбора файла
        pathhome = Path.home()
        # name = QtWidgets.QFileDialog.getOpenFileNames(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),)
        self.nameDialogs = QtWidgets.QFileDialog.getOpenFileNames(None, 'Выбор файла', str(pathhome.joinpath('Desktop')),)
        # f = r'C:/Users/systemsupport/Desktop/report106_1000005103_20211005_081401.csv'
        # print(f"""'{str(self.nameDialogs[0][0])}'""")
        # print()
        # print(self.nameDialogs[0][0])

        # print(self.nameDialogs[0])
        l106.opencsv('C:/Users/systemsupport/Desktop/report106_1000005103_20211005_081403.csv')
        # print(str(self.nameDialogs[0][0]))
        # print(self.nameDialogs[0])





    def showDialog(self): # Открыть окно выбора файла
        pathhome = Path.home()
        self.nameDialog = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # print(self.nameDialog)
        # l106.opencsv()
        # self.on_finished()
        # proba.opencsv()

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