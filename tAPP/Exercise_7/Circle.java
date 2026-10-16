/**
 * Circle — implements Figure.
 *
 * Perimeter = 2 * π * r
 * Area      = π * r * r
 */
public class Circle implements Figure {

    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double calculatePerimeter() {
        return 2 * Math.PI * radius;
    }

    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}
