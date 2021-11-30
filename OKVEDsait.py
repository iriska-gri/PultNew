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
import random
import datetime
from pathlib import Path

orm = Orm()

class OKVEDload(Orm):

    def __init__(self, **kwargs):
        super(OKVEDload, self).__init__(**kwargs)
        if self.usering == 'systemsupport':
            self.tablemsp = 'viruzka_msp'
            self.tablenp = 'viruzka_np'
            self.myBD = "okved"
        else:
            
            self.tablemsp = 'Viruzka_MSP'
            self.tablenp = 'Viruzka_NP'
            self.myBD = "OKVED"

    def inTime(self):
        
        ddate = date.today() - pd.to_timedelta('365 day')

        dfmindata = orm.SQLOkved(orm.SelectWhere('min(datelikedale)', self.tablemsp, 'datelikedale', '>', ddate), self.myBD)
     
        se = dfmindata.values.tolist()
        sdate = se[0][0]
        edate = date.today() - pd.to_timedelta('1 day') # Вычитаем из сегодняшнего дня 1 день
        delta = edate - sdate

        datelist = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            datelist.append(day)
        
        df = orm.SQLOkved(orm.Selected('datelikedale', self.tablemsp), self.myBD)
        dateinbase = []
        for x in range(len(df.to_numpy().tolist())):
            dateinbase.append(df.to_numpy().tolist()[x][0])
        # -------------------------------------------------------------------------------------- Проверка на даты которых нет в базе
        pusto = []
        for d in datelist:
            if d in dateinbase:
                pass
            else:
                pusto.append(d.strftime("%Y-%m-%d"))
        return pusto

# # -- --------------------------------------------------------------------------------------------------- Скачивание файла с сайта с декодированием
    def loadInSite(self):
        now = datetime.datetime.now()
        a = str(now)
        b = a.split(' ')[1]
 
        if self.inTime() == []: # Если все даты в базе
            print('Все даты в базе')
        else:
            # for i in self.inTime():
            #     self.itogdate = i
                # print(self.itogdate)
            try:
                url='https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&start=0&limit=1000'

                page=requests.get(url)
                # f = requests.get('http://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=2021-02-01T11:23:00.008Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # encoded = json.loads(f.text)
                # data = base64.b64decode(encoded['content'])
                # self.toread = BytesIO()
                # self.toread.write(data)  # pass your 'decrypted' string as the argument here
                # self.toread.seek(0)  # reset the pointer
                # timer_work = time.monotonic()
                # # # -------------------------------------------------------------------------------------- Проверка на 0 значения
                # stolb = pd.read_excel(self.toread, sheet_name='Выручка', usecols = 'A')
                # print(stolb)
            except Exception:
                print("провал загрузки {}".format('f'))
                # continue
                # f = requests.get('https://ya.ru/')
                # try:
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/'+key+'?dateTime=' + result_date_convert + str(int(random.random()*1000)) + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + 'T07:56:55.723Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + 'T' + str(int(random.random()*1000)) + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + self.kod + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + str(int(random.random()*1000)) + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=2021-02-01T11:23:00.008Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # encoded = json.loads(f.text)
                # data = base64.b64decode(encoded['content'])
                # self.toread = BytesIO()
                # self.toread.write(data)  # pass your 'decrypted' string as the argument here
                # self.toread.seek(0)  # reset the pointer
                # timer_work = time.monotonic()
                # # # -------------------------------------------------------------------------------------- Проверка на 0 значения
                # stolb = pd.read_excel(self.toread, sheet_name='Выручка', usecols = 'A')
                # print(stolb)
                # nb_row = len(stolb.index)-7 # Сичтает количество строк в файле
                # kontroldf = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=nb_row, usecols = 'B:FQ')
                # kontroldf = kontroldf.fillna(0)
                # kontroldf = kontroldf.replace('-', 0)
                # if kontroldf.sum(axis = 0, skipna = True).sum() == 0:
                #     a = "ОКВЕД с датой {} имеет нулевые значения".format(i)
                #     print(a)
                # else:
                #     try:
                #         self.obrabotkaFile('B:CI', self.tablenp, nb_row)
                #         self.obrabotkaFile('CJ:FQ', self.tablemsp, nb_row)
                #     except Exception:
                #         print("Провал загрузки в базу: {}".format(i))
                #         continue
                # # except Exception:
                    
                # #     print("Провал скачивания даты с кластера: {}".format(i))
                # #     continue

# ---------------------------------------------------------------------------------------------------------------------------- Формирование данных для заливки           
    def obrabotkaFile(self, diapason, inTable, row):
        idOkved = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = 'A')
        np = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = diapason)
        df = idOkved.join(np)
        df = df.fillna(0)
        df = df.replace('-', 0)
        df.insert(loc=0, column='datelikedale', value = self.itogdate)
        df.to_csv('okved', sep=';', na_rep=r'\N', quoting = 1, mode='a', header=False, index=False)
        orm.commitOkved(orm.load_local('okved', inTable))
        Path('okved').unlink()
        print("Загрузка прошла успешно: таблица: {} дата: {}".format(inTable, self.itogdate))
        

if __name__ == '__main__':
    OKVEDload().loadInSite() 
