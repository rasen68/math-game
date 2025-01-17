import random
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

def multQuestionAnswer(i, queue, file):
    i = list(i)
    question = f"What's {i[0]} times {i[1]}?"
    answer = i[0] * i[1]

    start = time.time()
    print(question)
    file.write(question + "\n")
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
    end = time.time()
    print("Good job!")
    print()
    mixer.init()
    mixer.music.load("C:\\Users\\Rasen\\Downloads\\Untitled-score.ogg")
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

def pretest(allNums, file):
    shuffled = [i for i in allNums]
    random.shuffle(shuffled)
    last3 = [(0, 0), (0, 0), (0, 0)]
    queue = []

    for i in shuffled:
        t = multQuestionAnswer(i, [], file)
        #print(f"{t:.2f}")
        enqueue(queue, (t, i)) 
        last3.pop(0)
        last3.append(i)
    return queue, last3    

def makeQuestions(allNums, file):
    queue, last3 = pretest(allNums, file)
    
    while True:
        # find question
        for i in range(3):
            if queue[i][1] not in last3:
                question = queue.pop(i)
                break
        else:
            question = queue.pop(3)

        # process question
        last3.pop(0)
        last3.append(question[1])
        t2 = multQuestionAnswer(question[1], queue, file) 
        if t2 == 0:
            break
        elif (t2 * 2 + question[0]) / 3 > 30:
            average = 30
        else:
            average = (t2 * 2 + question[0]) / 3
        question = (average, question[1])
        enqueue(queue, question)

        # +1 second to random question in queue
        rand = queue.pop(random.randint(1, len(queue) - 1))
        rand = (rand[0] + 1, rand[1])
        enqueue(queue, rand)
    file.write(str(queue))
    file.close()
                     
def drillMult(file, num1s, num2s = None, extras = None):
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
    
    makeQuestions(allNums, file)

def drillTimesTables(nums, file):
    list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    drillMult(file, nums, list)

def drillTimesTablesHard(nums, file):
    extras = []
    list = [3, 4, 6, 7, 8, 9, 12]
    if 12 in nums:
        extras.append([12, 10])
        extras.append([12, 11])
    if 11 in nums:
        extras.append([11, 10])
        extras.append([11, 11])
    drillMult(file, nums, list, extras)

if __name__ == "__main__":
    file = open("C:\\Users\\Rasen\\Downloads\\program\\aldan files\\" + input(), "a")
    drillTimesTables([9], file)
    