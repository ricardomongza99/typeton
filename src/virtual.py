from queue import Queue
from enum import Enum


class ValueType(Enum):
    INT = "int"
    STRING = "string"
    FLOAT = "float"
    BOOL = "bool"


class TypeData:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.pointer = start


class Memory:
    def __init__(self):
        self.__int_data = TypeData(0, 10)
        self.__float_data = TypeData(11, 15)
        self.__string_data = TypeData(16, 25)

        self.memory = {}

        self.__free_string_addrs = Queue(maxsize=self.__int_data.end-self.__int_data.start)
        self.__free_int_addrs = Queue(maxsize=self.__float_data.end-self.__float_data.start)
        self.__free_float_addrs = Queue(maxsize=self.__string_data.end-self.__float_data.start)

    @staticmethod
    def get_address(queue: Queue, data: TypeData):
        if queue.empty():
            if data.pointer <= data.end:
                addr = data.pointer
                data.pointer += 1
                return addr, False
            else:
                return None, True

        if queue.qsize() == data.end - data.start: #free memory
            queue = []
            data.pointer = data.start
            res = data.pointer
            data.pointer += 1
            return res, False

        return queue.get(), False

    def retrieve_value(self, addr):
        value = self.memory[addr]

        if value is None:
            return None, True
        return value, False

    def stats(self):
        single_stats("int",self.__int_data, self.__free_int_addrs)
        single_stats("float",self.__float_data, self.__free_float_addrs)
        single_stats("string",self.__string_data, self.__free_string_addrs)

    def assign_address(self, type: ValueType, value):
        q = None
        d = None
        if type == ValueType.INT:
            q = self.__free_int_addrs
            d = self.__int_data
        elif type == ValueType.FLOAT:
            q = self.__free_float_addrs
            d = self.__float_data
        else:
            d = self.__string_data
            q = self.__free_string_addrs

        addr, err = self.get_address(q, d)
        if err:
            print("Too many variables")
            return None, True

        self.memory[addr] = value
        return addr, False

    def release_address(self, addr):
        if self.__int_data.start <= addr <= self.__int_data.end:
            self.__free_int_addrs.put(addr)
        elif self.__float_data.start <= addr <= self.__float_data.end:
            self.__free_float_addrs.put(addr)
        elif self.__string_data.start <= addr <= self.__string_data.end:
            self.__free_string_addrs.put(addr)
        else:
            print("Invalid addr")


def single_stats(type, data: TypeData, q: Queue):

    cap = (data.end - data.start)
    use = (data.pointer - data.start) - q.qsize()
    per = (use / cap) * 100
    print("-----------------------")
    print("Stats for" ,type)
    print("Capacity: ", cap)
    print("Current Use:", use, "(", per, "%)")
    print("Freed Addresses", q.qsize())

def run_tests():
    mem = Memory()

    addrs = []

    for x in range(12):
        addr, err = mem.assign_address(ValueType.INT, x*10)
        if err:
            break
        print(addr)
        addrs.append(addr)

    mem.release_address(addrs[1])
    mem.release_address(addrs[2])
    mem.release_address(addrs[3])

    mem.stats()

    print("retreiving")

    for x in range(11):
        value, err = mem.retrieve_value(addrs[x])
        if err:
            break
        print(value)


