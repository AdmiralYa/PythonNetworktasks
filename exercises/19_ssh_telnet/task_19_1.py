# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''
# import yaml
# import netmiko
# command = 'ip route'

# def send_show_command(device,command):
#     with netmiko.ConnectHandler(**device) as ssh:
#         #ssh.enable()
#         result=ssh.send_command(command)
#         return result

# if __name__=="__main__":
#     with open('devices.yaml') as dev_file:
#         dev_list=yaml.safe_load(dev_file)
#     for device in dev_list:
#         print(send_show_command(device,command))

import re
list_items='Tunnel1                    1.1.1.1         YES manual up                    up    \nTunnel20                    unassigned         YES manual up                    up    '
result=re.findall(r'Tunnel(\d+) ',list_items)
print(result)