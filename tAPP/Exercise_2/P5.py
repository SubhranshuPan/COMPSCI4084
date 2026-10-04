import random

def pick_number():
    low = int(input("enter the bottom : "))
    high = int(input("enter the top of the range: "))
    comp_num = random.randint(low, high)
    return comp_num

def first_guess():
    print("I am thinking...")
    guess = int(input("What I am thinking ? "))
    return guess

def check_answer(comp_num, guess):
    if comp_num == guess:
        print("Correct you win!")
    
    else:
        try_again = guess
        while try_again != comp_num:
            if try_again > comp_num:
                print("too high")
            else:
                print("too low")

            try_again = int(input("Try again : "))

        print("Correct you win!")

def main():
    comp_num = pick_number()
    guess = first_guess()
    check_answer(comp_num, guess) 

main()