from create_db import create_db as new_db, check_if_db_exists
import sqlite3
from add_data import parse_yml_file, parse_dhcp_snoop_file
from datetime import datetime,timedelta

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

def create_db(db_name,scheme_name):
    """
    reference to original create_db.py func
    """
    new_db(db_name,scheme_name)

def add_data_switches(db_file, filename):
    """
    adding data to switch table
    parsing args from list to strings
    """
    if check_if_db_exists(db_file):
        print('Добавляю данные в таблицу switches...')
        connection=sqlite3.connect(db_file)             # connecting to database
        for yml_name in filename:
            for item in parse_yml_file(yml_name):        # going through all tuples in .yml file
                try:
                    with connection:
                        query_switch_table='insert into switches (hostname, location) values (?,?)'
                        connection.execute(query_switch_table,item)     # execute query
                except sqlite3.IntegrityError as err:
                    print('Возникла ошибка: ', err)
    else: print('База данных не существует. Перед добавлением данных, ее надо создать')

def add_data(db_file, filename):
    """
    same as add_data.py, just parsing list into strings
    """
    connection=sqlite3.connect(db_file)
    query_dhcp_table="insert into dhcp (mac, ip, vlan, interface, switch, active, last_active) values (?,?,?,?,?,1,datetime('now'))"
    query_active_false='update dhcp set active=0'
    query_replace_true="replace into dhcp values (?,?,?,?,?,1,datetime('now'))"
    query_delete_old_record="delete from dhcp where last_active < ?"
    with connection:
        connection.execute(query_active_false)
        for snooping_file in filename:
            for item in parse_dhcp_snoop_file(snooping_file): # iterating through list of variables received from parse_dhcp_snoop_file
                try:
                    with connection:
                        connection.execute(query_dhcp_table, item)
                except sqlite3.IntegrityError as err:       # if mac already exists, replace the record
                    with connection:
                        connection.execute(query_replace_true,item)
        with connection:
            connection.execute(query_delete_old_record,(week_ago,))

def get_data(db_file, key, value):
    """
    same as get_data.py
    """
    connection=sqlite3.connect(db_file)
    query_active_with_args='select * from dhcp where {}=? and active=1'.format(key)
    query_inactive_with_args='select * from dhcp where {}=? and active=0'.format(key)
    result_active=connection.execute(query_active_with_args,(value,))
    result_inactive=connection.execute(query_inactive_with_args,(value,))
    print("Активные записи:\n"+"-"*40)
    for row in result_active:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("")
    print("-"*40)
    print("Неактивные записи:")
    for row in result_inactive:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("\n"+"-"*40,end='')

def get_all_data(db_file):
    """
    same as get_data.py
    """
    connection=sqlite3.connect(db_file)
    query_get_active='select * from dhcp where active=1'
    query_get_inactive='select * from dhcp where active=0'
    result_active=connection.execute(query_get_active)
    result_inactive=connection.execute(query_get_inactive)
    print("Активные записи:\n"+"-"*40)
    for row in result_active:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("")
    print("-"*40)
    print("Неактивные записи:")
    for row in result_inactive:
        for item in row:
            print("{:<16}  ".format(item),end='')
        print("\n"+"-"*40,end='')