/**
 * Problem 2: Enumerated type with a method.
 *
 * Each enum constant (PLUS, MINUS, TIMES, DIVIDE) overrides the abstract
 * calculate() method with its own arithmetic operation.
 *
 * Usage: Operation.PLUS.calculate(2.0, 4.0) → 6.0
 */
public enum Operation {

    PLUS {
        @Override
        public double calculate(double x, double y) {
            return x + y;
        }
    },

    MINUS {
        @Override
        public double calculate(double x, double y) {
            return x - y;
        }
    },

    TIMES {
        @Override
        public double calculate(double x, double y) {
            return x * y;
        }
    },

    DIVIDE {
        @Override
        public double calculate(double x, double y) {
            return x / y;
        }
    };

    // Abstract method — every constant MUST override this
    public abstract double calculate(double x, double y);

    // Demo
    public static void main(String[] args) {
        System.out.println("=== Problem 2: Operation Enum ===");

        double a = 10.0, b = 3.0;

        System.out.printf("%.1f PLUS  %.1f = %.1f%n", a, b, Operation.PLUS.calculate(a, b));
        System.out.printf("%.1f MINUS %.1f = %.1f%n", a, b, Operation.MINUS.calculate(a, b));
        System.out.printf("%.1f TIMES %.1f = %.1f%n", a, b, Operation.TIMES.calculate(a, b));
        System.out.printf("%.1f DIVIDE %.1f = %.4f%n", a, b, Operation.DIVIDE.calculate(a, b));

        // The specific example from the exercise
        System.out.println("\nExercise example:");
        System.out.printf("Operation.PLUS.calculate(2.0, 4.0) = %.1f%n",
            Operation.PLUS.calculate(2.0, 4.0));  // 6.0
    }
}
