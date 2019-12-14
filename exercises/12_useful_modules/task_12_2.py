# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''
import ipaddress

def check_if_ip(ip_add):              #Check if it the second ip is ip or just last octet (10.10.10.1-3 or 10.10.10.1-10.10.10.10)
    try:
        ipaddress.ip_address(ip_add)
        return True
    except ValueError:
        return False

def convert_ranges_to_ip_list(ip_add_list):
    ip_add_list_splitted=[]
    result_list=[]
    for ip_add in ip_add_list:
        ip_add_list_splitted.append(ip_add.split('-'))  # split ip range to list
    for item in ip_add_list_splitted:
        if len(item) == 1:                              # if it is not range
            result_list.append(str(ipaddress.ip_address(item[0])))  # just append
        elif check_if_ip(item[-1]) == False:                        # if it is 10.1.1.1-3
            for iter in range(int(item[-1])):                       # check range
                result_list.append(str(ipaddress.ip_address(item[0]) + iter)) # apply str from ip ++
        else:
            iterable=int(ipaddress.ip_address(item[1]))-int(ipaddress.ip_address(item[0])) # substraction from last ip to first, take the range
            for iter in range(iterable+1):                                                 # cycle + 1 and append this to list
                result_list.append(str(ipaddress.ip_address(item[0]) + iter))
    return(result_list)

if __name__=="__main__":
    ip_list=['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
    print(convert_ranges_to_ip_list(ip_list))