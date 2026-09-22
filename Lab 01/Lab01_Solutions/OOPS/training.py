class Employee:
    def __init__(self, name, score, active):
        self.name = name
        self.score = score
        self.active = active

    def eligible_for_training(self):
        return self.active and self.score >= 70


employees = [
    Employee("Maya", 75, True), # eligible
    Employee("Tom", 40, True), # low score 
    Employee("Preeti", 90, False), # high score but active = False
    Employee("Som", 70, True), # boundary case
    Employee("Manas", 69, False) # low score and not active
]

for emp in employees:
    if emp.eligible_for_training():
        print(f"{emp.name} is eligible for training.")
    else:
        print(f"{emp.name} is NOT eligible for training.")



