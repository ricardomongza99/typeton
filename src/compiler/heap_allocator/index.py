import heapq


class HeapRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.size < other.val

    @property
    def size(self):
        return self.end - self.start


class MaxRangeHeap:
    """Get the largest slot of available space in the memory heap"""

    def __init__(self, size):
        self.heap = []
        heapq.heapify(self.heap)
        self.push_range(HeapRange(0, size - 1))

    def pop(self):
        """get value from tuple"""
        return heapq.heappop(self.heap)[1]

    @property
    def largest(self):
        """get value from tuple"""
        return self.heap[0][1]

    def push_range(self, heap_range: HeapRange):
        """* -1 to make it a max heap (max at the top)"""
        heapq.heappush(self.heap, (heap_range.size * -1, heap_range))


# 0 4
# 0 10

# 0 - 4 (5), (5 - 9) 5

class HeapAllocator:
    def __init__(self, size):
        self.size = size
        self.heap = MaxRangeHeap(size)
        self.used = 0
        self.range_end = {}

    def available(self):
        return self.size - self.used

    def allocate_reference(self, size):
        if self.available() == 0:
            return None
        largest_free_block = self.heap.largest.size
        if size > largest_free_block:
            print("out of memory")
            return

        free_block = self.heap.pop()
        if size == largest_free_block:
            return free_block.start

        reference = free_block.start
        new_start = free_block.start + size
        free_block.start = new_start

        self.range_end[reference] = new_start - 1

        self.heap.push_range(free_block)
        self.used += size
        return reference

    def display(self):
        for size, range in self.heap.heap:
            print("Free Ranges")

    def free_reference(self, reference):
        """Adds range to be able to usable again"""
        self.heap.push_range(HeapRange(reference, self.range_end[reference]))
        self.used -= (self.range_end[reference] - reference) + 1
