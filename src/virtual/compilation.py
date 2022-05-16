# Stores Type Data
from src.virtual.helpers import get_available_address, is_between_range, print_stats, init_types
from src.virtual.types import ValueType, DEFAULT_TYPES, MemoryType


class Scheduler:
    def __init__(self, type_resources: [MemoryType] = DEFAULT_TYPES):
        self.__type_resources = init_types(type_resources)

    # Compilation
    def schedule_address(self, value_type: ValueType):
        resource, resource_error = self.__get_resource_from_type(value_type)
        if resource_error:
            print("invalid type")
            return None, True

        new_address, error = get_available_address(resource)
        if error:
            print("could not assign new address for specified range")
            return None, True

        return new_address, False

    def release_addresses(self, address_list):
        for address in address_list:
            self.release_address(address)

    def release_address(self, address):
        resource, error = self.__get_resource_from_address(address)
        if error:
            print("unable to release, address range not found for: ",address)
            return True

        resource.free_addresses_list.put(address)
        return False

    # -------Internal Helpers--------
    def __get_resource_from_type(self, value_type: ValueType):
        for resource in self.__type_resources:
            if resource.type == value_type:
                return resource, False

        return None, False

    def __get_resource_from_address(self, address):
        for resource in self.__type_resources:
            if is_between_range(resource.start, address, resource.end):
                return resource, False

        return None, True

    def stats(self):
        for resource in self.__type_resources:
            print_stats(resource)


