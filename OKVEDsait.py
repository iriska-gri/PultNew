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
        ddate = date.today() - pd.to_timedelta('30 day')

        dfmindata = orm.mySQL(orm.SelectWhere('min(datelikedale)', self.tablemsp, 'datelikedale', '>', ddate), self.myBD)
        
        se = dfmindata.values.tolist()
        sdate = se[0][0]
        edate = date.today() - pd.to_timedelta('1 day') # Вычитаем из сегодняшнего дня 1 день
        delta = edate - sdate

        datelist = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            datelist.append(day)
        
        df = orm.mySQL(orm.Selected('datelikedale', self.tablemsp), self.myBD)
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

# -- --------------------------------------------------------------------------------------------------- Скачивание файла с сайта с декодированием
    def loadInSite(self):
        now = datetime.datetime.now()
        a = str(now)
        b = a.split(' ')[1]
        
 
        if self.inTime() == []: # Если все даты в базе
            print('Все даты в базе')
        else:
            for i in self.inTime():
                self.itogdate = i
                # try:
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/'+key+'?dateTime=' + result_date_convert + str(int(random.random()*1000)) + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + 'T07:56:55.723Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + 'T' + str(int(random.random()*1000)) + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
                # f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + self.kod + 'Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')

                encoded = json.loads(f.text)
                data = base64.b64decode(encoded['content'])
                self.toread = BytesIO()
                self.toread.write(data)  # pass your 'decrypted' string as the argument here
                self.toread.seek(0)  # reset the pointer
                timer_work = time.monotonic()
                # -------------------------------------------------------------------------------------- Проверка на 0 значения
                stolb = pd.read_excel(self.toread, sheet_name='Выручка', usecols = 'A')
                nb_row = len(stolb.index)-7 # Сичтает количество строк в файле
                kontroldf = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=nb_row, usecols = 'B:FQ')
                kontroldf = kontroldf.fillna(0)
                kontroldf = kontroldf.replace('-', 0)
                if kontroldf.sum(axis = 0, skipna = True).sum() == 0:
                    a = "ОКВЕД с датой {} имеет нулевые значения".format(i)
                    print(a)
                else:
                    try:
                        self.obrabotkaFile('B:CI', self.tablenp, nb_row)
                        self.obrabotkaFile('CJ:FQ', self.tablemsp, nb_row)
                    except Exception:
                        print("Провал загрузки в базу: {}".format(i))
                        continue
                # except Exception:
                    
                #     print("Провал скачивания даты с кластера: {}".format(i))
                #     continue

# ---------------------------------------------------------------------------------------------------------------------------- Формирование данных для заливки           
    def obrabotkaFile(self, diapason, inTable, row):
        idOkved = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = 'A')
        np = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=5, nrows=row, usecols = diapason)
        df = idOkved.join(np)
        df = df.fillna(0)
        df = df.replace('-', 0)
        df.columns = ['OKVED', 'Respublika_Adygeya', 'Respublika_Bashkortostan', 'Respublika_Buryatiya', 'Respublika_Altaj', 'Respublika_Dagestan', 'Respublika_Ingushetiya', 'Kabardino_Balkarskaya_Respublika', 'Respublika_Kalmykiya', 'Karachaevo_CHerkesskaya_Respublika', 'Respublika_Kareliya', 'Respublika_Komi', 'Respublika_Marij_El', 'Respublika_Mordoviya', 'Respublika_Saha', 'Respublika_Severnaya_Osetiya_Alaniya', 'Respublika_Tatarstan', 'Respublika_Tyva', 'Udmurtskaya_Respublika', 'Respublika_Hakasiya', 'CHechenskaya_Respublika', 'CHuvashskaya_Respublika_CHuvashiya', 'Altajskij_kraj', 'Krasnodarskij_kraj', 'Krasnoyarskij_kraj', 'Primorskij_kraj', 'Stavropolskij_kraj', 'Habarovskij_kraj', 'Amurskaya_oblast', 'Arhangelskaya_oblast', 'Astrahanskaya_oblast', 'Belgorodskaya_oblast', 'Bryanskaya_oblast', 'Vladimirskaya_oblast', 'Volgogradskaya_oblast', 'Vologodskaya_oblast', 'Voronezhskaya_oblast', 'Ivanovskaya_oblast', 'Irkutskaya_oblast', 'Kaliningradskaya_oblast', 'Kaluzhskaya_oblast', 'Kamchatskij_kraj', 'Kemerovskaya_oblast', 'Kirovskaya_oblast', 'Kostromskaya_oblast', 'Kurganskaya_oblast', 'Kurskaya_oblast', 'Leningradskaya_oblast', 'Lipeckaya_oblast', 'Magadanskaya_oblast', 'Moskovskaya_oblast', 'Murmanskaya_oblast', 'Nizhegorodskaya_oblast', 'Novgorodskaya_oblast', 'Novosibirskaya_oblast', 'Omskaya_oblast', 'Orenburgskaya_oblast', 'Orlovskaya_oblast', 'Penzenskaya_oblast', 'Permskij_kraj', 'Pskovskaya_oblast', 'Rostovskaya_oblast', 'Ryazanskaya_oblast', 'Samarskaya_oblast', 'Saratovskaya_oblast', 'Sahalinskaya_oblast', 'Sverdlovskaya_oblast', 'Smolenskaya_oblast', 'Tambovskaya_oblast', 'Tverskaya_oblast', 'Tomskaya_oblast', 'Tulskaya_oblast', 'Tyumenskaya_oblast', 'Ulyanovskaya_oblast', 'CHelyabinskaya_oblast', 'Zabajkalskij_kraj', 'YAroslavskaya_oblast', 'Moskva', 'Sankt_Peterburg', 'Evrejskaya_avtonomnaya_oblast', 'Neneckij_avtonomnyj_okrug', 'Hanty_Mansijskij_avtonomnyj_okrug_YUgra', 'CHukotskij_avtonomnyj_okrug', 'YAmalo_Neneckij_avtonomnyj_okrug', 'Respublika_Krym', 'Sevastopol', 'Inye_territorii']
        df.insert(loc=0, column='datelikedale', value = self.itogdate)
        df.to_sql(inTable, con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
        print("Загрузка прошла успешно: таблица: {} дата: {}".format(inTable, self.itogdate))
        

if __name__ == '__main__':
    OKVEDload().loadInSite() 
