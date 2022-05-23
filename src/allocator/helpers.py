# Static Helpers
from enum import Enum

from src.allocator.types import TypeResource, MemoryType


def is_between_range(start: int, value: int, end: int):
    if start <= value <= end:
        return True
    return False


# TODO move to type resource
def get_available_address(resource: TypeResource):
    # if no free addresses, use pointer
    if resource.free_addresses_list.empty():
        if resource.pointer <= resource.end:
            address = resource.pointer
            resource.pointer += 1
            return address, False
        else:
            raise SyntaxError("Hello world")
            return None, True

    # if all addressed were freed, reset pointer and empty queue
    if resource.free_addresses_list.qsize() == resource.end - resource.start:
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
    def __init__(self, type_: Layers):
        self.type_ = type_
        self.start = 0
        self.end = 0
        self.resources = {}


def init_types(memory_types: [MemoryType]):
    """Initializes segment types for each type"""
    segments = {}
    current_start = 0

    for layer in Layers:
        segment = Segment(type_=layer)
        for memory_type in memory_types:
            new_end = current_start + memory_type.size
            segment.resources[memory_type.type.value] = TypeResource(start=current_start,
                                                                     end=new_end, resource_type=memory_type.type)
            current_start = new_end + 1
        segment.end = current_start - 1
        segments[layer.value] = segment

    return segments
