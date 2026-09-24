food = {}

for i in range(1, 5):
    fav = input("Enter fav food: ")
    food[i] = fav

print("List of food are: ")
print(food)

rem = int(input("Enter which key you want to remove: "))
if rem in food:
    del food[rem]
    print(food)
else:
    print("That key doesn't exist!")

print(sorted(food.values()))