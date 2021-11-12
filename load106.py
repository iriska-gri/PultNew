import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta, date
from sqlalchemy import create_engine
from settings.conn import Orm
from settings.readFiles import read_files
import json
import io
from io import BytesIO
import os
import requests
import base64
from datetime import datetime, timedelta
import time
from pathlib import Path

orm = Orm()

pd.options.display.float_format ='{:,.0f}'.format


class load106(Orm):
    def __init__(self, **kwargs):
        super(load106, self).__init__(**kwargs)
        if self.usering == 'systemsupport':
            self.myBD = "sroki_svod"
            self.inTablek = 'a_all_data_106_k'
            self.inTable = 'a_all_data_106'
            self.spravSNTS = 'sprav_snts_svod'
        else:
            self.myBD = "Sroki_svod"
            self.inTable = 'a_all_data_106'
            self.spravSNTS = 'sprav_SNTS_svod'
        
    def encode_Control(self,filename):
        try:
            f = open(filename, 'rb')
            data = f.read()

            for x in ['cp1251','utf-8']:
                try:
                    data.decode(x)
                    return x
                except:
                    print('Ошибка определения кодировки')
                    continue
            f.close()
            return ''
        except Exception:
            return 'cp1251'

    def opencsv(self, names):
    # def opencsv(self):
        # name='C:/Users/systemsupport/Desktop/report106_1000005384_20211112_080920.csv'
        name = names
        whatcode = self.encode_Control(name)
        myrows = {0 : ('history_id', ''),
                  1 : ('actions', 'id_actions', 'id_actions, actions', 'sprav_actions'),
                  3 : ('task_step_name', 'task_step_id', 'task_step_id, task_step_name', 'sprav_task_step_name'),
                  4 : ('card_id', ''),
                  5 : ('card_task_id', ''),
                  6 : ('tax_code', ''),
                  8 : ('login', 'id_login', 'id_login, login', 'sprav_login'),
                  9 : ('start_ts_reg', ''),
                  10 : ('end_ts_reg', ''),
                  15 : ('org_title', 'id_org_title', 'id_org_title, org_title', 'sprav_org_title'), 
                  16 : ('out_date', ''),
                  18 : ('in_date', ''),
                  21 : ('registration_number', ''),
                  22 : ('life_situation_name', 'id_life_situation_name', 'id_life_situation_name, life_situation_name', 'sprav_life_situation_name'),
                  23 : ('snts_code', ''),
                  24 : ('dubl', ''),
                  26 : ('appeal_source', 'id_appeal_source', 'id_appeal_source, appeal_source', 'sprav_appeal'),
                  27 : ('date_reg_appeal', '')}

        datarows = [9, 10, 27, 16, 18] # Все столбцы с датами
        spravrows = [1, 3, 8, 15, 22, 26] #Все столбцы для замены со справочником
        simvol = [3, 22] # Замена "" символа

        file = open(name)
        numline = len(file.readlines())
        kolvoline = round(numline/10000)
        # print(kolvoline)
        gg = 0
        filestr = str(Path(name).parent.joinpath("new_file_.csv")) # Сохранить каждый чанк в файл
        for chunk in pd.read_csv(name, sep=';', header=None, dtype=str, chunksize=10000, engine='python', encoding = whatcode):
        # for chunk in pd.read_csv(name, sep=';', header=None, dtype=str, chunksize=10000, engine='python', encoding='utf-8'):
            # while gg < 1:
            self.chunk = chunk.drop(columns=[2,7,11,12,13,14,17,19,20,25])
            
        
            self.probeliZamena(3)
            self.chunk[23] = self.chunk[23].fillna('35100')
            self.chunk[5] = self.chunk[5].fillna(0)
            self.chunk[24] = self.chunk[24].fillna(0)
            self.chunk[24] = self.chunk[24].replace(to_replace ='-1', value ='0')
            self.chunk[10] = self.chunk[10].fillna("1900-01-01 00:00:00")
            self.chunk[15] = self.chunk[15].fillna('')
            self.chunk[23] = self.chunk[23].replace(to_replace ='-1', value ='35100')
            self.chunk[21] = self.chunk[21].fillna(0)
            self.chunk = self.chunk.fillna('')
            # ----------------------------------------------------------------------------------------------------------------------------- Поиск и замена текста на код (единичный случай)
            stringZamena = self.chunk[23][~self.chunk[23].str.contains('0|1|2|3|4|5|6|7|8|9')].unique()  # Поиск всех нечисловых значений
            naZamenu = []
            for b in stringZamena:
                try:
                    a = orm.mySQL(orm.SelectWhere('cod_SNTS', self.spravSNTS, 'vid_object', '=', b), self.myBD)
                    naZamenu.append(a['cod_SNTS'][0])
                except Exception:
                    continue
            for x in range(len(stringZamena)):
                self.chunk[23] = self.chunk[23].replace(to_replace = stringZamena[x], value = naZamenu[x])
                self.chunk[23] = self.chunk[23].astype(str)
            
            # ----------------------------------------------------------------------------------------------------------------------------- Проверка наличия данных в словаре
            for y in spravrows:
                self.chunk[y].unique() #Выбираем уникальные значения стобца
                csvunik = self.chunk[y].unique()
                spravunik = []
                spradf = orm.mySQL(orm.SelecteAll(myrows[y][0], myrows[y][3]), self.myBD) #Выбираем уникальные значения из справочника
                for x in range(len(spradf)): #Добавляем уникальные значения справочника
                    spravunik.append(spradf[myrows[y][0]][x])
                newslovo = []
                # print(range(len(csvunik)))
                # print(csvunik)
                for x in range(len(csvunik)): #Проверяем каждое уникальное значение на присутсвие в справочнике
                    # print(x)
                    # print(csvunik[x])
                    if csvunik[x] in spravunik:
                        pass
                    else:
                        newslovo.append(csvunik[x])
                # self.chunk[3] = self.chunk[3].str.replace('Сведения НО соответствуют данным РО', "сведения НО соответствуют данным РО")
                for x in simvol:

                    self.chunk[x] = self.chunk[x].str.replace('»', "'") 
                    self.chunk[x] = self.chunk[x].str.replace('«', "'")  
                for x in range(len(newslovo)):
                    if newslovo[x] != '':
                        orm.loadSlovar(myrows[y][3], myrows[y][0], newslovo[x])
                        print("Добавлено новое значение: Таблица - {}; Слово - {}".format(myrows[y][3], newslovo[x]))
            # -----------------------------------------------------------------------------------------------------------------------------
            for x in datarows:
                self.simvolZamena(x, '+')
                self.formatdataZamena(x)

            for x in spravrows:
                self.spravkaZamena(myrows[x][2], myrows[x][3], myrows[x][1], x, myrows[x][0]) #Замена всех данных со справочником
            for x in myrows:
                self.chunk.rename(columns={x: myrows[x][0]}, inplace=True) # Переназывай столбцы
            # ------------------------------------------------------------------------------------------- Подготовка экселевского файла
            act = [16, 34, 63]
            for x in act:
                self.chunk.loc[self.chunk['actions'] == x, 'task_step_name'] = 1
            self.chunk = self.chunk.astype({'history_id': int}) #Делаем столбец числовым
            self.chunk.loc[(self.chunk.actions == 34), 'history_id'] *= -1
            self.chunk.insert(loc=0, column='status_task', value = 3)

            self.chunk = self.chunk.drop_duplicates()
            # ------------------------------------------------------------------------------------------- Заливка файла в базу
            self.chunk.to_csv(filestr, sep=';', na_rep=r'\N', quoting = 1, mode='a', header=False, index=False)
            orm.load_local(filestr, self.inTable)
            Path(filestr).unlink()
            gg +=1
            print("Загружено: {} из {}".format(gg, kolvoline))
        print("Загрузка 106 завершена")
                
    def spravkaZamena(self, spravRows, spravTable, spravId, chunrows, sprav):
        dfspravka = orm.mySQL(orm.Selected(spravRows, spravTable), self.myBD)
        self.chunk = self.chunk.merge(dfspravka, left_on=chunrows, right_on=sprav, how='left')
        self.chunk[chunrows] = self.chunk[spravId]
        del self.chunk[spravId]
        del self.chunk[sprav]

    def simvolZamena(self, numb, sim):    
        if (np.core.defchararray.find(self.chunk[numb].values.astype(str), sim) > -1).any() == True: # Просмотр наличия символа в строке
            self.chunk[numb] = self.chunk[numb].apply(lambda x: x.split(sim)[0]) # Производит замену после определнного символа

    # def zamenakov(self, numb, sim):
        

    def formatdataZamena(self, numb):
        # dataexcel =  pd.to_datetime(ss.columns[0]).date()
        # datastr = str(dataexcel)
        # datasplit = datastr.split('-')
        # databse = datasplit[0] + '-' + datasplit[2] + '-' + datasplit[1]
        if numb == 27:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb], dayfirst=True).dt.date
        else:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb], dayfirst=True)
    
    def probeliZamena(self, numb):
        self.chunk[numb] = self.chunk[numb].str.strip() # Удаляем все пробелы в столбце


if __name__ == '__main__':
    load106().opencsv() 
  