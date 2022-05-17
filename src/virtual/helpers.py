# Static Helpers
from src.virtual.types import TypeResource, MemoryType
from enum import Enum


def is_between_range(start: int, value: int, end: int):
    if start <= value <= end:
        return True
    return False


def get_available_address(resource: TypeResource):
    if resource.free_addresses_list.empty():
        if resource.pointer <= resource.end:
            address = resource.pointer
            resource.pointer += 1
            return address, False
        else:
            return None, True

    if resource.free_addresses_list.qsize() == resource.end - resource.start:  # free memory
        resource.free_addresses_list = []
        resource.pointer = resource.start
        initial_point = resource.pointer
        resource.pointer += 1
        return initial_point, False

    return resource.free_addresses_list.get(), False


def print_stats(resource: TypeResource):
    cap = (resource.end - resource.start)
    use = (resource.pointer - resource.start) - resource.free_addresses_list.qsize()
    per = (use / cap) * 100
    print("-----------------------")
    print("Stats for", resource.type)
    print("Capacity: ", cap)
    print("Current Use:", use, "(", per, "%)")
    print("Freed Addresses", resource.free_addresses_list.qsize())


class Layers(Enum):
    GLOBAL = 0
    LOCAL = 1
    TEMPORARY = 2
    CONSTANT = 3


class Segment:
    def __init__(self, type_: Layers, resources: [TypeResource], start, end):
        self.type_ = type_
        self.start = start
        self.end = end
        self.resources = resources


def init_types(memory_types: [MemoryType]):
    segments = {}
    current_start = 0

    for layer in Layers:
        segment = Segment(type_=layer, start=current_start, resources={},end=0)
        for simple in memory_types:
            new_end = current_start + simple.size
            segment.resources[simple.type.value] = TypeResource(start=current_start, end=new_end, resource_type=simple.type)
            current_start = new_end + 1
        segment.end = current_start-1
        segments[layer.value] = segment

    return segments
