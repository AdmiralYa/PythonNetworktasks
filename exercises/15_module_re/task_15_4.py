# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''
import re
def get_ints_without_description(filename):
    int_flag=False
    result_list=[]
    with open(filename) as file:
        for line in file:
            if line.startswith("interface"):
                int_flag=True
                int_name=re.search(r'\w+\s+([\w/.]+)',line).group(1)
            if line.startswith(" description"):
                int_flag=False
            if line=='!\n':
                if int_flag==True and int_name!="":
                    result_list.append(int_name)
                int_name=""
    return result_list

if __name__=="__main__":
    print(get_ints_without_description("config_r1.txt"))