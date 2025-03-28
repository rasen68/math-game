from typing import List, Tuple

def hash(nums: Tuple[int, int]) -> int:
    return nums[0] + 31*nums[1]

class NumsDict:
    def __init__(self):
        self.dict = {}

    def checkHash(self, tup: Tuple[int, int]) -> bool:
        sortedTup = (tup[1], tup[0]) if tup[0] > tup[1] else tup
        key = hash(sortedTup)
        if key not in self.dict:
            self.dict[key] = [sortedTup]
            return True
        elif sortedTup not in self.dict[key]:
            self.dict[key].append(sortedTup)
            return True
        return False

    def makeQuestions(self, num1s: List[int], num2s: List[int] = None, 
                    extras: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        if not num2s:
            num2s = num1s
        allNums = []

        for num1 in num1s:
            for num2 in num2s:
                if self.checkHash((num1, num2)):
                    allNums.append((num1, num2))
        
        if extras:
            for x in extras:
                if self.checkHash(x):
                    allNums.append(x)

        return allNums