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
    # def __init__(self):
    def __init__(self, **kwargs):
        
        self.usering = getpass.getuser()
        
        if self.usering == 'systemsupport':
            self.set_connect = ("localhost", "root", "P@ssw0rd")
            # self.set_connect = ("localhost", "root")
        else:
            print(self.usering)
            
            # self.set_connect = ("10.252.44.38", "root", "P@ssw0rd")
            self.set_connect = ("10.252.44.38", "root", 'P@ssw0rd')
            # self.set_connect = ("10.252.45.177", "root")

#---------------------------------------------------------------------------------------------------------
    # def connect(self, host_names, user_name, user_password, db_name):
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:                                    #  ('postgres://user:%s@host/database' % urlquote('badpass'))
            # connection = create_engine(f"""mysql+mysqlconnector://{user_name}:"""%s f"""@{host_names}/{db_name}""" % urlquote('P@ssw0rd'))
            # connection = create_engine('mysql+mysqlconnector://user:%s@10.252.44.38/Sroki_svod' % urlquote('P@ssw0rd'))
            # connection = create_engine("mysql+mysqlconnector://"+user_name+":"+user_password+"@"+host_names+"/"+db_name)
            # connection = create_engine('mysql+mysqlconnector://{user}:%s@{host_name}/{db}' % urlquote(''))
            connection = create_engine(f"""mysql+mysqlconnector://{user_name}:%s@{host_names}/{db_name}""" % urlquote(user_password))
                        # .format(host_name = host_names,
                        #         user=user_name,
                        #         # pw=user_password,
                        #         db=db_name))
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return connection
    

        
    def mySQL(self, zapros, nameTable):
        # my_conn = create_engine("mysql+mysqldb://root:P@ssw0rd@/10.252.44.38/my_db")
        sql = pd.read_sql(zapros, con = self.connect(*self.set_connect, nameTable))
        # sql = pd.read_sql(zapros, con = self.connect())
        return sql

    def connclose(self):
        self.connection.close()
        print("Соединение закрыто")
    
    def SelectWhere(self, rows, table, uslovie, dan, data):
        OKVEDmindata = f"""SELECT DISTINCT {rows} FROM {table} WHERE {uslovie} {dan} '{data}'"""
        return OKVEDmindata

    def Selected(self, rows, table):
        OKVEDmindata = f"""SELECT DISTINCT {rows} FROM {table}"""
        return OKVEDmindata

