import numpy as np
import pandas as pd
# from datetime import datetime, time, timedelta, date
# from sqlalchemy import create_engine
# from settings.conn import Orm
# from settings.readFiles import read_files
# import json
# from io import BytesIO
# import requests
# import base64
# from datetime import datetime, timedelta
# import time
from OKVEDsait import OKVEDload
# import datetime
from datetime import datetime


class OKVEDmanual(OKVEDload):

    def __init__(self, **kwargs):
        super(OKVEDmanual, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)

    def loadSite(self, name):
        self.toread = name
        ss = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=1, nrows=0, usecols = 'B')
        dataexcel =  pd.to_datetime(ss.columns[0], dayfirst=True).date() # Получаем дату из файла
        self.itogdate = dataexcel
        stolb = pd.read_excel(name, sheet_name='Выручка', usecols = 'A')
        nb_row = len(stolb.index)-7 # Сичтает количество строк в файле
        print("Количество строк в файле {} - {}".format(name, nb_row))
        self.obrabotkaFile('B:CI', self.tablenp, nb_row)
        self.obrabotkaFile('CJ:FQ', self.tablemsp, nb_row)
