# Stores Type Data
from src.compiler.allocator.helpers import get_available_address, print_stats, init_types, Layers
from src.compiler.allocator.types import ValueType, DEFAULT_TYPES, MemoryType, TypeResource
from src.compiler.errors import CompilerError, CompilerEvent
from src.utils.debug import Debug
from src.utils.observer import Publisher, Event


class Allocator(Publisher):
    def __init__(self, type_resources: [MemoryType] = DEFAULT_TYPES):
        super().__init__()
        self.__segments = init_types(type_resources)

    # Compilation
    def allocate_address(self, value_type: ValueType, layer: Layers):
        segment = self.__segments[layer.value]
        resource: TypeResource = segment.resources[value_type.value]
        # Refactor method get_available_address
        new_address, error = get_available_address(resource)

        if error:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Too many variables")))

        if layer == layer.TEMPORARY:
            debug = Debug.map()
            if debug.get(new_address) is None:
                temp_type = f'{resource.type.value[0].lower()}'
                temp_address = str(new_address - resource.start)
                debug[new_address] = f'T{temp_address} ({temp_type})'

        return new_address

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
