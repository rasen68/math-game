import random
import sys
import time
from scamp import *

'''
global timesTable
timesTable = []
for i in range(13):
    timesTable.append([])
for table in timesTable:
    for i in range(13):
        table.append(0)
'''
  
def drillAdd(low, high):
    num1 = random.randint(low,high)
    num2 = random.randint(low,high)
    question = f"What's {num1} plus {num2}?"
    answer = num1 + num2
    questionAnswer(question, answer)

def drillSub(low, high):
    num1 = random.randint(low,high)
    num2 = random.randint(low,high)
    if num1 > num2:
        question = f"What's {num1} minus {num2}?"
        answer = num1 - num2
    else:
        question = f"What's {num2} minus {num1}?"
        answer = num2 - num1
    questionAnswer(question, answer)

def drillSubTens():
    num1 = random.randint(1, 10) * 10
    num2 = random.randint(1, 9)
    question = f"What's {num1} minus {num2}?"
    answer = num1 - num2
    questionAnswer(question, answer)

def drillDiv(low, high):
    while True:
        num1 = random.randint(low*low,high*high)
        num2 = random.randint(low, high)
        if num1 % num2 == 0:
            break
    question = f"What's {num1} divided by {num2}?"
    answer = num1 // num2
    questionAnswer(question, answer)

def questionAnswer(question, answer):
    start = time.time()
    while True:
        print(question)
        try:
            userAnswer = int(input())
            if userAnswer == answer:
                break
            else:
                print("Not quite! Try again")
                print()
        except:
            continue
    end = time.time()
    #print(f"Time: {end - start:.2f}")
    print("Good job!")
    print()
    #victorySound()

    return end - start



def victorySound():
    key = random.randint(-4, 4)
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = open('trash', 'w')
    sys.sterr = open('trash', 'w')
    
    sesh = Session(tempo = 160)
    
    s = sesh.new_part("soprano")
    a = sesh.new_part("alto")
    t = sesh.new_part("tenor")
    b = sesh.new_part("bass")

    b.play_note(40 + key, 0.5, 0.5, blocking=False)
    t.play_note(52 + key, 0.7, 0.5, blocking=False)
    a.play_note(59 + key, 0.9, 0.5, blocking=False)
    s.play_note(68 + key, 1, 0.5, blocking=True)

    b.play_note(44 + key, 0.5, 0.5, blocking=False)
    t.play_note(56 + key, 0.7, 0.5, blocking=False)
    a.play_note(65 + key, 0.9, 0.5, blocking=False)
    s.play_note(71 + key, 1, 0.5, blocking=True)

    b.play_note(47 + key, 0.5, 0.5, blocking=False)
    t.play_note(59 + key, 0.7, 0.5, blocking=False)
    a.play_note(66 + key, 0.9, 0.5, blocking=False)
    s.play_note(75 + key, 1, 0.5, blocking=True)

    b.play_note(44 + key, 0.5, 0.5, blocking=False)
    t.play_note(56 + key, 0.7, 0.5, blocking=False)
    a.play_note(65 + key, 0.9, 0.5, blocking=False)
    s.play_note(71 + key, 1, 0.5, blocking=True)

    b.play_note(47 + key, 0.5, 1.5, blocking=False)
    t.play_note(59 + key, 0.7, 1.5, blocking=False)
    a.play_note(66 + key, 0.9, 1.5, blocking=False)
    s.play_note(75 + key, 1, 1.5, blocking=True)

    sys.stdout = save_stdout
    sys.sterr = save_stderr

def generateNums(allNums):
    nums = random.choice(allNums)
    if len(nums) == 1:
        loop2 = True
        while loop2:
            loop2 = False
            extraNum = random.choice(allNums)
            if len(extraNum) == 0:
                loop2 = True
            else:
                extraNum = extraNum[0]
        if random.randint(0, 1) == 1:
            num1 = nums[0]
            num2 = random.choice(allNums)[0]
        else:
            num1 = random.choice(allNums)[0]
            num2 = nums[0]
    if random.randint(0, 1) == 1:
        num1 = nums[0]
        num2 = nums[1]
    else:
        num1 = nums[0]
        num2 = nums[1]
    return num1, num2

def probFunction(t):
    if t < 4.6:
        t = 4.6
    return 100 - (150 / (t - 3))

def multQuestionAnswer(i):
    i = list(i)
    question = f"What's {i[0]} times {i[1]}?"
    answer = i[0] * i[1]

    start = time.time()
    while True:
        print(question)
        try:
            userAnswer = int(input())
            if userAnswer == answer:
                break
            else:
                print("Not quite! Try again")
                print()
        except:
            continue
    end = time.time()
    print("Good job!")
    print()
    #victorySound()

    return end - start

def makeQuestions(allNums):
    myDict = {}

    shuffled = [i for i in allNums]
    random.shuffle(shuffled)
    last3 = [(0, 0), (0, 0), (0, 0)]

    queue = [(0, (0, 0))]

    for i in shuffled:
        t = multQuestionAnswer(i)
        print(f"{t:.2f}")

        index = 0
        while index < len(queue):
            if queue[index][0] < t:
                queue.insert(index, (t, i))
                break
            else:
                index += 1
        last3.pop(0)
        last3.append(i)

    while True:
        if queue[0][1] not in last3:
            question = queue[0][1]
        elif queue[1][1] not in last3:
            question = queue[1][1]
        elif queue[2][1] not in last3:
            question = queue[2][1]
        else:
            question = queue[3][1]

        last3.pop(0)
        last3.append(question)
        
        t = multQuestionAnswer(question)

        #print(f"Time: {questionAnswer(question, answer):.2f}")
        

def drillMult(num1s, num2s = None, extras = None):
    if not num2s:
        num2s = num1s
    allNums = []
    for num1 in num1s:
        for num2 in num2s:
            if (num2, num1) not in allNums:
                allNums.append((num1, num2))
    if extras:
        for extra in extras:
            allNums.append(extra)
    
    makeQuestions(allNums)

def drillTimesTables(nums):
    list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    drillMult(nums, list)

def drillTimesTablesHard(nums):
    extras = []
    list = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append([12, 10])
        extras.append([12, 11])
    if 11 in nums:
        extras.append([11, 10])
        extras.append([11, 11])
    drillMult(nums, list, extras)

def drillMultLowHigh(low, high, excludeOne=[], excludeBoth=[]):
    r1 = range(low, high+1)
    r1 = [i for i in r1 if i not in excludeBoth]
    r2 = [i for i in r1 if i not in excludeOne]
    drillMult(r1, r2)

if __name__ == "__main__":

    sesh = Session(tempo = 160)
    s = sesh.new_part("soprano")
    s.play_note(68, 0, 0.5)

    #while True:
    #    drillDiv(6, 24)

    #drillMult([2, 3, 4, 5, 6], extras=[[1], [0], [10], [11]])
    #drillMult([4, 6, 7, 8, 9, 12], extras=[[11, 11], [11, 12]])
    drillTimesTablesHard([7])
    #drillTimesTables([2, 3, 4, 5])
    #drillMult([3, 4, 6, 7, 8, 9], extras=[[10, 11], [11, 11], [12, 11], [10, 12]])
    #drillMult([2, 3, 4, 5, 6], extras=[[2, 7], [2, 8], [2, 9], [3, 7], [3, 8], [3, 9], [3, 9], [3, 9], [4, 6], [4, 6], [5, 7], [5, 8], [5, 9], [11, 6], [11, 8]])
    #drillMultLowHigh(3, 12, [5, 10, 11, 7, 8, 9])
    #operation = random.choice(["addition", "subtraction", "multiplication", "division"]