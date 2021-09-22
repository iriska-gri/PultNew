
import json
import pandas as pd
from io import BytesIO
import requests
import base64
from datetime import datetime, timedelta
import time

class loadOkVED():
    def inTime(self):
        # -- --------------------------------------------------------------------------------------------------- Диапазон дат
        s = '2021-09-17' 
        sdate = datetime.strptime(s, "%Y-%m-%d")
        e = '2021-09-18'
        edate = datetime.strptime(e, "%Y-%m-%d")
        delta = edate - sdate
        datelist = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            datelist.append(day.strftime("%Y-%m-%d"))
        return datelist

# -- --------------------------------------------------------------------------------------------------- Скачивание файла с сайта
    def loadInSite(self):
        for i in self.inTime():
            result_date_convert = i
            f = requests.get('https://cluster-analysis.nalog.ru/webproxy/api/OkvedReport/new/okved/download/base64?dateTime=' + result_date_convert + 'T07:56:55.723Z&apikey=d808c003f1d69c5fa97713b2a5e1b591')
            encoded = json.loads(f.text)
            data = base64.b64decode(encoded['content'])
            toread = BytesIO()
            toread.write(data)  # pass your 'decrypted' string as the argument here
            toread.seek(0)  # reset the pointer
            timer_work = time.monotonic()
            return toread
            # df = pd.read_excel(toread,sheet_name='Выручка',header=None) #номер листа с 0
            # dataOkved = pd.read_excel(toread, sheet_name='Выручка', skiprows=1, nrows=0, usecols = 'B')
            # print(dataOkved)
# -- --------------------------------------------------------------------------------------------------- 