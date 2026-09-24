import random
from array import *
floatArray = array("f", [])

for i in range(5):
    num = random.randint(10, 100)
    floatArray.append(num)

number = int(input("Enter a whole number from 2 to 5: "))
while number not in [2, 3, 4, 5]:
    number = int(input("Enter a whole number from 2 to 5: "))

for num in floatArray:
    print(f"{num / number:.2f}")

