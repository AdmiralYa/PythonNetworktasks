import pytest
import task_27_2
from netmiko.cisco.cisco_ios import CiscoIosBase
import sys
sys.path.append('..')

from common_functions import check_class_exists, check_attr_or_method


def test_class_created():
    check_class_exists(task_27_2, 'MyNetmiko')


def test_class_inheritance(first_router_from_devices_yaml):
    r1 = task_27_2.MyNetmiko(**first_router_from_devices_yaml)
    assert isinstance(r1, CiscoIosBase), "Класс MyNetmiko должен наследовать CiscoIosBase"
    check_attr_or_method(r1, attr='send_command')
    check_attr_or_method(r1, attr='send_config_set')
    r1.disconnect()