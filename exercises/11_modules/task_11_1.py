# -*- coding: utf-8 -*-
'''
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое файла в строку.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

В словаре интерфейсы должны быть записаны без пробела между типом и именем. То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def parse_cdp_neighbors(command_output):
    '''
    На вход подается строка, преобразуем ее в список, содержащий только строки с cdp инфой
    Делаем списки внутри списка через .split(), бегаем по каждому списку, берем 1,2,3 и 2 последних элемента
    Обьединяем 2,3 и 2 последних в строку и создаем словарь из кортежей
    '''
    command_list=[line for line in command_output.split('\n') if line and (line.startswith('R') or line.startswith('SW'))] #делим строку по \n, оставляем только те строки, которые начинаются с R или SW
    local_device_name=command_output.strip().split('\n')[0].split('>')[0]
    return_dict={}
    nested_list=[[line for line in line.split()] for line in command_list[1:]] #обрабатываем все элементы списка, кроме первого, т.к. там SW/R>sh cdp nei
    #print(nested_list)
    for remote_device, local_intf_name,local_intf_number, *other, remote_intf_name, remote_intf_number in nested_list:
        local_intf=''.join('{}{}'.format(local_intf_name,local_intf_number)) #создаем строку локального интерфейса
        remote_intf=''.join('{}{}'.format(remote_intf_name,remote_intf_number)) #remote intf
        return_dict[(local_device_name,local_intf)]=(remote_device,remote_intf) #создаем словарь, ключ-значение --- кортежи
    return return_dict
    
if __name__ == "__main__":
    file=open('sh_cdp_n_sw1.txt','r')
    line=file.read()
    file.close()
    sh_cdp_n_sw1 = (
        'SW1>show cdp neighbors\n\n'
        'Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge\n'
        '                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone\n\n'
        'Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID\n'
        'R1           Eth 0/1         122           R S I           2811       Eth 0/0\n'
        'R2           Eth 0/2         143           R S I           2811       Eth 0/0\n'
        'R3           Eth 0/3         151           R S I           2811       Eth 0/0\n'
        'R6           Eth 0/5         121           R S I           2811       Eth 0/1')
    result=parse_cdp_neighbors(line)
    print(result)