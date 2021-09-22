import mysql.connector
from mysql.connector import Error
import getpass # Определить пользователя
import datetime
import pandas
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

#--------------------------------------------------------------------------------------------------------- Подключение
class Orm():
    """ Создает список определенной длины, вставляя элемент в нужное место списка.
    Возвращает созданный список """
    def __init__(self):
        self.set_connect = ("localhost", "root", "", "okved")
        # self.set_connect = ("10.252.44.38", "root", "P@ssw0rd", "proba")
        self.connection = self.connect(*self.set_connect)

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
        
# ------------------------------------------------------------------------------------------
    def commit_to(self):
        """Подтверждение отправки данных"""
        try:
            self.connection.commit()
        except Exception:
            self.connection.rollback()
# ------------------------------------------------------------------------------------------
    def exec_query(self, query, msg = ''):
        """Курсор для записи данных"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except Error as e:
            print(f"The error '{e}' occurred")
# ------------------------------------------------------------------------------------------
    def exec_query_rows(self, query):
        """Курсор для чтения данных"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"The error '{e}' occurred")
# ------------------------------------------------------------------------------------------


    def selectOneTable1(self):
        # """Выбирает задания из таблицы по пользователю"""
        # query = f"""SELECT DISTINCT * FROM viruzka_np;"""
        # return self.exec_query_rows(query)
        df = pandas.read_sql("SELECT * FROM persons", con = engine)
        return df