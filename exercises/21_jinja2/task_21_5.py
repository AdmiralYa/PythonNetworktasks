# -*- coding: utf-8 -*-
'''
Задание 21.5

Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.


Создать функцию create_vpn_config, которая использует эти шаблоны для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациямя (строки), которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
'''
from sys import argv
import jinja2
from pprint import pprint
data = {
        'tun_num': 17,
        'wan_ip_1': '80.241.1.1',
        'wan_ip_2': '90.18.10.2',
        'tun_ip_1': '10.255.1.1 255.255.255.252',
        'tun_ip_2': '10.255.1.2 255.255.255.252'
}

def create_vpn_config(template1, template2, data_dict):
    env=jinja2.Environment(loader=jinja2.FileSystemLoader(template1.split('/')[0]))
    template_file1=env.get_template(template1.split('/')[1])
    template_file2=env.get_template(template2.split('/')[1])
    return (template_file1.render(data_dict),template_file2.render(data_dict))

if __name__=="__main__":
  template_file1=argv[1]
  template_file2=argv[2]
  pprint(create_vpn_config(template_file1,template_file2,data))