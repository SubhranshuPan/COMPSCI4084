/**
 * Problem 3 — Demo: Shows polymorphism with the Figure interface.
 *
 * All three shapes (Circle, Triangle, Rectangle) are stored as Figure
 * and the same methods are called on each — but they produce different results.
 */
public class FigureDemo {

    public static void main(String[] args) {
        System.out.println("=== Problem 3: Figure Interface Demo ===\n");

        // Create shapes — note: the variable type is Figure (the interface)
        Figure circle    = new Circle(5.0);
        Figure triangle  = new Triangle(6.0);
        Figure rectangle = new Rectangle(4.0, 7.0);

        // Polymorphism in action — same method calls, different results
        System.out.println("Circle (radius = 5.0):");
        System.out.printf("  Perimeter = %.2f%n", circle.calculatePerimeter());
        System.out.printf("  Area      = %.2f%n", circle.calculateArea());

        System.out.println("\nEquilateral Triangle (side = 6.0):");
        System.out.printf("  Perimeter = %.2f%n", triangle.calculatePerimeter());
        System.out.printf("  Area      = %.2f%n", triangle.calculateArea());

        System.out.println("\nRectangle (width = 4.0, height = 7.0):");
        System.out.printf("  Perimeter = %.2f%n", rectangle.calculatePerimeter());
        System.out.printf("  Area      = %.2f%n", rectangle.calculateArea());

        // Demonstrate treating them all the same in a loop
        System.out.println("\n--- All shapes in a loop (polymorphism) ---");
        Figure[] shapes = { circle, triangle, rectangle };
        for (Figure shape : shapes) {
            System.out.printf("%s → Area = %.2f%n",
                shape.getClass().getSimpleName(), shape.calculateArea());
        }
    }
}
