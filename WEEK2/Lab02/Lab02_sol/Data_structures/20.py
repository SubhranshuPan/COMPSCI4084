from array import *
numArray = array('i', [])
for i in range(5):
    num = int(input(f"Enter number {i+1}: "))
    numArray.append(num)

numArray = sorted(numArray)
numArray.reverse()
print(numArray)
