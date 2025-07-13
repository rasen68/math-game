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

class MaxHeap:
    last2 = [(0, 0), (0, 0)]

    def __init__(self, array: List[Node], last2: List[Tuple[int, int]] = [(0, 0), (0, 0)]):
        self.array = [i for i in array]
        self.size = len(array)
        MaxHeap.last2 = last2

        secondLastLayer = 2 ** (math.floor(math.log2(self.size))) - 2

        # heapify by downheaping 
        for i in range(secondLastLayer, -1, -1):
            self.downheap(i)
    
    def __getitem__(self, index: int) -> Node:
        return self.array[index]

    def __setitem__(self, index: int, node: Node):
        self.array[index] = node
    
    def __contains__(self, i: int) -> bool:
        return i < self.size and i >= 0

    def swap(self, i: int, j: int):
        self[j], self[i] = self[i], self[j]

    def upheap(self, i: int):
        p = parent(i)

        if p in self:
            pNode = self[p]
            iNode = self[i]
            if pNode < iNode:
                self.swap(p, i)
                self.upheap(p)
    
    def downheap(self, i: int):
        r = rightChild(i)
        l = leftChild(i)

        if l not in self:
            return

        # if r doesn't exist we only need to test for l
        if r not in self and self[l] > self[i]:
            self.swap(l, i)
            self.downheap(l)
        elif r in self:
            rNode = self[r]
            lNode = self[l]
            iNode = self[i]

            m = max(rNode, lNode, iNode)
            if m != iNode:
                s = r if m == rNode else l
                self.swap(s, i)
                self.downheap(s)
    
    def peekMax(self) -> Node:
        if len(self.array) == 0:
            raise LookupError
        return self.array[0]

    def peekSecondMax(self) -> Node:
        if len(self.array) <= 1:
            raise LookupError
        if len(self.array) == 2:
            return self.array[1]
        return max(self.array[1], self.array[2])

    def extract(self) -> Node:
        if self.peekMax().data not in MaxHeap.last2:
            return self.extractMax()
        elif self.peekSecondMax().data not in MaxHeap.last2:
            return self.extractSecondMax()
        else:
            return self.extractThirdMax()

    def extractMax(self) -> Node:
        self.swap(0, self.size - 1)
        self.size -= 1
        ret = self.array.pop(self.size)

        self.downheap(0)

        return ret
    
    def extractSecondMax(self) -> Node:
        i = 1 if (2 >= self.size or self[1] > self[2]) else 2
        
        self.swap(i, self.size - 1)
        self.size -= 1
        ret = self.array.pop(self.size)
        
        self.downheap(i)

        return ret

    def extractThirdMax(self) -> Node:
        secondMax = 1 if self[1] > self[2] else 2
        other = 2 if secondMax == 1 else 1
        l = leftChild(secondMax) if leftChild(secondMax) < self.size else other
        r = rightChild(secondMax) if rightChild(secondMax) < self.size else l
        m = max(self[l], self[r], self[other])

        i = l if m == self[l] else (r if m == self[r] else other)

        self.swap(i, self.size - 1)
        self.size -= 1
        ret = self.array.pop(self.size)
        
        self.downheap(i)

        return ret

    def insert(self, new: Node):
        MaxHeap.last2.pop(0)
        MaxHeap.last2.append(new.data)

        self.array.append(new)
        self.size += 1
        self.upheap(self.size - 1)

    def update(self, i: int, newPriority: float):
        arr = self.array
        iNode = arr[i]

        if newPriority > iNode.priority:
            iNode.priority = newPriority
            self.upheap(i)
        else: 
            iNode.priority = newPriority
            self.downheap(i)

    def __str__(self):
        return str([str(i) for i in self.array])

def level(i: int) -> int:
    return math.floor(math.log2(i+1))

