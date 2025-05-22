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

        secondLastLayer = 2 ** (math.floor(math.log2(self.size))) - 2

        # heapify by pushing down 
        for i in range(secondLastLayer, -1, -1):
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

    def grandchild(self, i: int, op: Callable) -> Tuple[int, int]:
        possible = [rightChild(leftChild(i)), leftChild(rightChild(i)), rightChild(rightChild(i))]
        current = leftChild(leftChild(i))
        next = 0
        for i in possible:
            if i in self and op(i, current):
                next = current
                current = i
            elif next != 0 and op(i, next):
                next = i
        return (current, next)
    
    def pushdown(self, i: int):
        if level(i) % 2 == 1:
            self.pushdownrec(i, self.greater)
        else:
            self.pushdownrec(i, self.less)

    def pushdownrec(self, i: int, op: Callable):
        if leftChild(i) in self:
            if rightChild(i) not in self or op(leftChild(i), rightChild(i)):
                c = leftChild(i)
            else: c = rightChild(i)

            if (leftChild(leftChild(i)) in self and op(g := self.grandchild(i, op)[0], c)):
                if op(g, i):
                    self.swap(g, i)
                    if not op(g, parent(g)):
                        self.swap(g, parent(g))
                    self.pushdown(g)
            elif op(c, i):
                self.swap(c, i)
    
    def pushup(self, i: int):
        if i != 0:
            if level(i) % 2 == 1:
                if self[i] > self[parent(i)]:
                    self.swap(i, parent(i))
                    self.pushuprec(parent(i), self.greater)
                else:
                    self.pushuprec(i, self.less)
            else:
                if self[i] < self[parent(i)]:
                    self.swap(i, parent(i))
                    self.pushuprec(parent(i), self.less)
                else:
                    self.pushuprec(i, self.greater)
    
    def pushuprec(self, i: int, op: Callable):
        if g := parent(parent(i)) in self and op(i, g):
            self.swap(i, g)
            self.pushuprec(i, op)
    
    def insert(self, new: Node):
        MaxMinHeap.last2.pop(0)
        MaxMinHeap.last2.append(new.data)

        self[self.size] = new
        self.size += 1
        self.pushup(self.size - 1)
    
    def remove(self, i: int) -> Node:
        self.swap(i, self.size - 1)
        self.size -= 1
        ret = self.array.pop(self.size)

        self.pushdown(i)

        return ret
    
    def peekMax(self) -> Node:
        if len(self.array) == 0:
            raise LookupError
        return self[0]

    def peekSecondMax(self) -> Node:
        if len(self.array) <= 1:
            raise LookupError
        if len(self.array) == 2:
            return self[1]
        return self.grandchild(0, self.greater)

    def extract(self) -> Node:
        if self.peekMax().data not in MaxHeap.last2:
            return self.remove(0)
        elif self.peekSecondMax().data not in MaxHeap.last2:
            return self.remove(self.grandchild(0, self.greater)[0])
        else:
            (g, n) = self.grandchild(0, self.greater)
            if self[gg := self.grandchild(g)[0]] > self[n]: 
                return self.remove(gg)
            else:
                return self.remove(n)
    
    def extractMin(self) -> Node:
        return self.remove(1) if self[1] > self[2] else self.remove(2)