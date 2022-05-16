# Memory is just a simple hash table to simulate actual memory during runtime
class Memory:
    def __init__(self):
        self.__storage = {}

    # Runtime
    def assign_address(self, address, value):
        self.__storage[address] = value

    def release_address(self, address):
        del self.__storage[address]

    def release_addresses(self, address_list: [int]):
        for address in address_list:
            del self.__storage[address]

    def retrieve_value(self, address):
        value = self.__storage[address]

        if value is None:
            return None, True
        return value, False

