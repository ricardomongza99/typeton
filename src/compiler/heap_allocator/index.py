from functools import cmp_to_key


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


class HeapAllocator:
    def __init__(self, size):
        self.size = size
        self.ranges = [FreeRange(0, size - 1)]
        self.end_map = {}

    def allocate_reference(self, size):
        """Take the biggest range possible, break it up if needed"""
        if len(self.ranges) == 0:
            return print('out of mem')
        largest_free_block = self.ranges[0].size
        if size > largest_free_block:
            print("out of memory")
            return

        free_block = self.ranges.pop()
        if size == largest_free_block:
            print("all memory used")
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
        """Adds range to be able to use it again"""
        self.ranges.append(FreeRange(reference, self.end_map[reference]))
        self._merge_intervals()
