import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import random

from pygame import mixer
from heap import MaxHeap
from typing import Callable, Tuple

def strip(original: str) -> str:
    i = 0
    new = original
    while i < len(new):
        if not new[i].isdigit():
            new = new[:i] if i == len(new) - 1 else new[:i] + new[i+1:] 
        else:
            i+=1
    print(new)
    return new

class MathIO:
    def __init__(self):
        self.students = []
        self.which = 0
        dir = os.path.dirname(os.path.abspath(__file__))
        self.score = os.path.join(dir, "Untitled-score.ogg")

    def setFile(self, fileType: str):
        if len(self.students) == 1:
            name = self.students[0] + ".txt"
        else:
            name = self.students[0] + self.students[1] + ".txt"
        self.file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      "tutoring-files", fileType, name), "a")
        
    def setOp(self, operation: Callable):
        self.operation = operation
    
    def getStudent(self):
        return self.students[self.which]

    def switch(self):
        self.which *= -1
        self.which += 1

    def setInput(self) -> int:
        self.students.append(input("Student 1? "))
        if self.students[0] != "1p":
            self.students.append(input("Student 2? "))
        self.opStr = ""
        valid = ["times", "timeshard", "test", "minus", "plus", "letter"]
        while self.opStr not in valid:
            self.opStr = input("Operation? ")

        if self.opStr == "test":
            self.opStr = input("Operation? ")
            self.seed = 1_234_567_890
        else:
            self.seed = random.randint(1_000_000_000, 10_000_000_000)
        
        self.setFile(self.opStr)

    def inputLoop(self, question: str, answer: int):
        start = time.time()
        while True:
            userAnswer = input().strip()
            if strip(userAnswer) == str(answer):
                self.file.write(userAnswer + "\n")
                return time.time() - start
            elif userAnswer == "end":
                return 0
            elif userAnswer == "":
                continue
            elif userAnswer == "`":
                return time.time() - start
            elif userAnswer == "unpause":
                start = time.time()
            elif userAnswer[:5] == "wait ":
                start -= int(userAnswer[5:])
            else:
                self.file.write(userAnswer + "\n")
                print("Not quite! Try again")
                print()
                print(question)

    def win(self):
        print("Good job!")
        print()
        mixer.init()
        mixer.music.load(self.score)
        mixer.music.play()

    def questionAnswer(self, i: Tuple[int, int]):
        first = i[0]
        second = i[1]
        if len(self.students) > 1:
            question = f"{self.getStudent()}: What's {first} {self.opStr} {second}?"
        else: 
            question = f"What's {first} {self.opStr} {second}?"
        answer = self.operation(first, second)

        print(question)
        self.file.write(question + "\n")
        time = self.inputLoop(question, answer)

        if time == 0: return 0
        self.win()
        if len(self.students) > 1:
            self.switch()
        self.file.write(str(round(time, 2)) + "\n")
        return time

    def end(self, heap1: MaxHeap, heap2: MaxHeap):
        self.file.write(self.students[0] + ": " + str(heap1) + "\n")
        if len(self.students) > 1:
            self.file.write(self.students[1] + ": " + str(heap2) + "\n")
        self.file.write("\n")
        self.file.close()
