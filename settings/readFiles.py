#Подключаем модуль
import pandas as pd
import os




class read_files():
    def __init__(self, **kwargs):
        super(read_files, self).__init__(**kwargs)
        self.track = 'C:/Users/systemsupport/Desktop/load_OKVED/excel/'

    def mesto(self):
         # Каталог из которого будем брать файлы
        directory =  self.track
        files = os.listdir(directory)
        # h = files[1]
         #Получаем список файлов в переменную files
        # print(h)
        return files

# if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
#     a().b()  # то запускаем функцию main()