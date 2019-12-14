# -*- coding: utf-8 -*-
'''
Задание 18.5

Для заданий 18 раздела нет тестов!

После выполнения заданий 18.1 - 18.5 в БД остается информация о неактивных записях.
И, если какой-то MAC-адрес не появлялся в новых записях, запись с ним,
может остаться в БД навсегда.

И, хотя это может быть полезно, чтобы посмотреть, где MAC-адрес находился в последний раз,
постоянно хранить эту информацию не очень полезно.

Например, если запись в БД уже больше месяца, то её можно удалить.

Для того, чтобы сделать такой критерий, нужно ввести новое поле,
в которое будет записываться последнее время добавления записи.

Новое поле называется last_active и в нем должна находиться строка,
в формате: YYYY-MM-DD HH:MM:SS.

В этом задании необходимо:
* изменить, соответственно, таблицу dhcp и добавить новое поле.
 * таблицу можно поменять из cli sqlite, но файл dhcp_snooping_schema.sql тоже необходимо изменить
* изменить скрипт add_data.py, чтобы он добавлял к каждой записи время

Получить строку со временем и датой, в указанном формате, можно с помощью функции datetime в запросе SQL.
Синтаксис использования такой:
sqlite> insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
   ...> values ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1', '0', datetime('now'));

То есть вместо значения, которое записывается в базу данных, надо указать datetime('now').

После этой команды в базе данных появится такая запись:
mac                ip               vlan        interface        switch      active      last_active
-----------------  ---------------  ----------  ---------------  ----------  ----------  -------------------
00:09:BC:3F:A6:50  192.168.100.100  1           FastEthernet0/7  sw1         0           2019-03-08 11:26:56
'''


import sqlite3
import re
import glob
import yaml
from create_db import check_if_db_exists

regex=re.compile(r'(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)') # take mac, ip , vlan, interface from sh dhcp snooping

def parse_yml_file(yml_file):
    '''
    read file, iterate through items in dict.values()
    append these vars to list
    return list of tuples
    '''
    switch_list=[]
    with open(yml_file) as ymlfile:
        reader=yaml.safe_load(ymlfile)
        for row in reader.values():
            for key,value in row.items():
                switch_list.append((key,value))
    return switch_list

def parse_dhcp_snoop_file(dhcp_snoop_file):
    '''
    open file, iterate through every line
    match string with regex, adding this to correspond vars
    add vars + switch (which is name of file) to the list of tuples
    return list of tuples
    '''
    match_list=[]
    with open(dhcp_snoop_file,newline='') as dhcp_file:
        for line in dhcp_file:
            match=regex.search(line)
            if match:
                mac,ip,vlan,interface=match.groups()
                switch=re.search(r'([^_]+)',re.sub(r'(\S+\\)','',dhcp_snoop_file)).group()   # switch var gets from re.sub, which cuts down upper dir
                match_list.append((mac,ip,vlan,interface,switch))
    return match_list

def add_data_to_db(db_name,switch_info, dhcp_snooping_list):
    if check_if_db_exists(db_name):
        print('Добавляю данные в таблицу switches...')
        connection=sqlite3.connect(db_name)             # connecting to database
        for item in parse_yml_file(switch_info):        # going through all tuples in .yml file
            try:
                with connection:
                    query_switch_table='insert into switches (hostname, location) values (?,?)'
                    connection.execute(query_switch_table,item)     # execute query
            except sqlite3.IntegrityError as err:
                print('Возникла ошибка: ', err)

        print('Добавляю данные в таблицу dhcp...')
        query_dhcp_table="insert into dhcp (mac, ip, vlan, interface, switch, active, last_active) values (?,?,?,?,?,1,datetime('now'))"
        query_active_false='update dhcp set active=0'
        query_replace_true="replace into dhcp values (?,?,?,?,?,1,datetime('now'))"
        with connection:
            connection.execute(query_active_false)
        for file_name in dhcp_snooping_list:            # iterating through files in list
            for item in parse_dhcp_snoop_file(file_name): # iterating through list of variables received from parse_dhcp_snoop_file
                try:
                    with connection:
                        connection.execute(query_dhcp_table, item)
                except sqlite3.IntegrityError as err:
                    with connection:
                        connection.execute(query_replace_true,item)

    else: print('База данных не существует. Перед добавлением данных, ее надо создать')

if __name__=="__main__":
    dhcp_files_list=glob.glob('new_data/*_dhcp_snooping.txt')
    add_data_to_db('dhcp_snooping.db','switches.yml',dhcp_files_list)