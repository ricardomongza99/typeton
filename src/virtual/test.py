# Testing
from src.virtual.runtime import Memory
from src.virtual.compilation import Scheduler
from src.virtual.types import ValueType


def run_tests():
    memory_instance = Memory()
    memory_scheduler = Scheduler()
    address_list = []

    for x in range(12):
        memory_scheduler.schedule_address(value_type=ValueType.INT)
        memory_instance.assign_address(x, x * 10)
        address_list.append(x)

    memory_scheduler.stats()
