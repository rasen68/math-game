import time
import os
import random

from pygame import mixer
from heap import Node, MaxHeap
from typing import Callable

class MathIO:
    def __init__(self):
        self.students = []
        self.which = 0
        dir = os.path.dirname(os.path.abspath(__file__))
        self.score = os.path.join(dir, "Untitled-score.ogg")

    def setFile(self, fileType: str):
        self.file = open(os.path.join(os.getcwd(), "tutoring-files", 
                        fileType, self.students[0] + self.students[1] + ".txt"), "a")
        
    def setOp(self, operation: Callable):
        self.operation = operation
    
    def getStudent(self):
        return self.students[self.which]

    def switch(self):
        self.which *= -1
        self.which += 1

    def setInput(self) -> int:
        self.students.append(input("Student 1? "))
        self.students.append(input("Student 2? "))
        self.opStr = ""
        valid = ["times", "timeshard", "test", "minus", "plus"]
        while self.opStr not in valid:
            self.opStr = input("Operation? ")

        if self.opStr == "test":
            self.opStr = input("Operation? ")
            return 1_234_567_890
        else:
            return random.randint(1_000_000_000, 10_000_000_000)
    
    def inputLoop(self, question: str, answer: int):
        start = time.time()
        while True:
            userAnswer = input().strip()
            if userAnswer == str(answer):
                self.file.write(userAnswer + "\n")
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

    def questionAnswer(self, i: Node):
        first = i.data[0]
        second = i.data[1]
        question = f"{self.getStudent()}: What's {first} {self.opStr} {second}?"
        answer = self.operation(first, second)

        print(question)
        self.file.write(question + "\n")
        time = self.inputLoop(question, answer)

        if time == 0: return 0
        self.win()
        self.switch()
        self.file.write(str(round(time, 2)) + "\n")
        return time

    def end(self, heap1: MaxHeap, heap2: MaxHeap):
        self.file.write(self.students[0] + ": " + str(heap1) + "\n")
        self.file.write(self.students[1] + ": " + str(heap2))
        self.file.close()
