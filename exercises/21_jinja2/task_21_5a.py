# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''
from sys import argv
import jinja2
from pprint import pprint
import netmiko
from itertools import repeat
import concurrent.futures
import re

data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}
def get_tunnel(device):
    '''
    This function gets the Tunnel interface numbers and returns a list of used intf_numbers
    '''
    with netmiko.ConnectHandler(**device) as ssh:
        tunn_intf=re.findall(r'Tunnel(\d+)',ssh.send_command('show ip interface brief | include Tunnel'))
        return tunn_intf

def config_tunnel(device,template,data):
    '''
    Configures tunnel with given parameters (rendered template)
    Returns string with configuration
    '''
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        result=ssh.send_config_from_file(template.render(data))
        return result

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    '''
    This function configures an empty tunnel interface with information taken from jinja template
    and returns nothing.
    '''
    tunn_numbers=set()
    default_tunn=0
    env=jinja2.Environment(loader=jinja2.FileSystemLoader(src_template.split('/')[0]))
    template_file1=env.get_template(src_template.split('/')[1])
    template_file2=env.get_template(dst_template.split('/')[1])
    devices_list=[src_device_params,dst_device_params]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        tunnel_interfaces=executor.map(get_tunnel, devices_list)       # sendind command to search which tunnel interfaces in free    
    for output in tunnel_interfaces:                            # set of unique tunnel numbers, need to find free one
        tunn_numbers.add(output)                                # adds a result to set
    while True:                                                 # finding empty tunnel interface
        if default_tunn in tunn_numbers:                        # if item in set, then increment free tunnel number, repeat until we'll find number which is not in set
            default_tunn+=1
        else: break
    data['tun_num']=default_tunn        # setting same tunnel number, which is free
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        #TODO: check if the fuction below will work
        result=executor.map(config_tunnel, devices_list, [template_file1,template_file2], repeat(vpn_data_dict))    # vpn_data_dict I'm not sure it will work (Probably it does.)
    for item in result:
        pprint(item)

if __name__=="__main__":
    src_device={'device_type': 'cisco_ios', 'ip': '10.198.20.197', 'username': 'cisco', 'password': '123', 'secret': 'cisco'}
    dst_device={'device_type': 'cisco_ios', 'ip': '10.198.20.194', 'username': 'cisco', 'password': '123', 'secret': 'cisco'}
    template_file1=argv[1]
    template_file2=argv[2]
    configure_vpn(src_device, dst_device, template_file1, template_file2, data)