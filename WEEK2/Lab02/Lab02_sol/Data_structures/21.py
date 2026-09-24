import random
from array import *
numArray = array('i', [])
for i in range(5):
    num = random.randint(-1000, 1000)
    numArray.append(num)

for num in numArray:
    print(num)


