'''
2. add_data.py - с помощью этого скрипта, выполняется добавление данных в БД. Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу (порядок добавления данных может быть произвольным, но сообщения должны выводиться аналогично выводу ниже):
$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac


На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

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
                switch=re.search(r'([^_]+)',dhcp_snoop_file).group()
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
        for file_name in dhcp_snooping_list:            # iterating through files in list
            query_dhcp_table='insert into dhcp (mac, ip, vlan, interface, switch) values (?,?,?,?,?)'
            for item in parse_dhcp_snoop_file(file_name): # iterating through list of variables received from parse_dhcp_snoop_file
                try:
                    with connection:
                        connection.execute(query_dhcp_table, item)
                except sqlite3.IntegrityError as err:
                    print('Возникла ошибка: ', err)
    else: print('База данных не существует. Перед добавлением данных, ее надо создать')

if __name__=="__main__":
    dhcp_files_list=glob.glob('*_dhcp_snooping.txt')
    add_data_to_db('dhcp_snooping.db','switches.yml',dhcp_files_list)