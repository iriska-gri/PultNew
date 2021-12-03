import numpy as np
import pandas as pd

from settings.conn import Orm
import os
from pathlib import Path
from VScomp import VScomp




vs = VScomp()

pd.options.display.float_format ='{:,.0f}'.format


class load106():
  

    def __init__(self, bd):
        VScomp.__init__(self)


        self.orm = Orm(bd)
    

    def encode_Control(self,filename):
        try:
            f = open(filename, 'rb')
            data = f.read()

            for x in ['cp1251','utf-8']:
                try:
                    data.decode(x)
                    print(x)
                    return x
                except:
                    print('Ошибка определения кодировки')
                    continue
            f.close()
            print('Возвращаем псевдопусто')
            return 'cp1251'
        except Exception:
            print('Возвращаем cp1251')
            return 'cp1251'

    # def namerows(self):



    def opencsv(self, names):
        name = names
        whatcode = self.encode_Control(name)
        razmer = os.path.getsize(name)
        

        

        if razmer < 600000000:
            file = open(name)
            numline = len(file.readlines())
            print("Маленький файл, количество строк: {}".format(numline))
            kolvoline = round(numline/10000)
        else:
            print("Большой файл, размер: {}".format(razmer))
        gg = 0
        filestr = str(Path(name).parent.joinpath("new_file_.csv")) # Сохранить каждый чанк в файл
        print('Пошла загрузка')
        for self.chunks in pd.read_csv(name, sep=';', header=None, dtype=str, chunksize=10000, engine='python', encoding = whatcode):

            self.chunk = self.chunks.drop(columns=[2,7,11,12,13,14,17,19,20,25])
        
            self.probeliZamena(3) # Удаление лишних пробелов в конце слова
            self.zeroValues() # Заменяем нулевые значения в столбцах
            self.replInColums() # Замена значений в столбце
            self.chunk = self.chunk.fillna('')
            self.replSimvol()
            self.replIskl()
            self.replRevers() # Поиск и замена текста на код (единичный случай)
            self.odrabDate()
            self.zamenaRows()
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
            self.orm.commit(self.orm.load_global())
            self.orm.commit(self.orm.load_local(filestr, self.inTable))
            Path(filestr).unlink()
            gg +=1
            if razmer < 600000000:
                print("Загружено: {} из {}".format(gg, kolvoline))
            else:
                print("Загружено: {}".format(gg))
        self.orm.connclose()
        print("Загрузка 106 завершена")
# ----------------------------------------------------------------------------------------------------------------------------- Проверка наличия данных в словаре
    def zamenaRows(self):
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
        
        spravrows = [1, 3, 8, 15, 22, 26] #Все столбцы для замены со справочником
        
        for y in spravrows:
            self.chunk[y].unique() #Выбираем уникальные значения стобца
            csvunik = self.chunk[y].unique()
            spravunik = []
            spradf = self.orm.SQLall(self.orm.Selected(myrows[y][0], myrows[y][3])) #Выбираем уникальные значения из справочника
            for x in range(len(spradf)): #Добавляем уникальные значения справочника
                spravunik.append(spradf[x][0])
            newslovo = []
            for x in range(len(csvunik)): #Проверяем каждое уникальное значение на присутсвие в справочнике
                if csvunik[x] in spravunik:
                    pass
                else:
                    newslovo.append(csvunik[x])
            for x in range(len(newslovo)):
                if newslovo[x] != '':
                    self.orm.commit(self.orm.loadSlovar(myrows[y][3], myrows[y][0], newslovo[x]))
                    if y != 8:
                        print("Добавлено новое значение: Таблица - {}; Слово - {}".format(myrows[y][3], newslovo[x]))
        for x in spravrows:
            self.spravkaZamena(myrows[x][2], myrows[x][3], myrows[x][1], x, myrows[x][0]) #Замена всех данных со справочником
        for x in myrows:
            self.chunk.rename(columns={x: myrows[x][0]}, inplace=True) # Переназывай столбцы

# ----------------------------------------------------------------------------------------------------------------------------- Обработка столбцов с датой
    def odrabDate(self):
        datarows = [9, 10, 27, 16, 18] # Все столбцы с датами
        for x in datarows:
            self.simvolZamena(x, '+')
            self.formatdataZamena(x)

