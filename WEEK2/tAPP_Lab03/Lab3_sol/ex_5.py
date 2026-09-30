curr_sum = 0
num = input("Enter a number (or press Enter to quit): ")

while num != "":
    try:
        curr_sum += float(num)
        print(f"Current Sum: {curr_sum}")
        num = input("Enter a number (or press Enter to quit): ")
    except ValueError:
        print(f"Invalid input. Current Sum: {curr_sum}")
        num = input("Enter a number (or press Enter to quit): ")

print(f"The final sum is {curr_sum:.5f}")

