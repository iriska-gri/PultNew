import mysql.connector
from mysql.connector import Error
import getpass # Определить пользователя
import datetime
import pandas
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import getpass # Определить пользователя
from mysql.connector.locales.eng import client_error
# from urllib import quote_plus as urlquote
import urllib.parse
from urllib.parse import quote as urlquote


#--------------------------------------------------------------------------------------------------------- Подключение
class Orm():
    """ Создает список определенной длины, вставляя элемент в нужное место списка.
    Возвращает созданный список """
    def __init__(self, **kwargs):
        super(Orm, self).__init__(**kwargs)

        self.usering = getpass.getuser()
        
        if self.usering == 'systemsupport':
            self.set_connect = ("localhost", "root", "P@ssw0rd")
            self.myBDo = "okved"
        else:
            self.set_connect = ("10.252.44.38", "root", "P@ssw0rd")
            self.myBDo = "OKVED"
        
        # nameTable
        # self.connection = self.connect(*self.set_connect, "okved")


# #---------------------------------------------------------------------------------------------------------
    # def connect(self, host_names, user_name, user_password, db_name):
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:
            connection = create_engine(f"""mysql+mysqlconnector://{user_name}:%s@{host_names}/{db_name}""" % urlquote(user_password))
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return connection

    def conections(self, nameTable):
        con = self.connect(*self.set_connect, nameTable)
        return con

    def connclose(self):
        self.conections.close()
        print("Соединение закрыто")
    
    def DeleteWhere(self, table, t, data1, data2):
    # def DeleteWhere(self, table, t):
        # sql = f"""DELETE FROM {table} WHERE {t} >= {data1} AND {t} <= {data2}"""
        sql = f"""DELETE FROM {table} WHERE {t} >= '{data1}' AND {t} <= '{data2}'"""
        s = self.conections(self.myBDo).execute(sql)
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

