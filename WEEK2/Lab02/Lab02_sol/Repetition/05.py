compnum = 50

number = int(input("Guess a number: "))
count = 0
while number != compnum:
    if number > compnum:
        print("Too High")
    else:
        print("Too Low")
    
    number = int(input("Guess a number: "))
    count += 1

print(f"Well done, you took {count} attempts")