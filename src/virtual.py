from queue import Queue


class TypeData:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.pointer = start


def get_address(queue: Queue, data: TypeData):
    if queue.empty():
        if data.pointer <= data.end:
            addr = data.pointer
            data.pointer += 1
            return addr, False
        else:
            return None, True

    return queue.get(), False


class Memory:
    def __init__(self):
        self.__int_data = TypeData(0, 800)
        self.__float_data = TypeData(801, 1500)
        self.__string_data = TypeData(1501, 2000)

        self.memory = {}

        self.__free_string_addrs = Queue(maxsize=100)
        self.__free_int_addrs = Queue(maxsize=100)
        self.__free_float_addrs = Queue(maxsize=100)

    def retrieve_value(self, addr):
        value = self.memory[addr]

        if value is None:
            return None, True
        return value, False

    def assign_address(self, type, value):
        q = None
        if type == "Int":
            q = self.__free_int_addrs
        elif type == "Float":
            q = self.__free_float_addrs
        else:
            q = self.__free_string_addrs

        addr, err = get_address(q)
        if err:
            print("Too many variables")
            return True

        self.memory[addr] = value
        return False

    def release_address(self, addr):
        if self.__int_data.start <= addr <= self.__int_data.end:
            self.__free_int_addrs.get(addr)
        elif self.__float_data.start <= addr <= self.__float_data.end:
            self.__free_float_addrs.get(addr)
        elif self.__string_data.start <= addr <= self.__string_data.end:
            self.__free_string_addrs.get(addr)
        else:
            print("Invalid addr")
