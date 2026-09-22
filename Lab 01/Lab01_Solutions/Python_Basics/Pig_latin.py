Vowels = "aeiou"
word = input("Enter one word: ").lower()

if word[0] in Vowels:
    pig_latin_word = word + "way"
else:
    pig_latin_word = word[1:] + word[0] + "ay"

print(pig_latin_word)
