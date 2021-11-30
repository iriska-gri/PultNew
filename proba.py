import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta, date
from sqlalchemy import create_engine
from settings.conn import Orm
from settings.readFiles import read_files
import json
from io import BytesIO
import getpass # Определить пользователя

orm = Orm()

class load107():
##- ----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(load107, self).__init__(**kwargs)
        self.usering3 = getpass.getuser()
        if self.usering3 == 'systemsupport':
            self.myBD = "sroki_svod"
            self.inTable = 'a'
            self.myBDo = "ikved"
        else:
            self.myBD = "Sroki_svod"
            self.inTable = 'a'
            self.myBDo = "OKVED"

            
    #     # self.way = way
        
        
    # def opencsv(self):
    #     # print(*self.set_connect)
    #     print(self.myBD)
    #     d = [1]
    #     dfrows = pd.DataFrame(d)
    #     dfrows.columns = ['C']
    #     print(dfrows)
    #     dfrows.to_sql('a', con=self.connect(*self.set_connect, self.myBD), if_exists="append", index = False)
    #     # dfrows.to_sql('a', con=self.connect(), if_exists="append", index = False)
##- ----------------------------------------------------------------------------------------------------------------------------
    # def opencsv(self):
    #     name='C:/Users/systemsupport/Desktop/Отчет ОКВЭД 20211004.xlsx'
    #     # sheet='Выручка'
    #     ss = pd.read_excel(name, sheet_name='Выручка', usecols = 'A')
    #     nb_row = len(ss.index)-6
    #     print(nb_row)
##- ----------------------------------------------------------------------------------------------------------------------------
    def opencsv(self):
        # a = orm.Sql()
        # print(a[0][0])
        spradf = orm.SQL(orm.SelectWhere('cod_SNTS', 'sprav_snts_svod', 'vid_object', '=', 'Автобусы'))
        print(spradf[0][0])

        # orm.DeleteWhere("viruzka_np.datelikedale >= '2021-10-04' AND viruzka_np.datelikedale <= '2021-10-04'")
        # orm.DeleteWhere('viruzka_np', 'viruzka_np.datelikedale', '2021-10-04', 'viruzka_np.datelikedale', '2021-10-04')
        # orm.mySQL(orm.Ses(), "okved")
        # sql = "DELETE FROM viruzka_np WHERE viruzka_np.OKVED = '01.13.11'"
        # # a = self.connection.execute(sql)
        # a = orm.conections("okved").execute(sql)
        # a = orm.mySQL(orm.DeleteWhere(), "okved")
        # print(a)


if __name__ == '__main__':
    load107().opencsv() 