# Stores Type Data

from src.singleton.debug import Debug
from src.virtual.helpers import get_available_address, print_stats, init_types, Layers
from src.virtual.types import ValueType, DEFAULT_TYPES, MemoryType


class Scheduler:
    def __init__(self, type_resources: [MemoryType] = DEFAULT_TYPES):
        self.__segments = init_types(type_resources)
        self.debug_t = 0

    # Compilation
    def schedule_address(self, value_type: ValueType, layer: Layers):
        segment = self.__segments[layer.value]
        resource = segment.resources[value_type.value]

        new_address, error = get_available_address(resource)
        if error:
            print("could not assign new address for specified range")
            return None, True

        if layer == layer.TEMPORARY:
            debug = Debug.get_instance().get_map()
            if debug.get(new_address) is None:
                debug[new_address] = "T" + str(self.debug_t)
                self.debug_t += 1

        return new_address, False

    def get_segment(self, address):
        for key in self.__segments:
            segment = self.__segments[key]
            if segment.start <= address <= segment.end:
                return segment

    def is_segment(self, address, type_: Layers):
        segment = self.get_segment(address)
        return segment.type_ == type_

    def get_resource(self, address, segment):
        resources = segment.resources
        for key in resources:
            resource = resources[key]
            if resource.start <= address <= resource.end:
                return resource

    def release_address(self, address):
        segment = self.get_segment(address)
        resource = self.get_resource(address, segment)
        resource.free_addresses_list.put(address)

    def stats(self):
        for resource in self.__type_resources:
            print_stats(resource)
