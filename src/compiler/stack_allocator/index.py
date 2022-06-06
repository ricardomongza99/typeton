# Stores Type Data
from typing import List
from src.compiler.stack_allocator.helpers import get_available_address, init_types, Layers, get_resource, get_segment
from src.compiler.stack_allocator.types import ValueType, DEFAULT_TYPES, MemoryType, TypeResource
from src.compiler.errors import CompilerError, CompilerEvent
from src.utils.debug import Debug
from src.utils.observer import Publisher, Event, Subscriber


class StackAllocator(Publisher, Subscriber):
    def __init__(self, type_resources: List[MemoryType] = DEFAULT_TYPES):
        super().__init__()
        self._segments = init_types(type_resources, is_runtime=False)

    def handle_event(self, event: Event):
        if event.type_ is CompilerEvent.RELEASE_MEM_IF_POSSIBLE:
            self._release_memory_if_possible(event.payload)
        elif event.type_ is CompilerEvent.FREE_MEMORY:
            self.release_local_addresses()

    def _release_memory_if_possible(self, address_list):
        for address in address_list:
            if self.is_segment(address, Layers.TEMPORARY):
                self.release_address(address)

    def release_local_addresses(self):
        self._segments[Layers.LOCAL.value].reset()
        self._segments[Layers.TEMPORARY.value].reset()

    # Compilation

    def allocate_address(self, value_type: ValueType, layer: Layers):
        print("Allocating address", value_type, layer)
        segment = self._segments[layer.value]
        resource: TypeResource = segment.resources[value_type.value]
        # Refactor method get_available_address
        new_address, error = get_available_address(resource)

        if error:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE,
                           CompilerError("Too many variables")))

        if layer == layer.TEMPORARY:
            debug = Debug.map()
            if debug.get(new_address) is None:
                temp_type = f'{resource.type_.value[0].lower()}'
                temp_address = str(new_address - resource.start)
                debug[new_address] = f'T{temp_address} ({temp_type})'

        return new_address

    def allocate_space(self, value_type: ValueType, layer: Layers, size):
        """ Allocates `size` spaces of memory. Used for arrays """
        segment = self._segments[layer.value]
        resource: TypeResource = segment.resources[value_type.value]

        if resource.end < resource.pointer + (size - 1):
            self.broadcast(Event(CompilerEvent.STOP_COMPILE,
                           CompilerError("Too many variables")))

        for i in range(size):
            self.broadcast(Event(0, resource.pointer))
            resource.pointer += 1

    def get_segment(self, address):

        return get_segment(address, self._segments)

    def is_segment(self, address, type_: Layers):
        segment = self.get_segment(address)
        return segment.type_ == type_

    def release_address(self, address):
        if address is None:
            return
        segment = self.get_segment(address)
        resource = get_resource(address, segment)
        resource.pointer = resource.start
        resource.free_addresses_list.put(address)
