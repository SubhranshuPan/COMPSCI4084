import random
number = []

for i in range(4):
    num = random.randint(100, 999)
    number.append(num)

for i in range(len(number)):
    print(number[i])

user_guess = int(input("Enter a 3 digit number: "))

if user_guess in number:
    for i in range(len(number)):
        if user_guess == number[i]:
            print("Number at index", i)
else:
    print("That's not in the list")

        
