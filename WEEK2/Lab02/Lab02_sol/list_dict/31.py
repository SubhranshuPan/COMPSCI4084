def func1(list1):
    newValue = int(input("enter value to add: "))
    list1.append(newValue)
    return list1

def func2(list2):
    newValue = int(input("enter value to add: "))
    newlist = list2.copy()
    newlist.append(newValue)
    return newlist

list1 = [1, 2, 3]
print(list1)
print(func2(list1))
print(func1(list1))
print(func2(list1))

