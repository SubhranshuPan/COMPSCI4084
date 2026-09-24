num = 10

while num > 0:
    print(num)
    num -= 1
    answer = int(input("How many remaining: "))
    while answer != num:
        print("No, try again")
        answer = int(input("How many remaining: "))

print("There are no more green bottles hanging on the wall")
