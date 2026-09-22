class Employee:
    company = "ABC Ltd"
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

class Manager(Employee):
    def lead_team(self):
        print(f"{self.name} is leading the team today.")

manager = Manager("Alex", 30)

manager.introduce()
manager.lead_team()

print(f"Is manager an instance of Employee? {isinstance(manager, Employee)}")
print(f"Is manager an instance of Manager? {isinstance(manager, Manager)}")

