a = float(input("Enter first side length: "))
b = float(input("Enter seconf side length: "))
c = float(input("Enter third side length: "))

if a == b == c:
    print("Equilateral triangle")
elif a == b or b == c or c == a:
    print("Isosceles triangle")
else:
    print("Scalene triangle")
