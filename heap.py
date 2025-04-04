from typing import List, Tuple
import math

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

    def __str__(self):
        return str(self.data) + ": " + str(self.priority)

class MaxHeap:
    last2 = [(0, 0), (0, 0)]

    def __init__(self, array: List[Node], last2: List[Tuple[int, int]] = [(0, 0), (0, 0)]):
        self.array = [i for i in array]
        self.size = len(array)
        self.mins = [min(array)]
        MaxHeap.last2 = last2

        secondLastLayer = 2 ** (math.floor(math.log2(self.size))) - 2

        # heapify by downheaping 
        for i in range(secondLastLayer, -1, -1):
            self.downheap(i)
    
    def upheap(self, i: int):
        arr = self.array
        p = parent(i)

        if p >= 0:
            pNode = arr[p]
            iNode = arr[i]
            if pNode < iNode:
                arr[p], arr[i] = arr[i], arr[p]
                self.upheap(p)
    
    def downheap(self, i: int):
        arr = self.array
        r = rightChild(i)
        l = leftChild(i)

        # if r doesn't exist we only need to test for l
        if r == self.size and arr[l] > arr[i]:
            arr[l], arr[i] = arr[i], arr[l]
            self.downheap(l)

        if r < self.size:
            rNode = arr[r]
            lNode = arr[l]
            iNode = arr[i]

            m = max(rNode, lNode, iNode)
            if m != iNode:
                s = r if m == rNode else l
                arr[s], arr[i] = arr[i], arr[s]
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
        arr = self.array
        arr[0], arr[self.size - 1] = arr[self.size - 1], arr[0]
        self.size -= 1
        ret = self.array.pop(self.size)

        self.downheap(0)

        return ret
    
    def extractSecondMax(self) -> Node:
        arr = self.array
        i = 1 if (2 >= self.size or arr[1] > arr[2]) else 2
        
        arr[i], arr[self.size - 1] = arr[self.size - 1], arr[i]
        self.size -= 1
        ret = self.array.pop(self.size)
        
        self.downheap(i)

        return ret

    def extractThirdMax(self) -> Node:
        arr = self.array
        secondMax = 1 if arr[1] > arr[2] else 2
        other = 2 if secondMax == 1 else 1
        l = leftChild(secondMax) if leftChild(secondMax) < self.size else other
        r = rightChild(secondMax) if rightChild(secondMax) < self.size else l
        m = max(arr[l], arr[r], arr[other])
        i = l if m == arr[l] else (r if m == arr[l] else other)

        arr[i], arr[self.size - 1] = arr[self.size - 1], arr[i]
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