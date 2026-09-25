status = input("Enter your status: ").lower()
score = int(input("Enter your score: "))

if status == "active" and score >= 70:
    print("Eligible for training")
else:
    print("Not eligible for training")


