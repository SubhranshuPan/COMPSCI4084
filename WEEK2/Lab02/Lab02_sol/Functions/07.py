def func():
    num = int(input("Enter a number: "))
    return num

def func2(num):
    for i in range(1, num + 1):
        print(i)

num = func()
func2(num)
