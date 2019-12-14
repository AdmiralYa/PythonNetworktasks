# -*- coding: utf-8 -*-
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом,
чтобы в значении словаря она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.
Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re
def get_ip_from_cfg(filename):
    result_dict={}
    result_list=[]
    int_flag=False
    with open(filename) as file:
        for line in file:
            if line.startswith(' ip address'):
                ip,mask=(re.search('\D+([\w.]+)\s([\w.]+)',line).group(1,2)) #unzip ip and mask to the appropriate variables
                result_list.append((ip,mask))           #append (ip,mask) to list
            if line.startswith("interface"):
                int_flag=True
                int_name=re.search(r'\w+\s+([\w/.]+)',line).group(1) #name of interface
            if line=='!\n':
                if int_flag==True and int_name!="" and len(result_list)!=0:
                    result_dict[int_name]=(result_list)     #dictionary key=interface name, value=list of (ip,mask)
                int_name=""
                int_flag=False
                result_list=[]
    return result_dict

if __name__=="__main__":
    filename='config_r2.txt'
    print(get_ip_from_cfg(filename))
