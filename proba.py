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

class load107(Orm):
    def __init__(self, **kwargs):
        super(load107, self).__init__(**kwargs)
        if self.usering == 'systemsupport':
            self.myBD = "sroki_svod"
            self.inTable = 'a'
        else:
            self.myBD = "Sroki_svod"
            self.inTable = 'a'

            
        # self.way = way
        
        
    def opencsv(self):
        # print(*self.set_connect)
        print(self.myBD)
        d = [1]
        dfrows = pd.DataFrame(d)
        dfrows.columns = ['C']
        print(dfrows)
        dfrows.to_sql('a', con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
        # dfrows.to_sql('a', con=self.connect(), if_exists="append", index = False)

if __name__ == '__main__':
    load107().opencsv() 
  