import csv
print("Menu")
print("1) Add to file")
print("2) View all records")
print("3) Delete a record")
print("4) Quit programme")

choice = int(input("Enter number of your selection: "))

while choice != 4:
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

    elif choice == 3:
        temp = []
        with open("Salaries.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                temp.append(row)
            print(temp)
            
        name = input("Enter the name of employee to delete: ")
        found = False
        for i in temp:
            if i[0] == name:
                temp.remove(i)
                found = True
                break
        
        if found == False:
            print("Record not found.")

        with open("Salaries.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i in temp:
                writer.writerow(i)
        print("Deletion completed")

    else:
        print("Enter a valid choice.")

    print("Menu")
    print("1) Add to file")
    print("2) View all records")
    print("3) Delete a record")
    print("4) Quit programme")

    choice = int(input("Enter number of your selection: "))

