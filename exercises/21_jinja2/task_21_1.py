# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''
import yaml
import jinja2
from sys import argv
from pprint import pprint
def generate_config(template,data_dict):
    env=jinja2.Environment(loader=jinja2.FileSystemLoader(template.split('/')[0]))
    template=env.get_template(template.split('/')[1])
    return template.render(data_dict)

if __name__=="__main__":
    with open("data_files/for.yml") as yamlfile:
        data_dict=yaml.safe_load(yamlfile)
    template_file=argv[1]
    pprint(generate_config(template_file,data_dict))