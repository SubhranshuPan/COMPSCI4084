import csv
print("Menu")
print("1) Add to file")
print("2) View all records")
print("3) Quit programme")

choice = int(input("Enter number of your selection: "))

while choice != 3:
    if choice == 1:
        with open("Salaries.csv", "a", newline="") as f:
            writer = csv.writer(f)
            name = input("Enter name: ")
            salary = int(input("Enter Salary: "))
            writer.writerow([name, salary])

    elif choice == 2:
        with open("Salaries.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    else:
        print("Enter a valid choice.")

    print("Menu")
    print("1) Add to file")
    print("2) View all records")
    print("3) Quit programme")

    choice = int(input("Enter number of your selection: "))

