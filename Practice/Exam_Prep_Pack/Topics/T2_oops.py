# class Book:
#     def __init__(self, title, author, year):
#         self.title = title
#         self.author = author
#         self.year = year

#     @property
#     def title(self):
#         return self._title
    
#     @title.setter
#     def title(self, value):
#         if not isinstance(value, str) or not value.strip():
#             raise ValueError("Title cannot be empty")
#         self._title = value.strip()

#     @property
#     def author(self):
#         return self._author

#     @author.setter
#     def author(self, value):
#         if not isinstance(value, str) or not value.strip():
#             raise ValueError("Author cannot be empty")
#         self._author = value.strip()

#     @property 
#     def year(self):
#         return self._year

    
#     @year.setter
#     def year(self, value):
#         if not isinstance(value, int) or not 1450 <= value <= 2025:
#             raise ValueError("Year must be between 1450 and 2025")
#         self._year = value

#     def __str__(self):
#         return f"{self.title}, {self.year}"

#     def __repr__(self):
#         return f"Book('{self.title}', '{self.author}', {self.year})"


# b1 = Book("Harry Potter and Chamber of Secrets", "J.K. Rowling", 1998)
# b2 = Book("Harry Potter and Deathly Hallows Part 2", "J.K. Rowling", 2014)

# print(b1)
# print(b2)

# try:
#     b1.year = 1449
# except ValueError as e:
#     print("Rejected: ", e)

# print(b1.year)

# try:
#     Book("", "J.K. Rowling", "2020")
# except ValueError as e:
#     print("Rejected: ", e)

# class Employee:                               # parent (kept short here)
#     def __init__(self, name, score, active=True):
#         self.name = name
#         self.score = score
#         self.active = active
#     def report(self):
#         print(f"{self.name} : {self.score}")

# class Manager(Employee):                      # child: Manager IS-A Employee
#     def __init__(self, name, score, active=True, team=None):
#         super().__init__(name, score, active) # parent sets name/score/active
#         self.team = team if team is not None else []   # extra attribute

#     def lead_team(self):                      # new method
#         print(f"{self.name} is leading {len(self.team)} people")

#     def report(self):                         # OVERRIDE the parent's method
#         super().report()                      # reuse it, then add more
#         print(f"Team Size : {len(self.team)}")

# boss = Manager("Zhong", 80, True, ["Som", "Adi"])
# worker = Employee("Nidhi", 100)
# for person in [boss, worker]:                 # same call, different behaviour
#     person.report()
# boss.lead_team()
# print(isinstance(boss, Employee), isinstance(boss, Manager))      # True True
# print(isinstance(worker, Manager))                                # False

# people = [Employee("Zhong", 80), Employee("Nidhi", 100),
#           Employee("Som", 71, False), Employee("Adi", 69)]

# for p in people:
#     if p.eligible_for_training():
#         print(p.name, "eligible")
#         count += 1
#     else:
#         print(p.name, "not eligible")
# print(count, "eligible")

# class Library:
#     def __init__(self):
#         self.books = []

#     def add_book(self, book):
#         if not isinstance(book, Book):
#             raise ValueError("Only Book Objects can be added")
#         self.books.append(book)

#     def find_by_author(self, author):
#         return [b for b in self.books if b.author == author]

#     def remove_book(self, title):
#         for b in self.books:
#             if b.title == title:
#                 self.books.remove(b)
#                 return
#         raise ValueError("Book not found")
    
#     def total_books(self):
#         return len(self.books)


# lib = Library()
# lib.add_book(Book("LOTR", "Tolkien", 1954))
# lib.add_book(Book("Moby Dick", "Tolkien", 1851))
# lib.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925))

# print("Books by Tolkien:", lib.find_by_author("Tolkien"))
# print("Total books before removal:", lib.total_books())

# lib.remove_book("LOTR")
# print("Total books after removing LOTR:", lib.total_books())

# # Testing absent book:
# try:
#     lib.remove_book("Nonexistent Book")
# except ValueError as e:
#     print("Caught expected error:", e)


from torch._dynamo import exc
from yaml import ValueToken
class Animal:
    SIZES = ["small", "medium", "large"]

    def __init__(self, name, size, low, high):
        self.name = name
        self.size = size
        self.set_comfort_range(low, high)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 3:
            raise ValueError("Name must be string and atleast 3 characters")
        self._name = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value not in Animal.SIZES:
            raise ValueError(f"Size must be one of {Animal.SIZES}")
        self._size = value

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    def set_comfort_range(self, low, high):
        if not (0 <= low <= high <= 50):
            raise ValueError("Need 0 <= low <= high <= 50.")
        self._low = low
        self._high = high

    def __str__(self):
        return f"{self.name} ({self.size}, comfortable {self.low} - {self.high})"

    def __eq__(self, other):
        return (isinstance(other, Animal) and self.name == other.name and self.size == other.size)

    def __hash__(self):
        return hash((self.name, self.size))



rex = Animal("Rex", "large", 5, 30)
print(rex)

print(rex == Animal("Rex", "large", 0, 10)) # ignores range

for bad in [("Al", "small", 0, 10), ("Kit", "tiny", 0, 10),
            ("Kit", "small", 20, 10), ("Kit", "small", 0, 60)]:
    try:
        Animal(*bad)

    except ValueError as e:
        print("Rejected: ", e)

try:
    rex.set_comfort_range(40, 10)
except ValueError as e:
    print("Rejected: ", e)

