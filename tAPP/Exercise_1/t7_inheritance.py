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

emp1 = Manager("Som", 80, True)
emp1.report()
emp1.lead_team()

emp2 = Employee("Nidhi", 100, True)



print("Whether object is instance? :", isinstance(emp1, Employee))
print("Whether object is instance? :", isinstance(emp1, Manager))
print("whether Nidhi is instance? :", isinstance(emp2, Manager))