# ----------------------------------------------------------------------------------------------------------------------------- Поиск и замена текста на код (единичный случай)
    def replRevers(self):
            stringZamena = self.chunk[23][~self.chunk[23].str.contains('0|1|2|3|4|5|6|7|8|9')].unique()  # Поиск всех нечисловых значений
            naZamenu = []
            for b in stringZamena:
                try:
                    a = self.orm.SQLall(self.orm.SelectWhere('cod_SNTS', self.spravSNTS, 'vid_object', '=', b))
                    naZamenu.append(a[0][0])
                except Exception:
                    continue
            for x in range(len(stringZamena)):
                self.chunk[23] = self.chunk[23].replace(to_replace = stringZamena[x], value = naZamenu[x])
                self.chunk[23] = self.chunk[23].astype(str)

# ------------------------------------------------------------------------------------------------------------- Заменяем текст с ошибками
    def replIskl(self):
        iskl = {0 : ("Официальный ответ НП по шаблону 'сведения НО соответствуют данным РО'", "Официальный ответ НП по шаблону 'Сведения НО соответствуют данным РО'"),
                    1 : ("Официальный ответ НП по шаблону 'В РО отсутствуют сведения о налогооблагаемом имуществе'", "Официальный ответ НП по шаблону 'в РО отсутствуют сведения о налогооблагаемом имуществе'"),
                    2 : ('Выявление типа ошибки препятствующей приему сведений о праве в АИС', 'Выявление типа ошибки, препятствующей приему сведений о праве в АИС'),
                    3 : ("Обработка причины, препятствующей приему сведений в АИС - 'Суммарный размер доли в праве в рассматриваемом периоде' >1'", "Обработка причины, препятствующей приему сведений в АИС - 'Суммарный размер доли в праве в рассматриваемом периоде >1'"),
                    4 : ("Добавление государственный орган в список", "Добавление государственного органа в список")}
        for i in iskl:
            self.chunk[3] = self.chunk[3].replace(iskl[i][0], iskl[i][1])  

# ------------------------------------------------------------------------------------------------------------- Заменяем интересующий символ на нужный
    def replSimvol(self):
        simvol = [3, 22] # Замена "" символа
        mysim = {0 : ('»', "'"),
                 1 : ('«', "'")
                }
        for x in simvol:
            for z in range(len(mysim)):
                self.chunk[x] = self.chunk[x].str.replace(mysim[z][0], mysim[z][1]) 
                # self.chunk[x] = self.chunk[x].str.replace('«', "'")  

# ------------------------------------------------------------------------------------------------------------- Замена значений в столбце
    def replInColums(self):
        zamena = {0 : (23, '-1', '35100'),
                  1 : (24, '-1', '0')
                 }    
        for z in range(len(zamena)):
            self.chunk[zamena[z][0]] = self.chunk[zamena[z][0]].replace(to_replace =zamena[z][1], value =zamena[z][2])

# ------------------------------------------------------------------------------------------------------------- Заменяем нулевые значения в столбцах
    def zeroValues(self): 
        zero = {0 : (5, 0), 
                1 : (10, "1900-01-01 00:00:00"),
                2 : (15, ''), 
                3 : (21, 0),
                4 : (23, '35100'),
                5 : (24, 0)
                }
        for z in range(len(zero)):
            self.chunk[zero[z][0]] = self.chunk[zero[z][0]].fillna(zero[z][1])

# ------------------------------------------------------------------------------------------------------------- Заменяем значения столбцов значениями из словоря
    def spravkaZamena(self, spravRows, spravTable, spravId, chunrows, sprav): 
        dfspravka = self.orm.mySQL(self.orm.Selected(spravRows, spravTable))
        self.chunk = self.chunk.merge(dfspravka, left_on=chunrows, right_on=sprav, how='left')
        self.chunk[chunrows] = self.chunk[spravId]
        del self.chunk[spravId]
        del self.chunk[sprav]

# ------------------------------------------------------------------------------------------------------------- Заменяем интересующий символ на нужный в дате
    def simvolZamena(self, numb, sim):    
        if (np.core.defchararray.find(self.chunk[numb].values.astype(str), sim) > -1).any() == True: # Просмотр наличия символа в строке
            self.chunk[numb] = self.chunk[numb].apply(lambda x: x.split(sim)[0]) # Производит замену после определнного символа

# ------------------------------------------------------------------------------------------------------------- Заменяем формат даты
    def formatdataZamena(self, numb):
        if numb == 27:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb], dayfirst=True).dt.date
        else:
            self.chunk[numb] = pd.to_datetime(self.chunk[numb], dayfirst=True)

# ------------------------------------------------------------------------------------------------------------- Удаление лишних пробелов в конце слова
    def probeliZamena(self, numb):
        self.chunk[numb] = self.chunk[numb].str.strip() # Удаляем все пробелы в столбце
  