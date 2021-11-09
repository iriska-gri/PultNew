import mysql.connector
from mysql.connector import Error

import getpass # Определить пользователя
import datetime
import pandas
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import getpass # Определить пользователя
from mysql.connector.locales.eng import client_error
# from urllib import quote_plus as urlquote
import urllib.parse
from urllib.parse import quote as urlquote

# session = Session()

#--------------------------------------------------------------------------------------------------------- Подключение
class Orm():
    """ Создает список определенной длины, вставляя элемент в нужное место списка.
    Возвращает созданный список """
    def __init__(self, **kwargs):
        super(Orm, self).__init__(**kwargs)

        self.usering = getpass.getuser()
        
        if self.usering == 'systemsupport':
            self.set_connect = ("localhost", "root", "P@ssw0rd")
            self.myBDokved = "okved"
            self.myBD = "sroki_svod"
        else:
            self.set_connect = ("10.252.44.38", "root", "P@ssw0rd")
            self.myBDokved = "OKVED"

        self.connectionOKVED = self.connect(*self.set_connect, self.myBDokved)
        
        self.connectionSroki = self.connect(*self.set_connect, self.myBD)

# #---------------------------------------------------------------------------------------------------------
    # def connect(self, host_names, user_name, user_password, db_name):
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:
            connection = create_engine(f"""mysql+mysqlconnector://{user_name}:%s@{host_names}/{db_name}""" % urlquote(user_password))
            session = Session(bind=connection)
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return session

    # def connclose(self):
    #     self.conections.close()
    #     print("Соединение закрыто")
    
    def DeleteWhere(self, table, t, data1, data2):
    # def DeleteWhere(self, table, t):
        # sql = f"""DELETE FROM {table} WHERE {t} >= {data1} AND {t} <= {data2}"""
        sql = f"""DELETE FROM {table} WHERE {t} >= '{data1}' AND {t} <= '{data2}'"""
        s = self.connectionOKVED.execute(sql)
        return s
        
    def mySQL(self, zapros, nameTable):
        sql = pd.read_sql(zapros, con = self.connect(*self.set_connect, nameTable))
        return sql
    
    def SelectWhere(self, rows, table, uslovie, dan, data):
        s = f"""SELECT DISTINCT {rows} FROM {table} WHERE {uslovie} {dan} '{data}'"""
        return s

    def Selected(self, rows, table):
        s = f"""SELECT DISTINCT {rows} FROM {table}"""
        return s

    def load_global(self):
        # sql ='SET GLOBAL local_infile = 1;'
        sql = 'SET GLOBAL local_infile = true;'
        # sql = 'SET sql_mode = "";'
        s = self.connectionSroki.execute(sql) 
        return s       

    # def load_local(self, val, tablename):
    def load_local(self):
        # sql ='SET GLOBAL local_infile = 1;'
        # s = self.connectionSroki.execute(sql)
        self.load_global()
        # sql ='LOAD DATA LOCAL INFILE "'+ val.replace('\\', '/')+'" REPLACE INTO TABLE '+ tablename +'  CHARACTER SET utf8 FIELDS TERMINATED BY ";"  ENCLOSED BY """" LINES TERMINATED BY "\r\n" ;'
        sql ='LOAD DATA LOCAL INFILE "new_file_.csv" REPLACE INTO TABLE a_all_data_106  CHARACTER SET utf8 FIELDS TERMINATED BY ";"  ENCLOSED BY """" LINES TERMINATED BY "\r\n" ;'
        # s = session.add(sql)
        # print(session.new)
        # session.commit()
        s = self.connectionSroki.execute(sql)
        self.connectionSroki.commit()
        return s