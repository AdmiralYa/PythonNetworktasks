# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


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
    access_flag=False
    with open(config_filename, 'r') as file:
        for line in file:
            if line.startswith('interface'):
                intf=line.split()
                access_flag=False ## сбрасываем флаг каждый раз, когда конфиг ссылается на новый интерфейс
            if 'access vlan' in line:
                vlan_numbers=line.split()
                access_vlan[intf[1]]=int(vlan_numbers[-1])

            elif 'allowed vlan' in line:
                vlan_numbers=line.split()
                vlan_numbers=vlan_numbers[-1].split(',')
                for item in range(len(vlan_numbers)):
                    vlan_numbers[item]=int(vlan_numbers[item])
                trunk_vlan[intf[1]]=vlan_numbers

            if 'switchport mode access' in line: ## смотрим, есть ли access
                access_flag=True
            if access_flag==True and len(intf)!=0: ## если это access и есть название интерфейса, то пилим дефолтное значение в список
                access_vlan.setdefault(intf[1], 1)
    result=(access_vlan,trunk_vlan)
    return result

ans=get_int_vlan_map('config_sw2.txt')
for item in ans:
    print(item)