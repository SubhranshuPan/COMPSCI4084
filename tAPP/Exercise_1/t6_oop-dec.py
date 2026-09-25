class Employee:
    def __init__(self, name, score, active):
        self.name = name
        self.score = score
        self.active = active

    def report(self):
        print(f"{self.name} : {self.score}")

    def eligible_for_training(self):
        return self.active and self.score >= 70

emp1 = Employee("Som", 80, True)
emp2 = Employee("Nidhi", 100, False)
emp3 = Employee("Adi", 60, True)

for emp in [emp1, emp2, emp3]:
    if emp.eligible_for_training():
        print(f"{emp.name} is eligible!")
    else:
        print(f"{emp.name} not eligible for training")





