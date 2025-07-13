from typing import List, Tuple, Callable
import math
import operator

def parent(i: int) -> int:
        return (i - 1) // 2
    
def leftChild(i: int) -> int:
    return (2 * i) + 1

def rightChild(i: int) -> int: 
    return (2 * i) + 2

class Node:
    def __init__(self, priority: float, data: Tuple[int]):
        self.priority = priority
        self.data = data
    
    def __lt__(self, other): 
        return self.priority < other.priority

    def __gt__(self, other): 
        return self.priority > other.priority
    
    def __le__(self, other): 
        return self.priority <= other.priority

    def __ge__(self, other): 
        return self.priority >= other.priority

    def __str__(self):
        return str(self.data) + ": " + str(round(self.priority, 2))

class MaxMinHeap:
    last2 = [(0, 0), (0, 0)]

    def __init__(self, array: List[Node], last2: List[Tuple[int, int]] = [(0, 0), (0, 0)]):
        self.array = sorted([i for i in array])
        self.size = len(array)
        MaxMinHeap.last2 = last2

    def __getitem__(self, index: int) -> Node:
        return self.array[index]

    def __setitem__(self, index: int, node: Node):
        self.array[index] = node

    def __contains__(self, i: int) -> bool:
        return i < self.size and i >= 0

    def __str__(self):
        return str([str(i) for i in self.array])

    def insert(self, new: Node):
        MaxMinHeap.last2.pop(0)
        MaxMinHeap.last2.append(new.data)
        
        print(self)
        for i in range(self.size):
            if new < self[i]:
                self.array.insert(i, new)
                break
        if len(self.array) == self.size:
            self.array.append(new)
        print(self)
        self.size += 1

    def remove(self, i: int) -> Node:
        if i >= self.size:
            raise IndexError("Index out of bounds")

        self.size -= 1

        return self.array.pop(i)

    def peekMax(self) -> Node:
        if len(self.array) == 0:
            raise LookupError("Heap is empty")
        return self.array[self.size-1]

    def peekMin(self) -> Node:
        if len(self.array) == 0:
            raise LookupError("Heap is empty")
        return self.array[0]

    def peekSecondMax(self) -> Node:
        if len(self.array) == 0:
            raise LookupError("Heap is empty")
        return self.array[self.size-2]

    def extractMax(self) -> Node:
        return self.remove(self.size-1)

    def extractMin(self) -> Node:
        return self.remove(0)

    def extract(self) -> Node:
        if self.peekMax().data not in MaxMinHeap.last2:
            return self.extractMax()
        elif self.size > 1 and self.peekSecondMax().data not in MaxMinHeap.last2:
            return self.remove(self.size-2)
        else:
            return self.remove(self.size-3)
