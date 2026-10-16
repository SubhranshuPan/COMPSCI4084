/**
 * Rectangle — implements Figure.
 *
 * Perimeter = 2 * (w + h)
 * Area      = w * h
 */
public class Rectangle implements Figure {

    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double calculatePerimeter() {
        return 2 * (width + height);
    }

    @Override
    public double calculateArea() {
        return width * height;
    }
}
