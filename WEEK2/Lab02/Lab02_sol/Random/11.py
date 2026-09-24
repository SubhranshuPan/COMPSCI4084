import random
num = random.randint(1, 5)
count = 0
guess = int(input("Guess the number: "))

if guess == num:
    print("Well done")
elif guess > num:
    print("Too high")
    guess = int(input("Guess the number: "))
    if guess == num:
        print("Correct")
    else:
        print("You lose")
        print(f"The number was {num}")
else:
    print("Too low")
    guess = int(input("Guess the number: "))
    if guess == num:
        print("Correct")
    else:
        print("You lose")
        print(f"The number was {num}")
        
