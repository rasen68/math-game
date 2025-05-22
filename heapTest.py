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
    heapSize = 40
    trials = 10

    def assertHeap(self, heap: MaxHeap):
        for i in range (heap.size):
            l = leftChild(i)
            r = rightChild(i)

            if l in heap:
                self.assertLess(heap[l], heap[i])
            if r in heap:
                self.assertLess(heap[r], heap[i])

    def test_heapify(self):
        start = time.time()

        for j in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize*10)]
            for k in range(self.heapSize*10):
                unsorted.append(Node(priorities[k], (0, j)))
            heap = MaxHeap(unsorted)

            self.assertHeap(heap)
        
        print("\nheapify:", time.time() - start)

    def test_extractMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize

            # this particular program will never need an empty heap
            for j in range(self.heapSize - 1):
                s = heap.extractMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(s, heap.peekMax())
                for i in heap:
                    self.assertGreater(s, i)
                currentSize -= 1

        print("\nextractMax:", time.time() - start)
    
    def test_extractSecondMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 1):
                s = heap.extractSecondMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(heap.peekMax(), s)
                for i in heap:
                    if i != heap.peekMax():
                        self.assertGreater(s, i)
                currentSize -= 1

        print("\nextractSecondMax:", time.time() - start)

    def test_extractThirdMax(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                s = heap.extractThirdMax()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                self.assertGreater(heap.peekMax(), s)
                self.assertGreater(heap.peekSecondMax(), s)
                for i in heap:
                    if i != heap.peekMax() and i != heap.peekSecondMax():
                        self.assertGreater(s, i)
                currentSize -= 1

        print("\nextractThirdMax:", time.time() - start)
    
    def test_extract(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                print(heap)
                m = heap.extract()
                self.assertHeap(heap)
                self.assertEqual(currentSize - 1, heap.size)
                for i in heap:
                    if i.data not in MaxHeap.last2:
                        self.assertGreaterEqual(m, i)
                currentSize -= 1

        print("\nextract:", time.time() - start)
    
    def test_insert(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            currentSize = self.heapSize
            for j in range(self.heapSize - 2):
                heap.insert((Node(random.random() * 10, (0, j))))
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
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            for i in range(self.heapSize - 2):
                m = heap.extract()
                self.assertHeap(heap)
                for n in heap:
                    if n.data not in MaxHeap.last2:
                        self.assertGreaterEqual(m, n)
                heap.insert((Node(random.random() * 10, (i, 0))))
                self.assertHeap(heap)
                self.assertEqual(self.heapSize, heap.size)

        print("\ninsert:", time.time() - start)

    def test_update(self):
        start = time.time()

        for i in range(self.trials):
            unsorted = []
            priorities = [random.random() * 10 for i in range(self.heapSize)]
            for j in range(self.heapSize):
                unsorted.append(Node(priorities[j], (0, j)))
            heap = MaxHeap(unsorted)
            
            for i in range(self.heapSize):
                heap.update(i, random.random() * 10)
                self.assertHeap(heap)

        print("\nupdate:", time.time() - start)

if __name__ == '__main__':
    unittest.main()