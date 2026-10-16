/**
 * Triangle (equilateral) — implements Figure.
 *
 * Perimeter = 3 * s
 * Area      = (√3 / 4) * s * s
 */
public class Triangle implements Figure {

    private double side;

    public Triangle(double side) {
        this.side = side;
    }

    @Override
    public double calculatePerimeter() {
        return 3 * side;
    }

    @Override
    public double calculateArea() {
        return (Math.sqrt(3) / 4) * side * side;
    }
}
