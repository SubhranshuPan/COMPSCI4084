class Employee:
    def __init__(self, name, score, active):
        self.name = name
        self.score = score
        self.active = active

    def report(self):
        print(f"{self.name} : {self.score}")

    def eligible_for_training(self):
        return self.active and self.score >= 70

class Manager(Employee):
    def lead_team(self):
        print(f"{self.name} is leading the team")

emp1 = Manager("Zhong", 80, True)
emp2 = Employee("Nidhi", 100, True)
emp3 = Employee("Som", 71, False)
emp4 = Employee("Adi", 69, True)

for emp in [emp1, emp2, emp3, emp4]:
    emp.report()
    if emp.eligible_for_training():
        print(f"{emp.name} is eligible for training")
    else:
        print(f"{emp.name} is not eligible for training")

print("Whether object is instance? :", isinstance(emp1, Employee))
print("Whether object is instance? :", isinstance(emp1, Manager))
print("whether Nidhi is instance? :", isinstance(emp2, Manager))


