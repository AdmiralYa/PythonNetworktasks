# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
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
    except netmiko.NetmikoAuthError as err:
        print(err)

if __name__=="__main__":
    with open('devices.yaml') as dev_file:
        dev_list=yaml.safe_load(dev_file)
    for device in dev_list:
        print(send_show_command(device,command))