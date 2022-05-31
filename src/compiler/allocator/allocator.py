# Stores Type Data
from src.compiler.allocator.helpers import get_available_address, init_types, Layers, get_resource, get_segment
from src.compiler.allocator.types import ValueType, DEFAULT_TYPES, MemoryType, TypeResource
from src.compiler.errors import CompilerError, CompilerEvent
from src.utils.debug import Debug
from src.utils.observer import Publisher, Event, Subscriber


class Allocator(Publisher, Subscriber):
    def __init__(self, type_resources: [MemoryType] = DEFAULT_TYPES):
        super().__init__()
        self.__segments = init_types(type_resources, is_runtime=False)

    def handle_event(self, event: Event):
        if event.type_ is CompilerEvent.RELEASE_MEM_IF_POSSIBLE:
            self._release_memory_if_possible(event.payload)
        elif event.type_ is CompilerEvent.FREE_MEMORY:
            self.release_address_list(event.payload)

    def _release_memory_if_possible(self, address_list):
        for address in address_list:
            if self.is_segment(address, Layers.TEMPORARY):
                self.release_address(address)

    def release_address_list(self, delete_list):
        for address in delete_list:
            self.release_address(address)

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
                temp_type = f'{resource.type_.value[0].lower()}'
                temp_address = str(new_address - resource.start)
                debug[new_address] = f'T{temp_address} ({temp_type})'

        return new_address

    def allocate_space(self, value_type: ValueType, layer: Layers, size):
        """ Allocates `size` spaces of memory. Used for arrays """
        segment = self.__segments[layer.value]
        resource: TypeResource = segment.resources[value_type.value]

        if resource.end < resource.pointer + (size - 1):
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Too many variables")))

        resource.pointer += (size - 1)

    def get_segment(self, address):

        return get_segment(address, self.__segments)

    def is_segment(self, address, type_: Layers):
        segment = self.get_segment(address)
        return segment.type_ == type_

    def release_address(self, address):
        if address is None:
            return
        segment = self.get_segment(address)
        resource = get_resource(address, segment)
        resource.free_addresses_list.put(address)
