package Exercise_6;

/**
 * Problem 1(ii): Demonstrates variable shadowing.
 *
 * The constructor declares a LOCAL variable 'i' that shadows the instance field.
 * So the field 'i' remains 3, and the output is: 3
 */
public class prob1 {

    public static class A {
        public int i = 3;

        public A(int val) {
            int i = val; // local variable — does NOT modify the field 'this.i'
        }
    }

    public static void main(String[] args) {
        // System.out.println("=== Problem 1(ii) ===");
        A a = new A(5);
        System.out.println("a.i = " + a.i); // Output: 3

        // Problem 1(iii): Won't compile — double cannot be assigned to int
        // int i = 5.0;   // COMPILE ERROR: incompatible types: possible lossy conversion
        // int j = 10.0;  // COMPILE ERROR: incompatible types: possible lossy conversion

        //Problem 1(iv): Won't compile — unreachable statement after throw
        // try {
        //     throw new Exception("Hello!");
        //     System.out.println("World!"); // COMPILE ERROR: unreachable statement
        // } catch (Exception ex) {
        //     System.out.println(ex.getMessage());
        // }

        // Problem 1(v): Won't compile — B extends A, but A has no no-arg constructor
        // Class B would need: public B() { super(someInt); }
    }
}
