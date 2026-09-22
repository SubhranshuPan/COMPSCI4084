isRaining = input("Is it raining (yes/no): ").lower()

if isRaining == "yes":
    isWindy = input("Is it windy (yes/no): ").lower()
    if isWindy == "yes":
        print("It's too windy for an umbrella")
    else:
        print("Take an umbrella")
else:
    print("Enjoy your day")