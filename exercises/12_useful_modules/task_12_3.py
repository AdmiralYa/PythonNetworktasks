# -*- coding: utf-8 -*-
'''
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
'''
from tabulate import tabulate
from task_12_1 import ping_ip_addresses

def print_ip_table(reach_list, unreach_list):
    header=['Reachable', 'Unreachable']
    result={key:value for key,value in zip(header,(reach_list,unreach_list))}
    print(tabulate(result, headers='keys'))

if __name__=="__main__":
    ping_check=['10.198.20.137','8.8.8.8', '1.1.1.1', '10.198.20.153','8.8.4.4' ]
    reach,unreach = (ping_ip_addresses(ping_check))
    print_ip_table(reach,unreach)