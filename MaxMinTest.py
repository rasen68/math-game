import unittest
import random
import time
import math
from heap import Node, MaxMinHeap

def parent(i: int) -> int:
    return (i - 1) // 2
    
def leftChild(i: int) -> int:
    return (2 * i) + 1

def rightChild(i: int) -> int: 
    return (2 * i) + 2

def level(i: int) -> int:
    return math.floor(math.log2(i+1))

class MaxMinTest(unittest.TestCase):
    heapSize = 400
    trials = 10

    def assertHeap(self, heap: MaxMinHeap):
        for i in range(heap.size):
            l = leftChild(i)
            r = rightChild(i)
            if level(i) % 2 == 0:
                if l in heap:
                    self.assertLess(self[l], self[i])
                if r in heap:
                    self.assertLess(self[r], self[i])
            else:
                if l in heap:
                    self.assertGreater(self[l], self[i])
                if r in heap:
                    self.assertGreater(self[r], self[i])

    def test_heapify(self):
        start = time.time()

        for j in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize*10)]
            for k in range(self.heapSize*10):
                unsorted.append(Node(priorities[k], (0, 0)))
            heap = MaxMinHeap(unsorted)

            self.assertHeap(heap)
        
        print("\nheapify:", time.time() - start)

    def test_extractMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxMinHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                m = heap.extractMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                for i in heap:
                    if i not in MaxMinHeap.last2:
                        self.assertGreater(m, i)
                currentSize -= 1

        print("\nextract:", time.time() - start)

    def test_extractMin(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxMinHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                m = heap.extractMin()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                for i in heap:
                    self.assertLess(m, i)
                currentSize -= 1

        print("\nextract:", time.time() - start)

    def test_insert(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxMinHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                heap.insert((Node(random.random() * 10, (0, 0))))
                self.assertHeap(heap)
                self.assertEqual(currentSize + 1, heap.size)
                currentSize += 1

        print("\ninsert:", time.time() - start)

    def test_extract_insert(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxMinHeap(unsorted)
            
            for i in range(self.heapSize - 2):
                heap.extract()
                self.assertHeap(heap)
                heap.insert((Node(random.random() * 10, (0, 0))))
                self.assertHeap(heap)
                self.assertEqual(self.heapSize, heap.size)

        print("\ninsert:", time.time() - start)

if __name__ == '__main__':
    unittest.main()