import os
from heap import MaxHeap, Node
from mathio import MathIO
from typing import List, Tuple
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def times(first: int, second: int) -> int:
    return first * second 

def minus(first: int, second: int) -> int:
    return first - second

def plus(first: int, second: int) -> int:
    return first + second

def seedShuffle(seed: int, allNums: List[Node]) -> List[Node]:
    shuffled = []
    tempSeed = seed
    while len(allNums) > 0:
        i = tempSeed % len(allNums)
        tempSeed //= len(allNums)
        if tempSeed == 0: tempSeed = seed

        shuffled.append(allNums.pop(i))
    return shuffled

def pretest(io: MathIO, seed: int, allNums: List[Node]) -> Tuple[MaxHeap, MaxHeap]:
    shuffled = seedShuffle(seed, allNums)

    last2 = [(0, 0),(0, 0)]
    arr = []
    for i in shuffled:
        t = io.questionAnswer(i)
        arr.append(Node(t, i.data))
        last2.pop(0)
        last2.append(i.data)
    
    heap1 = MaxHeap(arr, last2)
    heap2 = MaxHeap(arr, last2)
    return heap1, heap2 

def processQuestion(heap: MaxHeap, question: Node):
    t2 = io.questionAnswer(question) 
    if t2 == 0:
        heap.insert(question)
        return 0
    
    average = (t2 * 2 + question.priority) / 3
    newQuestion = Node(average, question.data) if average < 30 else Node(30, question.data)

    heap.insert(newQuestion)

def drill(io: MathIO, heaps: Tuple[MaxHeap]):
    whichHeap = heaps[io.which]
    
    while True:
        question = whichHeap.extract()
        if processQuestion(whichHeap, question) == 0:
            break

        # + 1.5 seconds to fastest question
        last = whichHeap.size - 1
        whichHeap.update(last, whichHeap.array[last].priority + 1.5)
        whichHeap = heaps[io.which]

    io.end(heaps[0], heaps[1])
                     
def makeQuestions(num1s: List[int], num2s: List[int] = None, extras: List[Tuple[int, int]] = None) -> List[Node]:
    if not num2s:
        num2s = num1s
    allNums = []

    for num1 in num1s:
        for num2 in num2s:
            node = Node(0, (num1, num2))
            allNums.append(node)
    
    if extras:
        for extra in extras:
            node = Node(0, extra)
            allNums.append(node)
    
    return allNums
    
def makeTimesTables(nums: List[int]) -> List[Node]:
    lis = list(range(2, 13))
    return makeQuestions(nums, lis)

def makeTimesTablesHard(nums: List[int]) -> List[Node]:
    extras = []
    lis = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append((12, 10))
        extras.append((12, 11))
    if 11 in nums:
        extras.append((11, 10))
        extras.append((11, 11))
    return makeQuestions(nums, lis, extras)

def setOpStr(io: MathIO):
    if (io.opStr == 'timeshard'):
        io.setOp(times)
        io.setFile("multiplication")
        tables = [int(i) for i in input("Times tables? ").split()]

        return makeTimesTablesHard(tables)
    elif (io.opStr == 'times'):
        io.setOp(times)
        io.setFile("multiplication")
        tables = [int(i) for i in input("Times tables? ").split()]

        return makeTimesTables(tables)
    elif (io.opStr == 'minus'):
        io.setOp(minus)
        io.setFile("subtraction")
        tables = [int(i) for i in input("Subtraction tables? ").split()]

        return makeQuestions(tables, list(range(1, 9)))
    elif (io.opStr == 'plus'):
        io.setOp(plus)
        io.setFile("addition")
        tables = [int(i) for i in input("Addition tables? ").split()]

        return makeQuestions(io, tables, list(range(1, 9)))
    
    else:
        raise ValueError

if __name__ == "__main__":
    io = MathIO()
    seed = io.setInput()

    allNums = setOpStr(io)
    heap1, heap2 = pretest(io, seed, allNums)
    drill(io, (heap1, heap2))