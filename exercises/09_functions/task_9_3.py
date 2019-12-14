# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):
    '''
    Функция обрабатывает файл, вытаскивает из него названия интерфейсов
    далее если строка содержит 'access vlan', разбиваем строку по пробелам, берем последний элемент и конвертируем его
    если строка содержит 'allowed vlan', повторяем те же процедуры, только в цикле меняем str значения на int
    '''
    intf_list=[]
    access_vlan={}
    trunk_vlan={}
    with open(config_filename, 'r') as file:
        for line in file:
            if line.startswith('interface'):
                intf=line.split()
            if 'access vlan' in line:
                vlan_numbers=line.split()
                access_vlan[intf[1]]=int(vlan_numbers[-1])
            elif 'allowed vlan' in line:
                vlan_numbers=line.split()[-1].split(',')
                vlan_numbers=[int(item) for item in vlan_numbers]
                trunk_vlan[intf[1]]=vlan_numbers
    result=(access_vlan,trunk_vlan)
    return result

ans=get_int_vlan_map('config_sw1.txt')
for item in ans:
    print(item)