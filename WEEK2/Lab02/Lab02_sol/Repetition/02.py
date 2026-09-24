total = 0

for i in range(5):
    number = int(input(f"Enter number {i+1}: "))
    choice = input("Add number to total? (y/n): ")
    if choice == "y":
        total += number
    
print("Final Total: ",total)
    