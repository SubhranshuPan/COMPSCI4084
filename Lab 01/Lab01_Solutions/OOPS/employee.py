class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def display(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")

e1 = Employee("John", 55)
e2 = Employee("Marie", 30)

e1.display()
e2.display()