from heap import MaxHeap, Node
from mathio import MathIO
from typing import List, Tuple
from numsdict import NumsDict

def times(first: int, second: int) -> int:
    return first * second 

def minus(first: int, second: int) -> int:
    return first - second

def plus(first: int, second: int) -> int:
    return first + second

def letter(first: str, second: str) -> str:
    o1 = ord(first) - ord('a') + 1
    o2 = ord(second) - ord('a') + 1
    return chr(ord('a') + o1 + o2 - 1)

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
    
    print() # newline to mark the end of pretest
    heap1 = MaxHeap(arr, last2)
    heap2 = MaxHeap(arr, last2)
    return heap1, heap2 

def processQuestion(io: MathIO, heap: MaxHeap, question: Node):
    t2 = io.questionAnswer(question.data) 
    if t2 == 0:
        heap.insert(question)
        return 0
    
    average = (t2 * 2 + question.priority) / 3
    if average > 20: average = 20
    newQuestion = Node(average, question.data)

    heap.insert(newQuestion)

def drill(io: MathIO, heaps: Tuple[MaxHeap]):
    whichHeap = heaps[io.which]
    
    while True:
        question = whichHeap.extract()
        if processQuestion(io, whichHeap, question) == 0:
            break

        # + 1 second to last question (not necessarily fastest... for now)
        last = whichHeap.size - 1
        whichHeap.update(last, whichHeap.array[last].priority + 1)
        whichHeap = heaps[io.which]

    io.end(heaps[0], heaps[1])
    
def makeAddition(nums: List[int]) -> List[Tuple[int, int]]:
    dict = NumsDict()
    allNums = []
    for j in nums:
        if j == 1:
            allNums += dict.makeQuestions([1], range(1, 11))
        elif j == 2:
            allNums += dict.makeQuestions([2], range(2, 11))
        elif j == 8:
            allNums += dict.makeQuestions([8], range(1, 9))
        elif j == 9:
            allNums += dict.makeQuestions([9], range(1, 10))
        elif j == 10:
            allNums += dict.makeQuestions([], extras=[(i, 10-i) for i in range(1, 6)])
        elif j == -1:
            allNums += dict.makeQuestions([3], range(3, 7), [(4, 4), (4, 5)])
        elif j == 11:
            allNums += dict.makeQuestions([7], range(4, 8), [(5, 6), (6, 6)])
        elif j == 22:
            allNums += dict.makeQuestions([], extras=[(i, i) for i in range(1, 11)])
        else:
            allNums += dict.makeQuestions([j], range(2, 10))
    return allNums

def makeSubtraction(nums: List[int]) -> List[Tuple[int, int]]:
    dict = NumsDict()
    allNums = []
    for i in nums:
        if i == 1:
            allNums += dict.makeQuestions()

def makeTimesTables(nums: List[int]) -> List[Tuple[int, int]]:
    dict = NumsDict()
    lis = list(range(2, 13))
    return dict.makeQuestions(nums, lis)

def makeTimesTablesHard(nums: List[int]) -> List[Tuple[int, int]]:
    dict = NumsDict()
    extras = []
    lis = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append((12, 10))
        extras.append((12, 11))
    if 11 in nums:
        extras.append((11, 10))
        extras.append((11, 11))
    return dict.makeQuestions(nums, lis, extras)

def makeLetter(nums: List[str]) -> List[Tuple[str, str]]:
    dict = NumsDict()
    allNums = []
    for i in nums:
        if i == 'aa':
            allNums += dict.makeQuestions([], extras=[(chr(ord('a') + j), chr(ord('a') + j)) for j in range(0, 13)])
        else:
            allNums += dict.makeQuestions([i], [chr(ord('a') + j) for j in range(0, ord('z') - ord(i))])
    return allNums

def setOpStr(io: MathIO) -> List[Tuple[int, int]]:
    if (io.opStr == 'timeshard'):
        io.opStr = 'times'
        io.setOp(times)
        io.setFile("times")
        tables = [int(i) for i in input("Times tables? ").split()]
        print()

        return makeTimesTablesHard(tables)
    elif (io.opStr == 'times'):
        io.setOp(times)
        tables = [int(i) for i in input("Times tables? ").split()]
        print()

        return makeTimesTables(tables)
    elif (io.opStr == 'minus'):
        io.setOp(minus)
        tables = [int(i) for i in input("Subtraction tables? ").split()]
        print()

        return makeSubtraction(tables)
    elif (io.opStr == 'plus'):
        io.setOp(plus)
        tables = [int(i) for i in input("Addition tables? ").split()]
        print()

        return makeAddition(tables)
    elif (io.opStr == 'letter'):
        io.opStr = 'plus'
        io.setOp(letter)
        tables = [i for i in input("Addition tables? ").split()]
        print()

        return makeLetter(tables)
    else:
        raise ValueError

def main():
    io = MathIO()
    io.setInput()

    allNums = setOpStr(io)
    heap1, heap2 = pretest(io, allNums)
    drill(io, (heap1, heap2))

if __name__ == "__main__":
    main()