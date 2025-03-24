import unittest
import random
import time
from heap import Node, MaxHeap

def parent(i: int) -> int:
    return (i - 1) // 2
    
def leftChild(i: int) -> int:
    return (2 * i) + 1

def rightChild(i: int) -> int: 
    return (2 * i) + 2

class HeapTest(unittest.TestCase):
    heapSize = 400
    trials = 10

    def assertHeap(self, heap: MaxHeap):
        for i in range (heap.size):
            l = leftChild(i)
            r = rightChild(i)
            arr = heap.array

            if l < heap.size:
                self.assertLess(arr[l].priority, arr[i].priority)
            if r < heap.size:
                self.assertLess(arr[r].priority, arr[i].priority)

    def test_heapify(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxHeap(unsorted)

            self.assertHeap(heap)
        
        print("\nheapify:", time.time() - start)

    def test_extractMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            # this particular program will never need an empty heap
            for i in range(self.heapSize - 1):
                s = heap.extractMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(s, heap.peekMax())
                currentSize -= 1

        print("\nextractMax:", time.time() - start)
    
    def test_extractSecondMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for i in range(self.heapSize - 1):
                s = heap.extractSecondMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(heap.peekMax(), s)
                currentSize -= 1

        print("\nextractSecondMax:", time.time() - start)

    def test_extractThirdMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for i in range(self.heapSize - 2):
                s = heap.extractThirdMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(heap.peekSecondMax(), s)
                currentSize -= 1

        print("\nextractThirdMax:", time.time() - start)

    def test_update(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, 0)))
            heap = MaxHeap(unsorted)
            
            for i in range(self.heapSize):
                heap.update(i, random.random() * 10)
                self.assertHeap(heap)

        print("\nupdate:", time.time() - start)

if __name__ == '__main__':
    unittest.main()