class MaxMinHeap:
    # from https://en.wikipedia.org/wiki/Min-max_heap
    last2 = [(0, 0), (0, 0)]

    def __init__(self, array: List[Node], last2: List[Tuple[int, int]] = [(0, 0), (0, 0)]):
        self.array = [i for i in array]
        self.size = len(array)
        MaxMinHeap.last2 = last2

        # heapify by pushing down
        for i in range(self.size // 2 - 1, -1, -1):
            self.pushdown(i)

    def __getitem__(self, index: int) -> Node:
        return self.array[index]

    def __setitem__(self, index: int, node: Node):
        self.array[index] = node

    def __contains__(self, i: int) -> bool:
        return i < self.size and i >= 0

    def __str__(self):
        return str([str(i) for i in self.array])

    def greater(self, x: int, y: int) -> bool:
        return self[x] > self[y]

    def less(self, x: int, y: int) -> bool:
        return self[x] < self[y]

    def swap(self, i: int, j: int):
        self[j], self[i] = self[i], self[j]

    def grandchildren(self, i: int) -> List[int]:
        """Get all valid grandchildren of node i"""
        grandchildren = []
        l = leftChild(i)
        r = rightChild(i)

        if l in self:
            if leftChild(l) in self:
                grandchildren.append(leftChild(l))
            if rightChild(l) in self:
                grandchildren.append(rightChild(l))

        if r in self:
            if leftChild(r) in self:
                grandchildren.append(leftChild(r))
            if rightChild(r) in self:
                grandchildren.append(rightChild(r))

        return grandchildren

    def pushdown(self, i: int):
        if level(i) % 2 == 0:  # max level
            self.pushdown_rec(i, self.greater, max)
        else:  # min level
            self.pushdown_rec(i, self.less, min)

    def pushdown_rec(self, i: int, op: Callable, max_or_min: Callable):
        candidates = [i for i in [leftChild(i), rightChild(i)] if i in self] + self.grandchildren(i)
        if not candidates: return

        # Find the largest
        m = max_or_min(candidates, key=lambda x: self[x].priority)

        if op(m, i):
            self.swap(m, i)

            # If m is a grandchild
            if m in self.grandchildren(i):
                # Check if we need to swap with parent
                if parent(m) in self and op(parent(m), m):
                    self.swap(m, parent(m))
                self.pushdown(m)
            # If m is a child, we might need to continue
            elif m in [leftChild(i), rightChild(i)]:
                self.pushdown(m)

    def pushup(self, i: int):
        if i == 0: return
        
        if level(i) % 2 == 0:
            if self[i] < self[parent(i)]:
                self.swap(i, parent(i))
                self.pushup_rec(parent(i), self.less)
            else:
                self.pushup_rec(i, self.greater)
        else:
            if self[i] > self[parent(i)]:
                self.swap(i, parent(i))
                self.pushup_rec(parent(i), self.greater)
            else:
                self.pushup_rec(i, self.less)
    
    def pushup_rec(self, i: int, op: Callable):
        if i == 0: return

        g = parent(parent(i))
        if g in self and op(i, g):
            self.swap(i, g)
            self.pushup_rec(g, op)

    def insert(self, new: Node):
        MaxMinHeap.last2.pop(0)
        MaxMinHeap.last2.append(new.data)

        self.array.append(new)
        self.size += 1
        self.pushup(self.size - 1)

    def remove(self, i: int) -> Node:
        if i >= self.size:
            raise IndexError("Index out of bounds")

        self.swap(i, self.size - 1)
        self.size -= 1
        ret = self.array.pop()

        if i < self.size:
            self.pushdown(i)
            self.pushup(i)

        return ret

    def peekMax(self) -> Node:
        if len(self.array) == 0:
            raise LookupError("Heap is empty")
        return self.array[0]

    def peekMin(self) -> Node:
        if len(self.array) == 0:
            raise LookupError("Heap is empty")
        if len(self.array) == 1:
            return self.array[0]
        if len(self.array) == 2:
            return self.array[1]
        return min(self.array[1], self.array[2])

    def peekSecondMax(self) -> Node:
        if len(self.array) <= 1:
            raise LookupError("Not enough elements")
        if len(self.array) == 2:
            return self.array[1]

        # Find second largest among children and grandchildren of root
        candidates = [1]  # Always include first child
        if 2 in self:
            candidates.append(2)

        # Add grandchildren
        candidates.extend(self.grandchildren(0))

        # Remove the maximum to find second maximum
        candidates.sort(key=lambda x: self[x].priority, reverse=True)
        return self[candidates[1]] if len(candidates) > 1 else self[candidates[0]]

    def extractMax(self) -> Node:
        return self.remove(0)

    def extractMin(self) -> Node:
        if self.size <= 1:
            return self.remove(0)
        if self.size == 2:
            return self.remove(1)

        min_idx = 1 if self[1] < self[2] else 2
        return self.remove(min_idx)

    def extract(self) -> Node:
        if self.peekMax().data not in MaxMinHeap.last2:
            return self.extractMax()
        elif self.size > 1 and self.peekSecondMax().data not in MaxMinHeap.last2:
            # Find the index of second max and remove it
            if self.size == 2:
                return self.remove(1)

            candidates = [1]
            if 2 in self:
                candidates.append(2)
            candidates.extend(self.grandchildren(0))

            candidates.sort(key=lambda x: self[x].priority, reverse=True)
            second_max_idx = candidates[1] if len(candidates) > 1 else candidates[0]
            return self.remove(second_max_idx)
        else:
            # Find third max
            candidates = [1]
            if 2 in self:
                candidates.append(2)
            candidates.extend(self.grandchildren(0))

            if len(candidates) >= 3:
                candidates.sort(key=lambda x: self[x].priority, reverse=True)
                return self.remove(candidates[2])
            else:
                return self.extractMax()  # Fallback
