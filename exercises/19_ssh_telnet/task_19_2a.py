# -*- coding: utf-8 -*-
'''
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр verbose,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

verbose - это параметр функции send_config_commands, не параметр ConnectHandler!

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, verbose=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
'''
commands = [
    'ip a', 'ip route', 'whoami'
]
import netmiko
import yaml

def send_config_commands(device,config_commands, verbose=True):
    with netmiko.ConnectHandler(**device) as ssh:
        if verbose:
            print("Connecting to ", device['ip'])
        result=ssh.send_config_set(config_commands)
    return result

if __name__=="__main__":
    with open('devices.yaml') as ymlfile:
        devices=yaml.safe_load(ymlfile)
    for device in devices:
        print (send_config_commands(device,commands))