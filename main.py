import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
# from PyQt5 import QtCore, QtGui
import design  # Это наш конвертированный файл дизайна
from completed import Ui_finished as finished
from pathlib import Path
from OKVEDmanual import OKVEDmanual
from OKVEDsait import OKVEDload
from load106 import load106
from VScomp import VScomp
from settings.conn import Orm
import time
import subprocess

vs = VScomp()

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, **kwargs):
        super(ExampleApp, self).__init__(**kwargs)
        VScomp.__init__(self)

        self.timeall = [0, 0] # Для подсчета затраченнного времени запросов       
        
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.OKVED.clicked.connect(self.on_radio_button_clicked)
        self.load106.clicked.connect(self.showDialog)
        self.checkManual.toggled.connect(self.on_radio_zagruzka)
        self.chekUpdate.toggled.connect(self.on_radio_Data)
        self.pushButton_All_bez_back.clicked.connect(self.zapros)
        self.pushButton_Sroki_svod.clicked.connect(self.zapros)
        self.pushButton_Daschbord_Sroki_svod.clicked.connect(self.openexel)
        self.OKVED_2.clicked.connect(self.OKVEDsaiti)
        # getattr(self, x).clicked.connect(lambda:self.openexcel(self.sender().objectName()))

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
           
    def openexel(self):

        myfiles = {0 : ('pushButton_Daschbord_Sroki_svod', r'Y:\WorkDocs\Отдел обработки обращений граждан\СООН_СХЕМЫ\Гришина\SROKI_SVOD_STAT.xlsx')}

        track = (r'C:\Windows\Installer\$PatchCache$\Managed\00005109110000000000000000F01FEC\15.0.4569\EXCEL.EXE',
                r'C:\Program Files\Microsoft Office 15\root\office15\EXCEL.EXE',
                r'C:\Program Files\Microsoft Office\Office15\EXCEL.EXE')

        for z in range(len(myfiles)):
            if self.sender().objectName() == myfiles[z][0]:
                for x in track:
                    try:
                        subprocess.Popen([x, myfiles[z][1]])
                    except:
                        continue
        
    
    # r''
    def OKVEDsaiti(self):
        okvedm = OKVEDload()
        okvedm.loadInSite() 
    #     self.on_finished()

    def OKVEDhand(self): # Событие загрузки файлов ОКВЭД с автоматическим вводом строк
        self.showDialog()
        for x in range(len(self.nameDialogs[0])):
            okvedm = OKVEDmanual(self.myBDokved)
            okvedm.loadSite(str(self.nameDialogs[0][x]))
        self.on_finished()

    def zapros(self):
        zaprosi = {0 : ('pushButton_All_bez_back', 'z_All_bez_back', self.timeall[0]),
                   1 : ('pushButton_Sroki_svod', 'z_sroki_svod_106', self.timeall[1])}
        orm = Orm(self.myBD)
        startTime = time.time() # время начала замера
        for x in range(len(zaprosi)):
            if self.sender().objectName() == zaprosi[x][0]:
                print("Предыдущее время, затраченное на исполнение запроса = {}".format(zaprosi[x][2]))
                orm.commit(orm.proceduri(zaprosi[x][1]))
                endTime = time.time() #время конца замера
                totalTime = endTime - startTime #вычисляем затраченное время
                time_format = time.strftime("%H:%M:%S", time.gmtime(totalTime))
                self.timeall[x] = time_format
        print("Время, затраченное на выполнение запроса = ", time_format)
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