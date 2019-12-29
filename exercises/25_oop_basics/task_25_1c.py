# -*- coding: utf-8 -*-

'''
Задание 25.1c

Изменить класс Topology из задания 25.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

'''

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    def _normalize(self,topology_dict):
        empty_topo={}
        for key,value in topology_dict.items():
            if topology_dict[key] not in empty_topo.keys():
                empty_topo[key]=value
        return empty_topo

    def delete_link(self,key,value):
        if key in self.topology.keys():
            del self.topology[key]
        elif value in self.topology.keys():
            del self.topology[value]
        else: print ("Такого соединения нет")

    def delete_node(self,node):
        delete=[key for key in self.topology if node in self.topology[key]]
        if node in self.topology.keys() or len(delete)!=0:      # idk why statement --> node in self.topology.values() doesn't working, so I used var delete 
            while node in self.topology.keys():                 # which represent the number of keys with desired node value
                del self.topology[node]
            for key in delete:
                del self.topology[key]
        else: print("Такого устройства нет")

if __name__=="__main__":
    top=Topology(topology_example)
    top.topology
    top.delete_node('SW1')
    print(top.topology)