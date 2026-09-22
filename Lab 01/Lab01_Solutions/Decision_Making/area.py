selection = int(input("1) Sqaure \n2) Triangle\nEnter your Choice (1 or 2): "))

if selection == 1:
    side_length = float(input("Enter side length of sqaure: "))
    area = side_length * side_length
    print(f"Area of sqaure: {area:.2f}")

elif selection == 2:
    base = float(input("Enter base length of triangle: "))
    height = float(input("Enter height of triangle: "))
    area = 0.5 * base * height
    print(f"Area of triangle: {area:.2f}")

else:
    print("Error: Invalid selection. Please enter 1 or 2.")
