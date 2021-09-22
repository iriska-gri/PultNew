DATABASE = {
    'drivername': 'MySQL', #Тут можно использовать MySQL или другой драйвер
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '',
    'database': 'okved'
}

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
engine  = create_engine(URL(**DATABASE))