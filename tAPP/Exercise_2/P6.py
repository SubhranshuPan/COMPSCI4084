scores = [60, 70]

def add_score_A(score):
    scores.append(score)

add_score_A(80)
print(scores)

scores = [60, 70]

def add_Score_B(scores, score):
    return scores + [score]

updated_scores = add_Score_B(scores, 80)

print(scores)
print(updated_scores)

"""Global Variable: The variable count is defined outside of any function, making it a global variable. This means a global variable can be read from functions, but assigning to it inside a function normally creates a local variable unless global is declared.

This practice is common in functional programming, which emphasises avoiding side effects to create more predictable and testable code.
avoiding side effects and making the code easier to understand and maintain
"""

