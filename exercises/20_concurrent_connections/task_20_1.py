# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_add(ip):
    result=subprocess.run('ping {}'.format(ip),stdout=subprocess.PIPE).returncode
    return [ip,result]

def ping_ip_addresses(ip_list,limit=3):
    result_list=[]
    success_list=[]
    false_list=[]
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result_list=[executor.submit(ping_add,ip) for ip in ip_list]
    for f in as_completed(result_list):
        if f.result()[1]==0:
            success_list.append(f.result()[0])
        else: false_list.append(f.result()[0])
    return (success_list,false_list)

if __name__=="__main__":
    ip_list=['10.198.20.159', '10.198.20.151']
    print(ping_ip_addresses(ip_list))
