class Employee:
    company = "ABC Ltd"
    def __init__(self, name, age):
        self.name = name
        self.age = age

emp1 = Employee("John", 30)
emp2 = Employee("Som", 22)

print(f"{emp1.name}, {emp1.age}, {emp1.company}")
print(f"{emp2.name}, {emp2.age}, {emp2.company}")