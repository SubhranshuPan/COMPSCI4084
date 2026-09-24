import random
from array import *

numArray = array("i", [])

for i in range(5):
    num = random.randint(0,100)
    numArray.append(num)

print(numArray)

select = int(input("Enter a value : "))

while select not in numArray:
    print("Invalid Index")
    select = int(input("Enter a value: "))
    
print("Index of values is : ", numArray.index(select))