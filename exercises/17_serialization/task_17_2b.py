# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''
from draw_network_graph import draw_topology
import yaml
from pprint import pprint

def transform_topology(yaml_filename):
    with open(yaml_filename) as file:
        read_dict=yaml.safe_load(file)
        result_dict={}
        fin_dict={}
        iter=0
        for key,value in read_dict.items():
            for k,v in value.items():
                first_val,sec_val=list(v.items())[0][0],list(v.items())[0][1]   ###### TODO: change this to normal style. using this to unpack values to make it a 1-elem tuple
                result_dict[(key,str(k))]=(first_val,sec_val)
        while len(result_dict)>7:   # assuming that all values are duplicated. Iterating through dict until it length become 14/2=7, and if the value of dict in keys,that delete key
            if result_dict[list(result_dict.keys())[iter]] in result_dict.keys(): ##### TODO: change this to normal style. Very bad code
                del result_dict[list(result_dict.keys())[iter]]
            else: iter+=1   # if the value is unique, than iterate through items by 1
        draw_topology(result_dict)
        return result_dict

if __name__=="__main__":
    transform_topology('topology.yaml')