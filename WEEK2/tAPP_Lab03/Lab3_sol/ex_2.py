import random
import csv

def generate_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(['+', '-', '*'])

    question = f"{num1} {operator} {num2}"

    if operator == '+':
        correct_answer = num1 + num2
    elif operator == '-':
        correct_answer = num1 - num2
    else:
        correct_answer = num1 * num2

    return question, correct_answer

def run_quiz():

    name = input("Enter your name: ")
    score = 0
    questions = []
    answers = []

    for i in range(1, 3):
        question, correct_answer = generate_question()
        print(f"Question {i}: {question} ?")

        user_answer = int(input("Your Answer: "))
        questions.append(question)
        answers.append(user_answer)

        if user_answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {correct_answer}")

    print(f"Final score of {name} is {score} / 2.")

    try:
        with open("results.csv", "r"):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open("results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Question 1", "Answer 1", "Question 2", "Answer 2", "Score"])

        writer.writerow([name, questions[0], answers[0], questions[1], answers[1], f"{score}/2"])

        
if __name__ == "__main__":
    run_quiz()
