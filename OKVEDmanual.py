import numpy as np
import pandas as pd
from settings.conn import Orm
from datetime import datetime
from pathlib import Path
from VScomp import VScomp

vs = VScomp()

class OKVEDmanual():

    def __init__(self, bd):
        VScomp.__init__(self)
        self.orm = Orm(bd)

    def loadSite(self, name):
        self.toread = name
        ss = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=1, nrows=0, usecols = 'B')
        dataexcel =  pd.to_datetime(ss.columns[0], dayfirst=True).date() # Получаем дату из файла
        self.itogdate = dataexcel
        stolb = pd.read_excel(name, sheet_name='Выручка', usecols = 'A')
        nb_row = len(stolb.index)-7 # Счетает количество строк в файле
        print("Количество строк в файле {} - {}".format(name, nb_row))
        self.obrabotkaFile('B:CI', self.tablenp, nb_row)
        self.obrabotkaFile('CJ:FQ', self.tablemsp, nb_row)
        self.orm.connclose()
    
    def obrabotkaFile(self, diapason, inTable, row):
        idOkved = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = 'A')
        np = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = diapason)
        df = idOkved.join(np)
        df = df.fillna(0)
        df = df.replace('-', 0)
        df.insert(loc=0, column='datelikedale', value = self.itogdate)
        df.to_csv('okved', sep=';', na_rep=r'\N', quoting = 1, mode='a', header=False, index=False)
        self.orm.commit(self.orm.load_local('okved', inTable))
        Path('okved').unlink()
        print("Загрузка прошла успешно: таблица: {} дата: {}".format(inTable, self.itogdate))
