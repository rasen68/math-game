import random
import time
import os
from pygame import mixer
from heap import maxHeap, Node
from typing import List, Tuple, TextIO

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
student1 = ""
student2 = ""
operation = ""
file = ""
seed = 0

def inputLoop(question: str, answer: int):
    start = time.time()
    while True:
        userAnswer = input().strip()
        if userAnswer == str(answer):
            file.write(userAnswer + "\n")
            return time.time() - start
        elif userAnswer == "end":
            return 0
        elif userAnswer == "":
            continue
        elif userAnswer == "q":
            return time.time() - start
        elif userAnswer == "unpause":
            start = time.time()
        else:
            file.write(userAnswer + "\n")
            print("Not quite! Try again")
            print()
            print(question)

def questionAnswer(i: Node, student: str):
    first = i.data[0]
    second = i.data[1]
    question = f"{student}: What's {first} {operation} {second}?"
    answer = first * second if operation == "times" else first - second

    print(question)
    file.write(question + "\n")

    time = inputLoop(question, answer)
    if time == 0:
        return 0

    print("Good job!")
    print()
    mixer.init()
    dir = os.path.dirname(os.path.abspath(__file__))
    mixer.music.load(os.path.join(dir, "Untitled-score.ogg"))
    mixer.music.play()

    file.write(str(round(time, 2)) + "\n")
    return time

def pretestMult(allNums: List[Node]) -> Tuple[maxHeap, maxHeap, List[Node]]:
    shuffled = []
    tempSeed = seed
    while len(allNums) > 0:
        i = tempSeed % len(allNums)
        tempSeed //= len(allNums)
        if tempSeed == 0: tempSeed = seed

        shuffled.append(allNums.pop(i))

    last2 = [(0, 0), (0, 0)]
    arr = []
    whichStudent = student1

    for i in shuffled:
        t = questionAnswer(i, whichStudent)
        #print(f"{t:.2f}")
        arr.append(Node(t, i.data))
        last2.pop(0)
        last2.append(i)
        whichStudent = student1 if whichStudent==student2 else student2
    
    heap1 = maxHeap(arr)
    heap2 = maxHeap(arr)
    return heap1, heap2, last2 

def findQuestion(heap: maxHeap, last2: List[Node]):
    if heap.peekMax().data not in last2:
        return heap.extractMax()
    elif heap.peekSecondMax().data not in last2:
        return heap.extractSecondMax()
    else:
        return heap.extractThirdMax()

def processQuestion(last2: List[Node], heap: maxHeap, question: Node, student: str):
    last2.pop(0)
    last2.append(question.data)

    t2 = questionAnswer(question, student) 
    if t2 == 0:
        heap.insert(question)
        return 0
    
    average = (t2 * 2 + question.priority) / 3
    newQuestion = Node(average, question.data) if average < 30 else Node(30, question.data)

    heap.insert(newQuestion)

def drill(which: int, heaps: Tuple[maxHeap], last2: List[Node]):
    whichStudent = student1 if which==0 else student2
    whichHeap = heaps[0] if which==0 else heaps[1]
    
    while True:
        question = findQuestion(whichHeap, last2)

        if processQuestion(last2, whichHeap, question, whichStudent) == 0:
            break
        

        # + 1.5 seconds to fastest question
        last = whichHeap.size - 1
        whichHeap.update(last, whichHeap.array[last].priority + 1.5)

        whichStudent = student1 if whichStudent==student2 else student2
        whichHeap = heaps[0] if whichHeap==heaps[1] else heaps[1]

    file.write(student1 + ": " + str(heaps[0]) + "\n")
    file.write(student2 + ": " + str(heaps[1]))
    file.close()
                     
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

def setUp():
    # These global variables never change after main access
    global student1, student2, operation, file, seed

    student1 = input("Student 1? ")
    student2 = input("Student 2? ")
    operation = ""

    valid = ["times", "timeshard", "test", "minus", "plus"]

    while operation not in valid:
        operation = input("Operation? ")

    if operation == "test":
        seed = 1_234_567_890
        operation = input("Operation? ")
    else:
        seed = random.randint(1_000_000_000, 10_000_000_000)

    if (operation == 'timeshard'):
        operation = 'times'
        tables = input("Times tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.path.join(os.getcwd(), "tutoring-files", "multiplication", student1 + student2 + ".txt"), "a")
        allNums = makeTimesTablesHard(tables)
        which = len(allNums)%2
        heap1, heap2, last2 = pretestMult(allNums)

    elif (operation == 'times'):
        tables = input("Times tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.path.join(os.getcwd(), "tutoring-files", "multiplication", student1 + student2 + ".txt"), "a")
        allNums = makeTimesTables(tables)
        which = len(allNums)%2
        heap1, heap2, last2 = pretestMult(allNums)

    elif (operation == 'minus'):
        tables = input("Subtraction tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.path.join(os.getcwd(), "tutoring-files", "subtraction", student1 + student2 + ".txt"), "a")
        allNums = makeQuestions(tables, list(range(1, 9)))
    
    elif (operation == 'plus'):
        tables = input("Addition tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.path.join(os.getcwd(), "tutoring-files", "addition", student1 + student2 + ".txt"), "a")
        allNums = makeQuestions(tables, list(range(1, 9)))
    
    else:
        raise ValueError
    
    drill(which, (heap1, heap2), last2)

setUp()

