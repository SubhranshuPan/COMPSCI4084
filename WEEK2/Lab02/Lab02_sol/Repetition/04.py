num1 = int(input("Enter First number: "))
num2 = int(input("Enter second number: "))

total = num1 + num2

while True:
    choice = input("Add another number? (y/n): ")
    if choice == "y":
        num = int(input("Enter the other number to add: "))
        total += num
    else:
        break

print("Final Total:",total)
