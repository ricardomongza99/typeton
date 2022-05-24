# Static Helpers
from enum import Enum

from src.compiler.allocator.types import TypeResource, MemoryType, TypeRange


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
            return None, True

    # if all addressed were freed, reset pointer and empty queue
    if resource.free_addresses_list.qsize() == resource.end - resource.start:
        resource.free_addresses_list = []
        resource.pointer = resource.start
        initial_point = resource.pointer
        resource.pointer += 1
        return initial_point, False

    return resource.free_addresses_list.get(), False


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


def get_segment(address, segments):
    for key in segments:
        segment = segments[key]
        if segment.start <= address <= segment.end:
            return segment


def is_segment(address, segments, type_: Layers):
    segment = get_segment(segments, address)
    return segment.type_ == type_


def get_resource(address, segment):
    resources = segment.resources
    for key in resources:
        resource = resources[key]
        if resource.start <= address <= resource.end:
            return resource


def init_types(memory_types: [MemoryType], is_runtime: bool):
    """Initializes segment types for each type"""
    segments = {}
    current_start = 0

    for layer in Layers:
        segment = Segment(type_=layer)
        for memory_type in memory_types:
            new_end = current_start + memory_type.size
            # Only take what we need
            if is_runtime:
                resource = TypeRange(current_start, new_end, memory_type.type)
            else:
                resource = TypeResource(current_start, new_end, memory_type.type)

            segment.resources[memory_type.type.value] = resource
            current_start = new_end + 1
        segment.end = current_start - 1
        segments[layer.value] = segment

    return segments
