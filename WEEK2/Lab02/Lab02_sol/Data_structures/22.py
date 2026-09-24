import random
from array import *
numArray1 = array("i", [])
numArray2 = array("i", [])

for i in range(5):
    number = int(input(f"Enter {i+1} number: "))
    numArray1.append(number)

for i in range(5):
    num = random.randint(-1000, 1000)
    numArray2.append(num)

numArray1.extend(numArray2)

numArray1 = sorted(numArray1)

for num in numArray1:
    print(num)

    