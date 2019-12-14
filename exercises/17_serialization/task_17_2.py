# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''
import re
def parse_sh_cdp_neighbors(sh_cdp_str):
        """
        Creating inner (compreh_dict) and outer (result_dict) dictionaries.
        dev_name=name of local device
        match=interable regex to find local_intf,remote_intf, and nei_name (remote device name)
        for every line adding new interfaces to compreh_dict
        after cycle add all info to result_dict with local device name
        """
        compreh_dict={}
        result_dict={}
        match=re.finditer(r'(?P<nei_name>\w+)\s+(?P<local_intf>\w+\s[\d/]+)\s+\d+[\D\s]+[\d-]+\s+(?P<remote_intf>\w+\s[\d/]+)',sh_cdp_str) #regex for string with cdp neighbors
        dev_name=re.search(r'(\w+)>',sh_cdp_str).group(1) #regex for local device name
        for item in match:
                compreh_dict[item.group('local_intf')]={k:v for k,v in zip([item.group('nei_name')],[item.group('remote_intf')])} #create dict from comprehension of zip(list,list) ##zip(str,str) doesn't work
        result_dict[dev_name]=compreh_dict
        return result_dict

if __name__=="__main__":
        with open('sh_cdp_n_r1.txt') as file:
                print(parse_sh_cdp_neighbors(file.read()))