# Testing
from src.virtual.memory import Memory
from src.virtual.scheduler import Scheduler
from src.virtual.types import ValueType


def run_tests():
    memory_instance = Memory()
    memory_scheduler = Scheduler()
    address_list = []

    for x in range(12):
        memory_scheduler.schedule_address(value_type=ValueType.INT)
        memory_instance.assign_address(x, x * 10)
        address_list.append(x)

    memory_scheduler.release_addresses([6,7,8])
    memory_instance.release_addresses([6,7,8])

    memory_scheduler.stats()

