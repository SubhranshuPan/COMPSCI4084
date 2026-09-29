again = "y"

while again == "y":
    print("Menu")

    print("1) Create a new file")
    print("2) Display the file")
    print("3) Add a new item to the file")

    sel = int(input("Enter a selection (1/2/3): "))

    if sel == 1:
        filename = input("Enter name of file to create: ")
        fout = open(filename, "w")
        sub = input("Enter a subject: ")

        fout.write(sub + "\n")
        fout.close()

    elif sel == 2:
        fout = open(filename, "r")
        line = fout.readline()

        while line != "":
            print(line)
            line = fout.readline()

        fout.close()

    elif sel == 3:
        fout = open(filename, "a")
        sub = input("Enter new subject to add: ")
        fout.write(sub + "\n")

        fout.close()
        fout = open(filename, "r")
        print(fout.read())

    else:
        print("Invalid Selection")

    again = input("Do you want to continue (y/n): ")        
