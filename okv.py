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
from OKVED import OKVEDload
import datetime
from datetime import datetime


class OKVEDmanual(OKVEDload):

    def __init__(self, **kwargs):
        super(OKVEDmanual, self).__init__(**kwargs)
        OKVEDload.__init__(self, **kwargs)

    def loadSite(self, name, nom):
        self.toread = name
        ss = pd.read_excel(self.toread, sheet_name='Выручка', skiprows=1, nrows=0, usecols = 'B')
        dataexcel =  pd.to_datetime(ss.columns[0]).date()
        datastr = str(dataexcel)
        datasplit = datastr.split('-')
        databse = datasplit[0] + '-' + datasplit[2] + '-' + datasplit[1]
        self.itogdate = databse
        self.obrabotkaFile('B:CI', self.tablenp, nom)
        self.obrabotkaFile('CJ:FQ', self.tablemsp, nom)

if __name__ == '__main__':
    OKVEDmanual().loadSite() 
