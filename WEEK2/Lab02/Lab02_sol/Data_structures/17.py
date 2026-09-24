names = []
for i in range(3):
    names.append(input(f"Enter {i+1} name: "))

user_input = input("Continue adding names (yes/no): ")
while user_input != "no":
    names.append(input("Enter the name to be added: "))
    
    user_input = input("Continue adding the names (yes/no): ")

print("Number of people invited:", len(names))
