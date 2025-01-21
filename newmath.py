import random
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

def inputLoop(question, answer, queue, file):
    while True:
        userAnswer = input()
        if userAnswer == str(answer):
            file.write(userAnswer + "\n")
            break
        elif userAnswer == "print":
            print(queue)
            continue
        elif userAnswer == "":
            continue
        elif userAnswer == "end":
            return 0
        else:
            file.write(userAnswer + "\n")
            print("Not quite! Try again")
            print()
            print(question)

def multQuestionAnswer(i, queue, student, file):
    i = list(i)
    question = f"{student}: What's {i[0]} times {i[1]}?"
    answer = i[0] * i[1]

    start = time.time()
    print(question)
    file.write(question + "\n")

    if inputLoop(question, answer, queue, file) == 0:
        return 0
    
    end = time.time()
    print("Good job!")
    print()
    mixer.init()
    mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + "\\Untitled-score.ogg")
    mixer.music.play()

    file.write(str(round(end - start, 2)) + "\n")
    return end - start

def enqueue(queue, question):
    question = (round(question[0], 2), question[1])
    index = 0
    while index < len(queue):
        if queue[index][0] < question[0]:
            queue.insert(index, question)
            break
        else:
            index += 1
    else:
        queue.insert(index, question)

def pretest(student1, student2, allNums, file):
    shuffled = [i for i in allNums]
    random.shuffle(shuffled)
    last3 = [(0, 0), (0, 0), (0, 0)]
    queue = []
    whichstudent = student1

    for i in shuffled:
        t = multQuestionAnswer(i, [], whichstudent, file)
        #print(f"{t:.2f}")
        enqueue(queue, (t, i)) 
        last3.pop(0)
        last3.append(i)
        whichstudent = student1 if whichstudent==student2 else student2
    return queue, last3 

def makeQuestions(allNums, student1, student2, file):
    queue1, last3 = pretest(student1, student2, allNums, file)
    queue2 = [i for i in queue1]
    whichstudent = student1 if len(allNums)%2==0 else student2
    whichqueue = queue1 if len(allNums)%2==0 else queue2
    
    while True:
        # find question
        for i in range(3):
            if queue1[i][1] not in last3:
                question = whichqueue.pop(i)
                break
        else:
            question = whichqueue.pop(3)

        # process question
        last3.pop(0)
        last3.append(question[1])
        t2 = multQuestionAnswer(question[1], whichqueue, whichstudent, file) 
        if t2 == 0:
            break
        elif (t2 * 2 + question[0]) / 3 > 30:
            average = 30
        else:
            average = (t2 * 2 + question[0]) / 3
        question = (average, question[1])
        enqueue(whichqueue, question)

        # +1 second to random question in queue
        rand = whichqueue.pop(random.randint(1, len(whichqueue) - 1))
        rand = (rand[0] + 1, rand[1])
        enqueue(whichqueue, rand)
        whichstudent = student1 if whichstudent==student2 else student2
        whichqueue = queue1 if whichqueue==queue2 else queue2

    file.write(student1 + ": " + str(queue1))
    file.write(student2 + ": " + str(queue2))
    file.close()
                     
def drillMult(student1, student2, file, num1s, num2s = None, extras = None):
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
    
    makeQuestions(allNums, student1, student2, file)

def drillTimesTables(nums, student1, student2, file):
    lis = list(range(2, 13))
    drillMult(student1, student2, file, nums, lis)

def drillTimesTablesHard(nums, student1, student2, file):
    extras = []
    lis = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append([12, 10])
        extras.append([12, 11])
    if 11 in nums:
        extras.append([11, 10])
        extras.append([11, 11])
    drillMult(student1, student2, file, nums, lis, extras)

if __name__ == "__main__":
    student1 = input("Student 1? ")
    student2 = input("Student 2? ")
    tables = input("Times tables? ").split()
    tables = [int(i) for i in tables]
    file = open(os.getcwd() + "\\tutoring-files\\" + student1 + student2 + ".txt", "a")
    drillTimesTables(tables, student1, student2, file)
    