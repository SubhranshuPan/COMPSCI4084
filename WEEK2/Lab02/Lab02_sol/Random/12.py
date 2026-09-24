import random
colors = ["red", "blue", "green", "black", "violet"]
choice = random.choice(colors)
print(colors)
user_guess = input("guess the color: ")

while user_guess != choice:
    for i in range(len(colors)):
        if colors[i] == choice:
            print(f"the color is at position {i} in the list {colors}")
    user_guess = input("guess the color: ")

print("Well done")

