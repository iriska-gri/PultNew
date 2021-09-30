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
        csv_df = pd.read_csv(name, sep=';', header=None, engine='python', encoding = None)

        csv_df1 = csv_df[3]
        new = csv_df1.str.strip()
        csv_df = csv_df.drop([3], axis=1)
        csv_df.insert(loc=3, column=3, value = new)
        print(list(csv_df))
        # print(new.loc[new == 'Проверка наличия объекта в АИС'])
        # print(csv_df)
        # print(csv_df['ll'].loc[csv_df['ll'] == 'Проверка наличия объекта в АИС'])





        # print(new.loc[new == 'Проверка наличия объекта в АИС'])
        # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part1
        # csv_df1 = csv_df.stack().str.strip().unstack() # Удаляет из выгрузки все лишние пробелы спереди и сзади
        # print(csv_df[3].loc[csv_df[3] == 'Проверка наличия объекта в АИС '])
        # csv_df.loc[csv_df[1] == "SENT", 0] *= -1 # Замена history_id на отрицательное, где SENT
        # -------------------------------------------------------------------------------------------
        # myrows = [0, 1, 3, 4, 5, 6, 8, 9, 11, 15, 16, 18, 21, 22, 23, 24, 26, 27]
        dfrows = csv_df[[0]]
        
        dfrows.columns = ['history_id']
        # print(dfrows)
        myrows = {1 : 'actions', 3 : 'task_step_name'}
        myloc = 1

        for x in myrows:
            self.obrabrows = csv_df[[x]]
            # self.obrabrows = self.obrabrows.stack().str.strip().unstack()
            self.obrabrows.columns = [myrows[x]]
            if x == 1:
                self.obrabrows = self.spravkaZamena('id_actions, actions', 'sprav_actions', myrows[x])
            if x == 3:
                self.obrabrows = self.spravkaZamena('task_step_id, task_step_name', 'sprav_task_step_name', myrows[x])
            dfrows.insert(loc=myloc, column=myrows[x], value = self.obrabrows)
            myloc += 1
        dfrows = dfrows.drop_duplicates()

        # ------------------------------------------------------------------------------------------- Подготовка экселевского файла part2
        # где столбец Y больше 13, в столбце Z присвоить 777
        dfrows.loc[dfrows['actions'] == 34, 'task_step_name'] = 1
        dfrows.loc[dfrows['actions'] == 63, 'task_step_name'] = 1
        dfrows.loc[dfrows['actions'] == 16, 'task_step_name'] = 1
        dfrows.loc[dfrows['actions'] == 34, 'history_id'] *= -1
        # dfrows = dfrows.loc[dfrows['actions'] == 16]
        # -------------------------------------------------------------------------------------------
        dfrows.to_sql('a_106', con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
        print(dfrows)

    # def probeliZamena(self):
    #     csv_df1 = csv_df[3]
    #     new = csv_df1.str.strip()
    #     csv_df.insert(loc=3, column='3', value = new)


    def spravkaZamena(self, spravRows, spravTable, nameRows):    
        dfspravka = orm.mySQL(orm.Selected(spravRows, spravTable), self.myBD)
        merge = self.obrabrows.merge(dfspravka, left_on=nameRows, right_on=nameRows, how='left')
        # merge.loc[(merge.actions == merge.actions), 'actions'] = merge.id_actions # Пока оставить, не знаю как используется

        del merge[nameRows]
        return merge

if __name__ == '__main__':
    load106().opencsv() 

        # a.to_sql('a_106', con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
        # print(dfspravka)
        # print(a)        
        # "status_task, history_id, actions, task_step_name, card_id, card_task_id, tax_code, login, start_ts_reg, end_ts_reg, org_title, out_date, in_date, registration_number, life_situation_name, snts_code, dubl, appeal_source, date_reg_appeal"

        # print(excel_data_df.columns.values)
        # print(new_df)
        # text = 'C:/Users/systemsupport/Desktop/1.csv'
        # with open(text) as f:
        #     print(f)


        # text = 'C:/Users/systemsupport/Desktop/1.csv'
        # f = open(text, 'rb')
        # data = f.read()

        # for x in ['cp1251','utf-8']:
        #     a= data.decode(x)

        # print(a)
