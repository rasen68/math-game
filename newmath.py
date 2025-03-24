from heap import MaxHeap, Node
from mathio import MathIO
from typing import List, Tuple

def times(first: int, second: int) -> int:
    return first * second 

def minus(first: int, second: int) -> int:
    return first - second

def plus(first: int, second: int) -> int:
    return first + second

def seedShuffle(seed: int, allNums: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    shuffled = []
    tempSeed = seed
    while len(allNums) > 0:
        i = tempSeed % len(allNums)
        tempSeed //= len(allNums)
        if tempSeed == 0: tempSeed = seed

        shuffled.append(allNums.pop(i))
    return shuffled

def pretest(io: MathIO, allNums: List[Tuple[int, int]]) -> Tuple[MaxHeap, MaxHeap]:
    shuffled = seedShuffle(io.seed, allNums)

    last2 = [(0, 0),(0, 0)]
    arr = []
    for i in shuffled:
        t = io.questionAnswer(i)
        arr.append(Node(t, i))
        last2.pop(0)
        last2.append(i)
    
    heap1 = MaxHeap(arr, last2)
    heap2 = MaxHeap(arr, last2)
    return heap1, heap2 

def processQuestion(io: MathIO, heap: MaxHeap, question: Node):
    t2 = io.questionAnswer(question.data) 
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
        if processQuestion(io, whichHeap, question) == 0:
            break

        # + 1.5 seconds to fastest question
        last = whichHeap.size - 1
        whichHeap.update(last, whichHeap.array[last].priority + 1.5)
        whichHeap = heaps[io.which]

    io.end(heaps[0], heaps[1])
                     
def makeQuestions(num1s: List[int], num2s: List[int] = None, 
                  extras: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
    if not num2s:
        num2s = num1s
    allNums = []

    for num1 in num1s:
        for num2 in num2s:
            allNums.append((num1, num2))
    
    if extras:
        for extra in extras:
            allNums.append(extra)
    
    return allNums
    
def makeAddition(nums: List[int]) -> List[Node]:
    for i in nums:
        if i == -1:
            makeQuestions()


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
        print()

        return makeTimesTablesHard(tables)
    elif (io.opStr == 'times'):
        io.setOp(times)
        io.setFile("multiplication")
        tables = [int(i) for i in input("Times tables? ").split()]
        print()

        return makeTimesTables(tables)
    elif (io.opStr == 'minus'):
        io.setOp(minus)
        io.setFile("subtraction")
        tables = [int(i) for i in input("Subtraction tables? ").split()]
        print()

        return makeQuestions(tables, list(range(1, 9)))
    elif (io.opStr == 'plus'):
        io.setOp(plus)
        io.setFile("addition")
        tables = [int(i) for i in input("Addition tables? ").split()]
        print()

        return makeQuestions(tables, list(range(1, 9)))
    
    else:
        raise ValueError

def main():
    io = MathIO()
    seed = io.setInput()

    allNums = setOpStr(io)
    heap1, heap2 = pretest(io, allNums)
    drill(io, (heap1, heap2))

if __name__ == "__main__":
    main()