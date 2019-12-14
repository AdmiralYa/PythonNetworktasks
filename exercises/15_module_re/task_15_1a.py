# -*- coding: utf-8 -*-
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
import re
def get_ip_from_cfg(filename):
    result_dict={}
    int_flag=False
    with open(filename) as file:
        for line in file:
            if line.startswith(' ip address'):
                ip,mask=(re.search('\D+([\w.]+)\s([\w.]+)',line).group(1,2)) #unzip ip and mask to the appropriate variables
            if line.startswith("interface"):
                int_flag=True
                int_name=re.search(r'\w+\s+([\w/.]+)',line).group(1) #name of interface
            if line=='!\n':
                if int_flag==True and int_name!="" and ip!=0:
                    result_dict[int_name]=(ip,mask)     #dictionary key=interface name, value=ip,mask
                int_name=""
                int_flag=False
                ip=mask=0
    return result_dict

if __name__=="__main__":
    filename='config_r1.txt'
    print(get_ip_from_cfg(filename))
