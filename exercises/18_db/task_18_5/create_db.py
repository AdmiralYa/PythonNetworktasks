'''
Задание 18.1

Для заданий 18 раздела нет тестов!

Необходимо создать два скрипта:

1. create_db.py
2. add_data.py

1. create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
  * должна выполняться проверка наличия файла БД
  * если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql, должна быть создана БД
  * имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует
'''
import sqlite3
import os

def check_if_db_exists(db_name):
    result=True if os.path.exists(db_name) else False
    return result

def create_db(db_name,db_scheme_name):
    if check_if_db_exists(db_name):
        print("База данных существует")
    else:
        print('Создаю базу данных...')
        connection=sqlite3.connect(db_name)
        with open(db_scheme_name) as schema:
            schema_str=schema.read()
        connection.executescript(schema_str)

if __name__=="__main__":
    create_db('dhcp_snooping.db','dhcp_snooping_schema.sql')