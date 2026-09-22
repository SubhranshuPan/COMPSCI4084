first_name = input("Enter your first name: ")
if len(first_name) < 5:
    surnname = input("Enter your surname: ")
    full_name = first_name + " " + surnname
    print(full_name.upper())
else:
    print(first_name.lower())