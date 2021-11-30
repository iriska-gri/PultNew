# import mysql.connector
from mysql.connector import Error
# import pymssql
# import getpass # Определить пользователя
# import datetime
# import pandas
import numpy as np
import pandas as pd
# import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from mysql.connector.locales.eng import client_error
# from main import ExampleApp
# import urllib.parse
from urllib.parse import quote as urlquote
from VScomp import VScomp

vs = VScomp()
# ex = ExampleApp()
# session = Session()

#--------------------------------------------------------------------------------------------------------- Подключение
class Orm():
    """ Создает список определенной длины, вставляя элемент в нужное место списка.
    Возвращает созданный список """
    def __init__(self, bdSession):
        # super(Orm, self).__init__(**kwargs)
        VScomp.__init__(self)

        self.mySession = self.session(bdSession)
        # self.sessionSroki = self.session(self.myBD)
        # self.sessionOKVED = self.session(self.myBDokved)

    def session(self, bd):
        connection = self.connect(*self.set_connect, bd)
        session = Session(bind=connection)
        return session

# #---------------------------------------------------------------------------------------------------------
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:
            connection = create_engine(f"""mysql+mysqlconnector://{user_name}:%s@{host_names}/{db_name}""" % urlquote(user_password))
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return connection

    # def cursors(self, sqll):
    #     connection = self.connectionSroki.raw_connection()
    #     cursor = connection.cursor()
    #     cursor.execute(sqll)
    #     return cursor.fetchall()

    def connclose(self):
        self.mySession.close()
        print("Соединение закрыто")
# ------------------------------------------------------------------------------------------------------------------------ Сессия
    def SQLall(self, newSQL):
        sql = newSQL
        result = self.mySession.execute(sql).all()
        return result

    def mySQL(self, newSQL):
        sql = pd.read_sql(newSQL, self.mySession.bind)
        return sql

    def commit(self, newSQL):
        sql = newSQL
        result = self.mySession.execute(sql)
        self.mySession.commit()
        return result

# ------------------------------------------------------------------------------------------------------------------------ Запросы    
    def DeleteWhere(self, table, t, data1, data2):
        sql = f"""DELETE FROM {table} WHERE {t} >= '{data1}' AND {t} <= '{data2}'"""
        return sql

    def SelectWhere(self, rows, table, uslovie, dan, data):
        sql = f"""SELECT DISTINCT {rows} FROM {table} WHERE {uslovie} {dan} '{data}'"""
        return sql

    def Selected(self, rows, table): 
        sql = f"""SELECT DISTINCT {rows} FROM {table}"""
        return sql

    def SelecteAll(self, rows, table): 
        sql = f"""SELECT {rows} FROM {table}"""
        return sql

    def load_global(self):
        sql = 'SET GLOBAL local_infile = true;'
        return sql      

    def load_local(self, val, tablename):
        sql ='LOAD DATA LOCAL INFILE "'+ val.replace('\\', '/')+'" REPLACE INTO TABLE '+ tablename +'  CHARACTER SET utf8 FIELDS TERMINATED BY ";"  ENCLOSED BY """" LINES TERMINATED BY "\r\n" ;'
        return sql

    def loadSlovar(self, tablename, rowsname, arr1):
        sql = f'''INSERT INTO {tablename} ({rowsname}) SELECT "{arr1}"'''
        return sql