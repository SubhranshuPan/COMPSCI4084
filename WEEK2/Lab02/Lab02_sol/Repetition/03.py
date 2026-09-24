direction = input("Enter direction for count (up/down): ")

if direction == "up":
    top_num = int(input("Enter the top number: "))
    for i in range(1, top_num + 1):
        print(i)

elif direction == "down":
    bottom_num = int(input("Enter a number below 20: "))
    for i in range(20, bottom_num - 1, -1):
        print(i)

else:
    print("I don't understand")
