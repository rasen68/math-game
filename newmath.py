import random
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
from heap import maxHeap, Node
from typing import List, Tuple, TextIO

def inputLoop(question, answer, file):
    start = time.time()
    while True:
        userAnswer = input()
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

def questionAnswer(i: Node, operation: str, student: str, file: TextIO):
    first = i.data[0]
    second = i.data[1]
    question = f"{student}: What's {first} {operation} {second}?"
    answer = first * second if operation == "times" else first - second

    print(question)
    file.write(question + "\n")

    time = inputLoop(question, answer, file)
    if time == 0:
        return 0

    print("Good job!")
    print()
    mixer.init()
    mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + "\\Untitled-score.ogg")
    mixer.music.play()

    file.write(str(round(time, 2)) + "\n")
    return time

def pretestMult(student1: str, student2: str, allNums: List[Node], file: TextIO):
    shuffled = [i for i in allNums]
    random.shuffle(shuffled)
    last2 = [(0, 0), (0, 0)]
    arr = []
    whichStudent = student1

    for i in shuffled:
        t = questionAnswer(i, "times", whichStudent, file)
        #print(f"{t:.2f}")
        arr.append(Node(t, i.data))
        last2.pop(0)
        last2.append(i)
        whichStudent = student1 if whichStudent==student2 else student2

    heap = maxHeap(arr)
    return heap, last2 

def drill(allNums: List[Node], operation: str, student1: str, student2: str, file: TextIO):
    if operation == "times":
        heap1, last2 = pretestMult(student1, student2, allNums, file)
    #else:
       # queue1, last2 = pretestSub(student1, student2, )
    
    dummy = Node(0, (0, 0))
    heap2 = maxHeap([dummy]) # heap initialisation requires nonempty array
    heap2.extractMax()
    heap2.array = [i for i in heap1.array]

    whichStudent = student1 if len(allNums)%2==0 else student2
    whichHeap = heap1 if len(allNums)%2==0 else heap2
    
    while True:
        # find question
        if whichHeap.peekMax().data not in last2:
            question = whichHeap.extractMax()
        elif whichHeap.peekSecondMax().data not in last2:
            question = whichHeap.extractSecondMax()
        else:
            question = whichHeap.extractThirdMax()

        # process question
        last2.pop(0)
        last2.append(question.data)

        t2 = questionAnswer(question, operation, whichStudent, file) 
        if t2 == 0:
            break
        
        elif (t2 * 2 + question.priority) / 3 > 30:
            average = 30
        else:
            average = (t2 * 2 + question.priority) / 3
        question = Node(average, question.data)

        whichHeap.insert(question)

        # + 1.5 seconds to fastest question
        last = whichHeap.size - 1
        whichHeap.update(last, whichHeap.array[last].priority + 1.5)

        whichStudent = student1 if whichStudent==student2 else student2
        whichHeap = heap1 if whichHeap==heap2 else heap2

    file.write(student1 + ": " + str(heap1) + "\n")
    file.write(student2 + ": " + str(heap2))
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
    
def makeTimesTables(nums) -> List[Node]:
    lis = list(range(2, 13))
    return makeQuestions(nums, lis)

def makeTimesTablesHard(nums) -> List[Node]:
    extras = []
    lis = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append((12, 10))
        extras.append((12, 11))
    if 11 in nums:
        extras.append((11, 10))
        extras.append((11, 11))
    return makeQuestions(nums, lis, extras)

if __name__ == "__main__":
    student1 = input("Student 1? ")
    student2 = input("Student 2? ")
    operation = 'stuff'

    while (operation != 'times' and operation != 'minus' and operation != 'plus'):
        operation = input("Operation? ")

    if (operation == 'times'):
        tables = input("Times tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.getcwd() + "\\tutoring-files\\multiplication\\" + student1 + student2 + ".txt", "a")
        allNums = makeTimesTablesHard(tables)

    else:
        tables = input("Subtraction tables? ").split()
        tables = [int(i) for i in tables]
        file = open(os.getcwd() + "\\tutoring-files\\subtraction\\" + student1 + student2 + ".txt", "a")
        allNums = makeQuestions(tables, list(range(1, 9)))
    
    drill(allNums, operation, student1, student2, file)
    