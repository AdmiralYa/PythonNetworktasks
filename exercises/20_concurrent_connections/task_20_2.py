# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''
import yaml
import netmiko
import datetime
def send_show_command_to_devices(devices, command, filename, limit=3):
    with open(devices) as devices:
        device_list=yaml.safe_load(devices)
    with open(filename,'w') as wfile:
        for device in device_list:
            with netmiko.ConnectHandler(**device) as ssh:
                ssh.send_command(command)                                                      # TODO: complete

if __name__=="__main__":
    command='sh ip int br'
    send_show_command_to_devices('devices.yaml',command, 'task_20_2.txt')
    # with open('devices.yaml') as devices:
    #     for device in devices:
    #         send_show_command_to_devices(device,command, 'task_20_2.txt')

