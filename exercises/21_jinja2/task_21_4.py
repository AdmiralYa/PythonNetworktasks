# -*- coding: utf-8 -*-
'''
Задание 21.4

Создайте шаблон templates/add_vlan_to_switch.txt, который будет использоваться
при необходимости добавить VLAN на коммутатор.

В шаблоне должны поддерживаться возможности:
* добавления VLAN и имени VLAN
* добавления VLAN как access, на указанном интерфейсе
* добавления VLAN в список разрешенных, на указанные транки

Если VLAN необходимо добавить как access, надо настроить и режим интерфейса и добавить его в VLAN:
interface Gi0/1
 switchport mode access
 switchport access vlan 5

Для транков, необходимо только добавить VLAN в список разрешенных:
interface Gi0/10
 switchport trunk allowed vlan add 5

Имена переменных надо выбрать на основании примера данных,
в файле data_files/add_vlan_to_switch.yaml.


Проверьте шаблон templates/add_vlan_to_switch.txt на данных в файле data_files/add_vlan_to_switch.yaml, с помощью функции generate_config из задания 21.1.
Не копируйте код функции generate_config.

'''
from task_21_1 import generate_config
from pprint import pprint
import yaml
from sys import argv

if __name__=="__main__":
  with open("data_files/add_vlan_to_switch.yaml") as yamlfile:
      data_dict=yaml.safe_load(yamlfile)
  template_file=argv[1]
  print(generate_config(template_file,data_dict))
