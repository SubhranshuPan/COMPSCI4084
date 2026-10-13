import java.util.Scanner;

public class InputTest {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Java Input/Output Test ===");
        System.out.println();

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();

        System.out.println();
        System.out.println("✅ Hello " + name + "! You are " + age + " years old.");
        System.out.println("🎉 Your setup is working perfectly!");

        scanner.close();
    }
}
