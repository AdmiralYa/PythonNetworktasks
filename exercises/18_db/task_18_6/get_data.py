# -*- coding: utf-8 -*-
'''
Задание 18.4

Для заданий 18 раздела нет тестов!

Скопировать файл get_data из задания 18.2.
Добавить в скрипт поддержку столбца active, который мы добавили в задании 18.3.

Теперь, при запросе информации, сначала должны отображаться активные записи,
а затем, неактивные. Если неактивных записей нет, не отображать заголовок "Неактивные записи".

Примеры выполнения итогового скрипта
$ python get_data.py
В таблице dhcp такие записи:

Активные записи:

-----------------  ----------  --  ----------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2   15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4     5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6    3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7    3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20    5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65  20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4   sw2  1
-----------------  ----------  --  ----------------  ---  -

Неактивные записи:

-----------------  ---------------  -  ---------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100  1  FastEthernet0/7  sw1  0
00:C5:B3:7E:9B:60  10.1.5.40        5  FastEthernet0/9  sw2  0
-----------------  ---------------  -  ---------------  ---  -

$ python get_data.py vlan 5

Информация об устройствах с такими параметрами: vlan 5

Активные записи:

-----------------  ---------  -  ---------------  ---  -
00:05:B3:7E:9B:60  10.1.5.4   5  FastEthernet0/9  sw1  1
00:B4:A3:3E:5B:69  10.1.5.20  5  FastEthernet0/5  sw2  1
-----------------  ---------  -  ---------------  ---  -

Неактивные записи:

-----------------  ---------  -  ---------------  ---  -
00:C5:B3:7E:9B:60  10.1.5.40  5  FastEthernet0/9  sw2  0
-----------------  ---------  -  ---------------  ---  -


$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5  sw1  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4  sw2  1
-----------------  ----------  --  ---------------  ---  -
'''

from sys import argv
import sqlite3

def get_data(db_name,*args):
    connection=sqlite3.connect(db_name)
    if len(args)==0:
        query_get_active='select * from dhcp where active=1'
        query_get_inactive='select * from dhcp where active=0'
        result_active=connection.execute(query_get_active)
        result_inactive=connection.execute(query_get_inactive)
    else: 
        query_active_with_args='select * from dhcp where {}=? and active=1'.format(key)
        query_inactive_with_args='select * from dhcp where {}=? and active=0'.format(key)
        result_active=connection.execute(query_active_with_args,(value,))
        result_inactive=connection.execute(query_inactive_with_args,(value,))
    print("Активные записи:\n"+"-"*40)
    for row in result_active:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("")
    print("-"*40)
    print("Неактивные записи:")
    for row in result_inactive:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("\n"+"-"*40,end='')

if __name__=="__main__":
    if len(argv)==1:
        get_data('dhcp_snooping.db')
    elif len(argv)==3:
        key,value=argv[1:]
        get_data('dhcp_snooping.db',key,value)
    else: 
        print("скрипт поддерживает только два или ноль аргументов")