# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''
import yaml
import netmiko
command = 'ip route'

def send_show_command(device,command):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            #ssh.enable()
            result=ssh.send_command(command)
            return result
    except netmiko.NetMikoTimeoutException as err:
        print(err)
    except netmiko.NetMikoAuthenticationException as err:
        print(err)

if __name__=="__main__":
    with open('devices.yaml') as dev_file:
        dev_list=yaml.safe_load(dev_file)
    for device in dev_list:
        print(send_show_command(device,command))