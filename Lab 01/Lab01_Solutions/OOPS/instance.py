class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

emp1 = Employee("Maya", 23)
emp2 = Employee("Jane", 40)

emp1.introduce()
emp2.introduce()