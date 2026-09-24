from array import *

jhaant = array("i", [])

for i in range(5):
    num = int(input("Enter a number: "))
    jhaant.append(num)

jhaant = sorted(jhaant)
print(jhaant)

newJhaant = array("i", [])
select = int(input("Select one of the values: "))
if select in jhaant:
    jhaant.remove(select)
    newJhaant.append(select)
else:
    print("Value not found")

print(jhaant)
print(newJhaant)
