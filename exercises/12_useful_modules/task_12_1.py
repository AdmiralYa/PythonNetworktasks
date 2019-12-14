# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
import subprocess
import ipaddress
success_list=[]
false_list=[]
def ping_ip_addresses(ip_addresses_list):
    for item in ip_addresses_list:
        result=subprocess.run('ping {}'.format(ipaddress.ip_address(item)))
        if result.returncode==0:
            success_list.append(item)
        else: false_list.append(item)
    return (success_list,false_list)

if __name__=="__main__":
    ping_check=['10.198.20.137','8.8.8.8', '1.1.1.1' , '2.2.2.2' ]
    print(ping_ip_addresses(ping_check))

