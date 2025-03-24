import sys
import newmath 
import os

if __name__ == '__main__':
    dir = os.path.dirname(os.path.abspath(__file__))

    input = open(os.path.join(dir, "pretestOrderInput.txt"), "r")
    output = open(os.path.join(dir, "pretestOrderOutput.txt"), "w")
    expected = open(os.path.join(dir, "pretestOrderExpected.txt"), "r")

    sys.stdin = input
    sys.stdout = output
    newmath.main()
    sys.stdout = sys.__stdout__
    actual = open(os.path.join(dir, "pretestOrderOutput.txt"), "r")
    passed = True

    a = actual.readlines()
    x = expected.readlines()
    if len(a) != len(x):
        print(f"ACTUAL LENGTH: {len(a)}\nEXPECTED LENGTH: {len(x)}")
        passed = False

    for line in zip(a, x):
        if line[0] != line[1]:
            print(f"ACTUAL: {line[0]}EXPECTED: {line[1]}")
            passed = False
    
    if passed:
        print("OK")

    input.close()
    actual.close()
    expected.close()
    