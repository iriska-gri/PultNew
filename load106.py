import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta, date
from sqlalchemy import create_engine
from settings.conn import Orm
from settings.readFiles import read_files
import json
import io
from io import BytesIO

import requests
import base64
from datetime import datetime, timedelta
import time

orm = Orm()

pd.options.display.float_format ='{:,.0f}'.format

class load106(Orm):
    def __init__(self, **kwargs):
        super(load106, self).__init__(**kwargs)
        if self.usering == 'systemsupport':
            self.myBD = "sroki_svod"
            self.inTable = 'a_all_data_106'
            self.spravSNTS = 'sprav_snts_svod'
        else:
            self.myBD = "Sroki_svod"
            self.inTable = 'a_all_data_106_copy'
            self.spravSNTS = 'sprav_SNTS_svod'
            
        # self.way = way
        
    def encode_Control(self,filename):
        try:
            f = open(filename, 'rb')
            data = f.read()

            for x in ['cp1251','utf-8']:
                try:
                    data.decode(x)
                    return x

                except:
                    print('Ошибка')
                    continue
            f.close()
            return ''
        except Exception:
            return 'cp1251'

    # def opencsv(self, name):
    def opencsv(self):
        name='C:/Users/systemsupport/Desktop/report106_1000005103_20211005_081401.csv'

        whatcode = self.encode_Control(name)
        myrows = {1 : ('actions', 'id_actions', 'id_actions, actions', 'sprav_actions'),
                  3 : ('task_step_name', 'task_step_id', 'task_step_id, task_step_name', 'sprav_task_step_name'),
                  8 : ('login', 'id_login', 'id_login, login', 'sprav_login'),
                  15 : ('org_title', 'id_org_title', 'id_org_title, org_title', 'sprav_org_title'), 
                  22 : ('life_situation_name', 'id_life_situation_name', 'id_life_situation_name, life_situation_name', 'sprav_life_situation_name'),
                  26 : ('appeal_source', 'id_appeal_source', 'id_appeal_source, appeal_source', 'sprav_appeal')}
        datarows = [9, 27] # Все столбцы с датами
        for chunk in pd.read_csv(name, sep=';', header=None, na_values='NULL', keep_default_na=False, dtype=str, chunksize=10000, engine='python', encoding = whatcode):
            self.chunk = chunk.drop(columns=[2,7,11, 12,13,14,17,19,20,25])
            # chunk = chunk.fillna(r'\N')
                #     self.csv_df[5] = self.csv_df[5].fillna(0)
    #     self.csv_df[10] = self.csv_df[10].fillna("1900-01-01 00:00:00")
    #     self.csv_df[23] = self.csv_df[23].fillna('35100')
    #     self.csv_df[24] = self.csv_df[24].fillna(0)
    #     self.csv_df[23] = self.csv_df[23].replace(to_replace ='-1', value ='35100')
            for x in datarows:
                self.simvolZamena(x, '+')
                self.formatdataZamena(x)
            for x in myrows:
                self.spravkaZamena(myrows[x][2], myrows[x][3], myrows[x][1], x, myrows[x][0])
            # for x in datarows:
            #     self.formatdataZamena(x)
            # self.chunk[9] = pd.to_datetime(self.chunk[9])
        # self.chunk.to_excel("output.xlsx")
            print(self.chunk)
                
    def spravkaZamena(self, spravRows, spravTable, spravId, chunrows, sprav):
        dfspravka = orm.mySQL(orm.Selected(spravRows, spravTable), self.myBD)
        self.chunk = self.chunk.merge(dfspravka, left_on=chunrows, right_on=sprav, how='left')
        self.chunk[chunrows] = self.chunk[spravId]
        del self.chunk[spravId]
        del self.chunk[sprav]

    def simvolZamena(self, numb, sim):    
        if (np.core.defchararray.find(self.chunk[numb].values.astype(str), sim) > -1).any() == True: # Просмотр наличия символа в строке
            self.chunk[numb] = self.chunk[numb].apply(lambda x: x.split(sim)[0]) # Производит замену после определнного символа

    def formatdataZamena(self, numb):

        if numb == 27:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb]).dt.date
        else:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb])
    
        # merge.to_excel("output.xlsx")
        
        # ------------------------------------------------------------------------------------------- Основные данные по файлу (settings))
            # myrows = {1 : ('actions', 'id_actions, actions', 'sprav_actions'),
            #         3 : ('task_step_name', 'task_step_id, task_step_name', 'sprav_task_step_name')}
                    # 4 : ('card_id', '')}
    #               5 : ('card_task_id', ''),
    #               6 : ('tax_code', ''),
    #               8 : ('login', 'id_login, login', 'sprav_login'),
    #               9 : ('start_ts_reg', ''),
    #               10 : ('end_ts_reg', ''),
    #               15 : ('org_title', 'id_org_title, org_title', 'sprav_org_title'), 
    #               16 : ('out_date', ''),
    #               18 : ('in_date', '')}
    #             #   21 : ('registration_number', ''),
    #               22 : ('life_situation_name', 'id_life_situation_name, life_situation_name', 'sprav_life_situation_name'),
    #               23 : ('snts_code', ''),
    #               24 : ('dubl', ''),
    #               26 : ('appeal_source', 'id_appeal_source, appeal_source', 'sprav_appeal'),
    #               27 : ('date_reg_appeal', '')
    #               }
            # print(self.csv_df)
            # datarows = [9, 10, 16, 18, 27] # Все столбцы с датами
    #     simvol = [21] # Удаление данных после символа
    #     # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part 1
    #     self.csv_df[5] = self.csv_df[5].fillna(0)
    #     self.csv_df[10] = self.csv_df[10].fillna("1900-01-01 00:00:00")
    #     self.csv_df[23] = self.csv_df[23].fillna('35100')
    #     self.csv_df[24] = self.csv_df[24].fillna(0)
    #     self.csv_df[23] = self.csv_df[23].replace(to_replace ='-1', value ='35100')
    #     # self.csv_df[21] = self.csv_df[21].fillna(0)
    #     self.csv_df[21] = self.csv_df[21].astype(str)
    #     if (np.core.defchararray.find(self.csv_df[21].values.astype(str),'.') > -1).any() == True: # Просмотр наличия символа в строке
    #         self.csv_df[21] = self.csv_df[21].apply(lambda x: x.split('.')[0])
    #     # -------------------------------- Поиск и замена текста на код (единичный случай)
    #     stringZamena = self.csv_df[23][~self.csv_df[23].str.contains('0|1|2|3|4|5|6|7|8|9')].unique()  # Поиск всех нечисловых значений
    #     naZamenu = []
    #     for b in stringZamena:
    #         try:
    #             a = orm.mySQL(orm.SelectWhere('cod_SNTS', self.spravSNTS, 'vid_object', '=', b), self.myBD)
    #             naZamenu.append(a['cod_SNTS'][0])
    #         except Exception:
    #             continue
    #     # print(stringZamena)
    #     # print(naZamenu)
    #     for x in range(len(stringZamena)):
    #         self.csv_df[23] = self.csv_df[23].replace(to_replace = stringZamena[x], value = naZamenu[x])
    #     # -------------------------------- 
    #     self.probeliZamena(3)

    #     for x in datarows:
    #         self.simvolZamena(x, '+')
    #         self.formatdataZamena(x)

    #     for x in simvol:
    #         self.simvolZamena(x, '.')
    #     # -------------------------------------------------------------------------------------------
            # dfrows = self.csv_df[[0]]
            # dfrows.columns = ['history_id']
        
            # myloc = 1
        
            # zamena = []
            # for x in myrows:
            #     if len(myrows[x]) > 2:
            #         zamena.append(x)
            #     self.obrabrows = self.csv_df[[x]]
            #     self.obrabrows.columns = [myrows[x][0]]
            #     print(self.obrabrows.columns)
            #     # for z in zamena:
            #     #     if x == z:
            #     #         self.obrabrows = self.spravkaZamena(myrows[z][1], myrows[z][2], myrows[z][0])
            #             # a = int(self.obrabrows)
            #     dfrows.insert(loc=myloc, column=myrows[x][0], value = self.obrabrows)
                
            #     myloc += 1
            # dfrows = dfrows.drop_duplicates()
            # print(dfrows)

    #     # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part 2
    #     act = [16, 34, 63]
        
    #     for x in act:
    #         dfrows.loc[dfrows['actions'] == x, 'task_step_name'] = 1
    #     dfrows.loc[dfrows['actions'] == 34, 'history_id'] *= -1
    #     dfrows['org_title'] = dfrows['org_title'].fillna(1)
        
    #     # -------------------------------------------------------------------------------------------
    #     dfrows.insert(loc=0, column='status_task', value = 3)
       
    #     # dfrows.to_sql(self.inTable, con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
    #     # dfrows.to_sql(self.inTable, con=self.connect(), if_exists="append", index = False)

    # def simvolZamena(self, numb, sim):    
    #     if (np.core.defchararray.find(self.csv_df[numb].values.astype(str), sim) > -1).any() == True: # Просмотр наличия символа в строке
    #         self.csv_df[numb] = self.csv_df[numb].apply(lambda x: x.split(sim)[0]) # Производит замену после определнного символа

    # def formatdataZamena(self, numb):

    #     if numb == 27:
    #         self.csv_df[numb] = pd.to_datetime(self.csv_df[numb]).dt.date
    #     else:
    #         self.csv_df[numb] = pd.to_datetime(self.csv_df[numb])

    # def probeliZamena(self, numb):
    #     self.csv_df[numb] = self.csv_df[numb].str.strip() # Удаляем все пробелы в столбце

    # def spravkaZamena(self, spravRows, spravTable, nameRows):    
    #     dfspravka = orm.mySQL(orm.Selected(spravRows, spravTable), self.myBD)
    #     merge = self.obrabrows.merge(dfspravka, left_on=nameRows, right_on=nameRows, how='left')
    #     del merge[nameRows]
    #     return merge

if __name__ == '__main__':
    load106().opencsv() 
  