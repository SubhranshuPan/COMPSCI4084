def add_name(user_list):
    name = input("Enter name to be added: ")
    user_list.append(name)
    return user_list

def del_name(user_list):
    name = input("Enter name to be removed: ")
    if name in user_list:
        user_list.remove(name)
    else:
        print("Name not in list")
    
    return user_list

def view_names(user_list):
    if len(user_list)== 0:
        print("Empty list")

    print("User list of names: \n")
    for name in user_list:
        print(name)

    print("-" * 10)
    

def main():
    user_list = []
    while True:
        print("\nMenu:\n 1. Add name\n 2. Remove a name\n 3. View all names\n 4. End program\n")
        choice = int(input("Enter choice (1-4): "))

        if choice == 1:
            user_list = add_name(user_list)
            view_names(user_list)
        
        elif choice == 2:
            user_list = del_name(user_list)
            view_names(user_list)
        
        elif choice == 3:
            view_names(user_list)
        
        elif choice == 4:
            print("Thank you for using the name program!")
            break

        else:
            print("Invalid choice. Please try again")

if __name__ == "__main__":
    main()  