master_list = [[2, 5, 8], [3, 7, 4], [1, 6, 9], [4, 2, 0]]
print(master_list)

row = int(input(f"Row you want to display (0 to {len(master_list) - 1}): "))
col = int(input(f"Column you want to inspect (0 to {len(master_list[0]) - 1}): "))

print(master_list[row][col])

change = input("You want to change (y/n)? : ")
if change == "y":
    updated_value = int(input("Enter updated Value: "))
    master_list[row][col] = updated_value

print(master_list[row])

