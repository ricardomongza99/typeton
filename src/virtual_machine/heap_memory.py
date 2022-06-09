from enum import Enum
from functools import cmp_to_key
from re import S

from src.config.definitions import HEAP_RANGE_SIZE
from src.utils.observer import Event, Publisher


class RuntimeActions(Enum):
    STOP_RUNTIME = 'stop_runtime'


class FreeRange:
    """Represents a continuous amount of available memory in the heap"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def size(self):
        return (self.end - self.start) + 1

    def __str__(self):
        return f'({self.start}, {self.end})'

    def __lt__(self, other):
        return self.size > other.size


def compare(a, b):
    return a.start - b.start or a.end - b.end


class Heap(Publisher):
    def __init__(self, range_start):
        super().__init__()
        self.size = HEAP_RANGE_SIZE
        self.start = range_start
        self.ranges = [FreeRange(range_start, range_start + self.size - 1)]
        self.end_map = {}
        self.end = range_start + self.size - 1
        self.memory = [None] * self.size

    def get_value(self, heap_address):
        value = self.memory[heap_address - self.start]

        # print('Heap', heap_address, 'value', value)

        if value is None:
            self.broadcast(Event(RuntimeActions.STOP_RUNTIME, 'NULL Pointer Exception: Trying to get value from uninitialized address'))

        return value

    def set_value(self, heap_address, value):
        if len(self.memory) <= heap_address - self.start:
            self.broadcast(Event(RuntimeActions.STOP_RUNTIME, 'Value does not exist'))
        self.memory[heap_address - self.start] = value

    def is_heap_address(self, address):
        return self.start <= address <= self.end

    def release_heap_memory(self, heap_address, level=0):
        """Release the heap memory at the given address"""
        end = self.end_map[heap_address] - self.start
        start = heap_address - self.start

        curr = start
        while (curr <= end):
            value = self.memory[curr]
            if type(value) is int and self.is_heap_address(value):
                # print('found object at level', level)
                self.release_heap_memory(value, level+1)
            elif value is not None:
                # print('freeing', value)
                self.memory[curr] = None
            curr += 1

        self.free_reference(heap_address)

    def allocate_reference(self, size):
        """Take the biggest range possible, break it up if needed"""
        if len(self.ranges) == 0:
            self.broadcast(Event(RuntimeActions.STOP_RUNTIME, 'Out of heap memory'))
            return
        largest_free_block = self.ranges[0].size
        if size > largest_free_block:
            self.broadcast(Event(RuntimeActions.STOP_RUNTIME, 'Not enough heap memory to allocate reference'))
            return

        free_block = self.ranges.pop()
        if size == largest_free_block:
            return free_block.start

        reference = free_block.start
        new_start = free_block.start + size
        free_block.start = new_start

        self.ranges.append(free_block)
        self.end_map[reference] = new_start - 1
        # maintain references for instant access and range optimization
        return reference

    def display(self):
        print('----------------------------------------')
        for range_ in self.ranges:
            print(range_)

        if len(self.ranges) == 0:
            print("no spaces left")

        print('----------------------------------------')

    def _merge_intervals(self):
        """To prevent fragmentation, always merge continuous intervals if possible"""
        self.ranges.sort(key=cmp_to_key(compare))

        result = []

        last = None
        for range_ in self.ranges:
            if not last or range_.start > last.end + 1:
                last = range_
                result.append(last)
            elif range_.end > last.end:
                last.end = range_.end

        self.ranges = result

    def free_reference(self, reference):
        # print('freeing reference', reference)
        """Adds range to be able to use it again"""

        end = self.end_map[reference]
        self.ranges.append(FreeRange(reference, end))
        self._merge_intervals()
