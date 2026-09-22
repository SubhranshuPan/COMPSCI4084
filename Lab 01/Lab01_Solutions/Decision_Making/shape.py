sides = int(input("Enter number of sides: "))

shape_names = {
    3: "Triangle",
    4: "Rectangle",
    5: "Pentagon",
    6: "Hexagon",
    7: "Heptagon",
    8: "Octagon",
    9: "Nonagon",
    10: "Decagon"
}

if sides in shape_names:
    print(f"A polygon with {sides} is called {shape_names[sides]}.")
else:
    print(f"Error: Number of sides {sides} should be in range 3 to 10.")