answer = input("Whether it is raining: ").lower()

if answer == "yes":
    if input("Whether it is windy: ").lower() == "yes":
        print("It's too windy for an umbrella.")
    else:
        print("Take an umbrella")
else:
    print("Enjoy your day.")
