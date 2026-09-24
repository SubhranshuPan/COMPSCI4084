master_list = [[2, 5, 8], [3, 7, 4], [1, 6, 9], [4, 2, 0]]

print(master_list)

row_idx = int(input("Enter a row index: "))
col_idx = int(input("Enter a col index: "))

if 0 <= row_idx <= len(master_list) - 1 and 0 <= col_idx <= len(master_list[0]) - 1:
    print(master_list[row_idx][col_idx])

else:
    print("Invalid index input")
