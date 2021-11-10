import mysql.connector
from mysql.connector import Error
# import pymssql
import getpass # Определить пользователя
import datetime
import pandas
import numpy as np
import pandas as pd
# import sqlalchemy as db
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

        self.sessionSroki = Session(bind=self.connectionSroki)

# #---------------------------------------------------------------------------------------------------------
    # def connect(self, host_names, user_name, user_password, db_name):
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:
            connection = create_engine(f"""mysql+mysqlconnector://{user_name}:%s@{host_names}/{db_name}""" % urlquote(user_password))
            # print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return connection

    def cursors(self, sqll):
        connection = self.connectionSroki.raw_connection()
        cursor = connection.cursor()
        cursor.execute(sqll)
        return cursor.fetchall()
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

    # def Selected(self, rows, table):
    def Selected(self, rows, table): 
        # connection = self.connectionSroki.raw_connection()
        # cursor = connection.cursor()
        s = f"""SELECT DISTINCT {rows} FROM {table}"""
        return s
        # cursor.execute(sql)
        
        # self.cursors(f"""SELECT DISTINCT * FROM d_spy_mini""")
        
        # self.connectionSroki.close()
        
        # names = [row[0] for row in s]
        # print names
        # s = pd.read_sql(sql, con = self.connectionSroki)
        # s = self.connectionSroki.execute(sql)
        # self.connectionSroki.commit()
        # s = 'hello' 
        # ql = f"""SELECT DISTINCT * FROM d_spy_mini""" 
        # s = self.connectionSroki.query(a).all()
        
        # sql = f"""SELECT DISTINCT {rows} FROM {table}"""
        # sql = f"""SELECT DISTINCT * FROM d_spy_mini"""
        # s = pd.read_sql_query(sql, self.connectionSroki)
        # s = self.connectionSroki.execute(sql)
        # return cursor.fetchall()

    def load_global(self):
        # sql ='SET GLOBAL local_infile = 1;'
        sql = 'SET GLOBAL local_infile = true;'
        # sql = 'SET sql_mode = "";'
        s = self.sessionSroki.execute(sql) 
        return s       

    def load_local(self, val, tablename):
        self.load_global()
        sql ='LOAD DATA LOCAL INFILE "'+ val.replace('\\', '/')+'" REPLACE INTO TABLE '+ tablename +'  CHARACTER SET utf8 FIELDS TERMINATED BY ";"  ENCLOSED BY """" LINES TERMINATED BY "\r\n" ;'
        s = self.sessionSroki.execute(sql)
        self.sessionSroki.commit()
        return s

    def loadSlovar(self, tablename, rowsname, arr1):
        sql = f'''INSERT INTO {tablename} ({rowsname}) SELECT "{arr1}"'''
        s = self.sessionSroki.execute(sql)
        self.sessionSroki.commit()
        return s