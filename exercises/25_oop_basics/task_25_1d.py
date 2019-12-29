# -*- coding: utf-8 -*-

'''
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует
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
    def add_link(self,side1,side2):
        if ((side1,side2) or (side2,side1)) in self.topology.items():
            print("Такое соединение существует")
        elif side1 in (self.topology.keys() or self.topology.values()) or side2 in (self.topology.keys() or self.topology.values()):
            print("Cоединение с одним из портов существует")
        else: self.topology.update({side1:side2})

if __name__=="__main__":
    top=Topology(topology_example)
    top.topology
    top.delete_node('SW1')
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    print(top.topology)