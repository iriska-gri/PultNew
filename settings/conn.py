import mysql.connector
from mysql.connector import Error
import getpass # Определить пользователя
import datetime
import pandas
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# import sqlalchemy.sql.default_comparator

#--------------------------------------------------------------------------------------------------------- Подключение
class Orm():
    """ Создает список определенной длины, вставляя элемент в нужное место списка.
    Возвращает созданный список """
    # def __init__(self):
    def __init__(self, **kwargs):
        # self.nameBD = "okved"
        self.set_connect = ("localhost", "root", "")
        # self.set_connect = ("10.252.44.38", "root", "P@ssw0rd", "proba")
        # self.connection = self.connect(*self.set_connect, self.nameBD)

#---------------------------------------------------------------------------------------------------------
    def connect(self, host_names, user_name, user_password, db_name):
        """Создается подключение к серверу"""
        connection = None
        try:
            connection = create_engine("mysql+mysqlconnector://{user}:{pw}@{host_name}/{db}"
                        .format(host_name = host_names,
                                user=user_name,
                                pw=user_password,
                                db=db_name))
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"--------------------ОШИБКА---------------- '{e}' ")
        return connection
        
    def mySQL(self, zapros, nameTable):
        # sql = pd.read_sql(zapros, con = self.connection)
        sql = pd.read_sql(zapros, con = self.connect(*self.set_connect, nameTable))
        return sql
    
    def SelectWhere(self, rows, table, uslovie, data):
        OKVEDmindata = f"""SELECT DISTINCT {rows} FROM {table} WHERE {uslovie} > '{data}'"""
        return OKVEDmindata

    def Selected(self, rows, table):
        OKVEDmindata = f"""SELECT DISTINCT {rows} FROM {table}"""
        return OKVEDmindata