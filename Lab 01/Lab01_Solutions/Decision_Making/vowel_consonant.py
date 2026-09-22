letter = input("Enter one leter: ").lower()

if letter in "aeiou":
    print(f"{letter} is Vowel")
elif letter == "y":
    print(f"{letter} can sometimes be a vowel and sometimes a consonant")
else:
    print(f"{letter} is a Consonant")

