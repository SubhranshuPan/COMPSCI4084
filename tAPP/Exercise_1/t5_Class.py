class Employee:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def report(self):
        print(f"{self.name} : {self.score}")

emp1 = Employee("Som", 80)
emp2 = Employee("Nidhi", 100)

emp1.report()
emp2.report()

