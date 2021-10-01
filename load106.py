import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta, date
from sqlalchemy import create_engine
from settings.conn import Orm
from settings.readFiles import read_files
import json
from io import BytesIO

import requests
import base64
from datetime import datetime, timedelta
import time

orm = Orm()
class load106(Orm):
    def __init__(self, **kwargs):
        super(load106, self).__init__(**kwargs)
        self.myBD = "sroki_svod"
        
        
    def opencsv(self):
        name='C:/Users/systemsupport/Desktop/1.csv'
        self.csv_df = pd.read_csv(name, sep=';', header=None, engine='python', encoding = None)
        # ------------------------------------------------------------------------------------------- Основные данные по файлу (settings))
        myrows = {1 : ('actions', 'id_actions, actions', 'sprav_actions'),
                  3 : ('task_step_name', 'task_step_id, task_step_name', 'sprav_task_step_name'),
                  4 : ('card_id', ''),
                  5 : ('card_task_id', ''),
                  6 : ('tax_code', ''),
                  8 : ('login', 'id_login, login', 'sprav_login'),
                  9 : ('start_ts_reg', ''),
                  10 : ('end_ts_reg', ''),
                  15 : ('org_title', 'id_org_title, org_title', 'sprav_org_title')
                  }
        datarows = [9, 10] # Все столбцы с датами
        # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part 1
        self.csv_df[5] = self.csv_df[5].fillna(0)
        self.csv_df[10] = self.csv_df[10].fillna("1900-01-01 00:00:00")

        self.probeliZamena(3)
        for x in datarows:
            self.formatdataZamena(x)
        # -------------------------------------------------------------------------------------------
        # myrows = [0, 1, 3, 4, 5, 6, 8, 9, 11, 15, 16, 18, 21, 22, 23, 24, 26, 27]
        dfrows = self.csv_df[[0]]
        
        dfrows.columns = ['history_id']
        myloc = 1

        zamena = []
        for x in myrows:
            if len(myrows[x]) > 2:
                zamena.append(x)
            self.obrabrows = self.csv_df[[x]]
            self.obrabrows.columns = [myrows[x][0]]

            for z in zamena:
                if x == z:
                    self.obrabrows = self.spravkaZamena(myrows[z][1], myrows[z][2], myrows[z][0])
            dfrows.insert(loc=myloc, column=myrows[x][0], value = self.obrabrows)
            myloc += 1
        dfrows = dfrows.drop_duplicates()

        # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part 2
        # где столбец Y больше 13, в столбце Z присвоить 777
        act = [16, 34, 63]
        for x in act:
            dfrows.loc[dfrows['actions'] == x, 'task_step_name'] = 1
        dfrows.loc[dfrows['actions'] == 34, 'history_id'] *= -1
        dfrows['org_title'] = dfrows['org_title'].fillna(1)
        # -------------------------------------------------------------------------------------------
        dfrows.to_sql('a_106', con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
        print(dfrows)

    def formatdataZamena(self, numb):
        self.csv_df[numb] = self.csv_df[numb].apply(lambda x: x.split('+')[0]) # Производит замену после определнного символа
        self.csv_df[numb] = pd.to_datetime(self.csv_df[numb])

    def probeliZamena(self, numb):
        self.csv_df[numb] = self.csv_df[numb].str.strip() # Удаляем все пробелы в столбце

    def spravkaZamena(self, spravRows, spravTable, nameRows):    
        dfspravka = orm.mySQL(orm.Selected(spravRows, spravTable), self.myBD)
        merge = self.obrabrows.merge(dfspravka, left_on=nameRows, right_on=nameRows, how='left')
        del merge[nameRows]
        return merge

if __name__ == '__main__':
    load106().opencsv() 
  
        #, , , , out_date, in_date, registration_number, life_situation_name, snts_code, dubl, appeal_source, date_reg_appeal"
