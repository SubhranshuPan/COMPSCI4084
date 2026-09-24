import random
coin = ["H", "T"]
choice = random.choice(coin)

user_choice = input("Enter your choice (H/T): ")

if user_choice == choice:
    print("You win")
else:
    print("Bad luck")

print(f"Computer choose {choice}")

