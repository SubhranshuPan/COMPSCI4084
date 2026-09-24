countries = ("India", "Japan", "England", "USA", "China")

user = input("Enter a country name: ")

if user in countries:
    print("Country is at index: ", countries.index(user))
else:
    print("Country not found")

user_idx = int(input("Enter an index: "))
if user_idx <= len(countries):
    print("Country at index", user_idx, "is", countries[user_idx])
else:
    print("Invalid Index")
