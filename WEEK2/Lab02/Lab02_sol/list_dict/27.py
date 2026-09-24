master_list = [[2, 5, 8], [3, 7, 4], [1, 6, 9], [4, 2, 0]]
print(master_list)
row = int(input(f"row number you want to display (0 to {len(master_list) - 1}): "))

print(master_list[row])

newValue = int(input("enter new value to add : "))
master_list[row].append(newValue)
print(master_list[row])