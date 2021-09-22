import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta, date
from sqlalchemy import create_engine
from settings.conn import Orm
from sait_okved import loadOkVED
from settings.readFiles import read_files
import json
from io import BytesIO
import requests
import base64
from datetime import datetime, timedelta
import time


orm = Orm()
load = loadOkVED()

class OKVEDload():

    def __init__(self):
        pass

    def proba(self):
        df = pd.read_sql("SELECT DISTINCT viruzka_msp.datelikedale FROM viruzka_msp", con = orm.connect("localhost", "root", "", "okved"))
        print(df)

#     def inTime(self):
#         # -- --------------------------------------------------------------------------------------------------- Диапазон дат
#         s = '2021-09-16' 
#         sdate = datetime.strptime(s, "%Y-%m-%d")
#         e = '2021-09-18'
#         edate = datetime.strptime(e, "%Y-%m-%d")
#         delta = edate - sdate
#         datelist = []
#         for i in range(delta.days + 1):
#             day = sdate + timedelta(days=i)
#             datelist.append(day.strftime("%Y-%m-%d"))
#         return datelist

# # -- --------------------------------------------------------------------------------------------------- Скачивание файла с сайта с декодированием
#     def loadInSite(self, diapason, inTable):
#     # def loadInSite(self):
#         # for key, values in datar.items():
#         # 
#         for i in self.inTime():
#             try:
#                 f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + i + 'T07:56:55.723Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
#                 encoded = json.loads(f.text)
#                 data = base64.b64decode(encoded['content'])
#                 toread = BytesIO()
#                 toread.write(data)  # pass your 'decrypted' string as the argument here
#                 toread.seek(0)  # reset the pointer
#                 timer_work = time.monotonic()
# # ---------------------------------------------------------------------------------------------------------------------------- Проверка на 0 значения
#                 kontroldf = pd.read_excel(toread, sheet_name='Выручка', skiprows=5, nrows=2714, usecols = 'B:FQ')
#                 kontroldf = kontroldf.fillna(0)
#                 kontroldf = kontroldf.replace('-', 0)
#                 if kontroldf.sum(axis = 0, skipna = True).sum() == 0:
#                     print("ОКВЕД с датой {} имеет нулевые значения".format(i))
#                 else:
# # ---------------------------------------------------------------------------------------------------------------------------- Формирование данных для заливки           
#                     idOkved = pd.read_excel(toread, sheet_name='Выручка', skiprows=5, nrows=2714, usecols = 'A')
#                     np = pd.read_excel(toread, sheet_name='Выручка', skiprows=5, nrows=2714, usecols = diapason)
#                     df = idOkved.join(np)
#                     df = df.fillna(0)
#                     df = df.replace('-', 0)
#                     df.columns = ['OKVED', 'Respublika_Adygeya', 'Respublika_Bashkortostan', 'Respublika_Buryatiya', 'Respublika_Altaj', 'Respublika_Dagestan', 'Respublika_Ingushetiya', 'Kabardino_Balkarskaya_Respublika', 'Respublika_Kalmykiya', 'Karachaevo_CHerkesskaya_Respublika', 'Respublika_Kareliya', 'Respublika_Komi', 'Respublika_Marij_El', 'Respublika_Mordoviya', 'Respublika_Saha', 'Respublika_Severnaya_Osetiya_Alaniya', 'Respublika_Tatarstan', 'Respublika_Tyva', 'Udmurtskaya_Respublika', 'Respublika_Hakasiya', 'CHechenskaya_Respublika', 'CHuvashskaya_Respublika_CHuvashiya', 'Altajskij_kraj', 'Krasnodarskij_kraj', 'Krasnoyarskij_kraj', 'Primorskij_kraj', 'Stavropolskij_kraj', 'Habarovskij_kraj', 'Amurskaya_oblast', 'Arhangelskaya_oblast', 'Astrahanskaya_oblast', 'Belgorodskaya_oblast', 'Bryanskaya_oblast', 'Vladimirskaya_oblast', 'Volgogradskaya_oblast', 'Vologodskaya_oblast', 'Voronezhskaya_oblast', 'Ivanovskaya_oblast', 'Irkutskaya_oblast', 'Kaliningradskaya_oblast', 'Kaluzhskaya_oblast', 'Kamchatskij_kraj', 'Kemerovskaya_oblast', 'Kirovskaya_oblast', 'Kostromskaya_oblast', 'Kurganskaya_oblast', 'Kurskaya_oblast', 'Leningradskaya_oblast', 'Lipeckaya_oblast', 'Magadanskaya_oblast', 'Moskovskaya_oblast', 'Murmanskaya_oblast', 'Nizhegorodskaya_oblast', 'Novgorodskaya_oblast', 'Novosibirskaya_oblast', 'Omskaya_oblast', 'Orenburgskaya_oblast', 'Orlovskaya_oblast', 'Penzenskaya_oblast', 'Permskij_kraj', 'Pskovskaya_oblast', 'Rostovskaya_oblast', 'Ryazanskaya_oblast', 'Samarskaya_oblast', 'Saratovskaya_oblast', 'Sahalinskaya_oblast', 'Sverdlovskaya_oblast', 'Smolenskaya_oblast', 'Tambovskaya_oblast', 'Tverskaya_oblast', 'Tomskaya_oblast', 'Tulskaya_oblast', 'Tyumenskaya_oblast', 'Ulyanovskaya_oblast', 'CHelyabinskaya_oblast', 'Zabajkalskij_kraj', 'YAroslavskaya_oblast', 'Moskva', 'Sankt_Peterburg', 'Evrejskaya_avtonomnaya_oblast', 'Neneckij_avtonomnyj_okrug', 'Hanty_Mansijskij_avtonomnyj_okrug_YUgra', 'CHukotskij_avtonomnyj_okrug', 'YAmalo_Neneckij_avtonomnyj_okrug', 'Respublika_Krym', 'Sevastopol', 'Inye_territorii']
#                     df.insert(loc=0, column='datelikedale', value= i)
#                     df.to_sql(inTable, con=orm.connect("localhost", "root", "", "okved"), if_exists="append", index = False)
#                     print("Загрузка прошла успешно: таблица: {} дата: {}".format(inTable, i))

#             except Exception:
#                 print("Провал загрузки: {}".format(i))
#                 continue
            
#     def uploadinfo(self):
#         self.loadInSite('B:CI', 'viruzka_np')
#         self.loadInSite('CJ:FQ', 'viruzka_msp')

if __name__ == '__main__':
    OKVEDload().proba() 
