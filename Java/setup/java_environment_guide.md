# ☕ Professional Java Environment — Setup & Fundamentals Guide

---

## 1. Your Environment Status

| Component | Status | Details |
|---|---|---|
| **JDK** | ✅ Installed | OpenJDK 17.0.20.1 (Eclipse Temurin) |
| **`java` compiler** | ✅ Available | `javac 17.0.20.1` at `/usr/bin/javac` |
| **`java` runtime** | ✅ Available | `/usr/bin/java` |
| **JDK Location** | ✅ Found | `/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home` |
| **`JAVA_HOME`** | ✅ Now Set | Added to `~/.zshrc` (was missing before) |
| **VS Code Extension** | ✅ Installed | Extension Pack for Java |

> [!IMPORTANT]
> `JAVA_HOME` was **not set** in your shell profile. I've added it to your `~/.zshrc`. Restart your terminal or run `source ~/.zshrc` to apply.

---

## 2. How to Run Java Files (Terminal Commands)

### The Two-Step Classic (Compile → Run)

```bash
# Step 1: Compile — creates Hello.class (bytecode)
javac Hello.java

# Step 2: Run — executes the bytecode
java Hello
```

> [!NOTE]
> When running with `java`, you use the **class name** (no `.java` or `.class` extension).

### One-Liner (Java 11+)

Since you have JDK 17, you can run single-file programs directly:

```bash
# Compiles and runs in one step — no .class file created
java Hello.java
```

### Quick Reference Table

| Goal | Command |
|---|---|
| Compile a file | `javac MyFile.java` |
| Run a compiled class | `java MyFile` |
| Compile + run in one step | `java MyFile.java` |
| Compile multiple files | `javac *.java` |
| Run with arguments | `java MyFile arg1 arg2` |
| Check Java version | `java -version` |
| Check compiler version | `javac -version` |
| See JDK location | `/usr/libexec/java_home` |

---

## 3. Java Project Structure Best Practices

For a clean professional setup, organize your workspace like this:

```
Documents/Java/
├── basics/              ← Fundamentals practice
│   ├── HelloWorld.java
│   ├── Variables.java
│   └── DataTypes.java
├── oop/                 ← Object-Oriented concepts
│   ├── Animal.java
│   ├── Dog.java
│   └── Main.java
├── projects/            ← Larger projects
│   └── calculator/
│       ├── Calculator.java
│       └── Main.java
└── README.md
```

---

## 4. Java Fundamentals

### 4.1 — The Anatomy of a Java Program

```java
// Every Java program needs a class with the SAME name as the file
public class Hello {

    // main() is the entry point — Java starts here
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

**Key Rules:**
- File name **must match** the public class name → `Hello.java` contains `public class Hello`
- Every statement ends with a **semicolon** `;`
- Code blocks use **curly braces** `{ }`
- Java is **case-sensitive** → `String` ≠ `string`

---

### 4.2 — Variables & Data Types

```java
public class Variables {
    public static void main(String[] args) {

        // === PRIMITIVE DATA TYPES (stored directly in memory) ===
        int age = 21;                  // Whole numbers
        double price = 19.99;          // Decimal numbers
        float gpa = 3.5f;             // Smaller decimal (needs 'f' suffix)
        long bigNumber = 9999999999L; // Large whole numbers (needs 'L')
        char grade = 'A';             // Single character (single quotes)
        boolean isStudent = true;      // true or false
        byte smallNum = 127;           // -128 to 127
        short mediumNum = 32000;       // -32,768 to 32,767

        // === REFERENCE TYPES (stored as references to objects) ===
        String name = "Brave Wolf";    // Text (double quotes)
        int[] numbers = {1, 2, 3};     // Array

        // === PRINTING ===
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Price: " + price);
        System.out.println("Student: " + isStudent);

        // === CONSTANTS (cannot be changed) ===
        final double PI = 3.14159;
        // PI = 3.14;  ← This would cause a compile error!
    }
}
```

| Type | Size | Range / Example |
|---|---|---|
| `byte` | 1 byte | -128 to 127 |
| `short` | 2 bytes | -32,768 to 32,767 |
| `int` | 4 bytes | ~±2 billion |
| `long` | 8 bytes | Very large numbers |
| `float` | 4 bytes | ~7 decimal digits |
| `double` | 8 bytes | ~15 decimal digits |
| `char` | 2 bytes | Single Unicode character |
| `boolean` | 1 bit | `true` or `false` |

---

### 4.3 — Operators

```java
public class Operators {
    public static void main(String[] args) {
        int a = 10, b = 3;

        // Arithmetic
        System.out.println(a + b);   // 13  (addition)
        System.out.println(a - b);   // 7   (subtraction)
        System.out.println(a * b);   // 30  (multiplication)
        System.out.println(a / b);   // 3   (integer division — truncates!)
        System.out.println(a % b);   // 1   (modulus — remainder)

        // Comparison (returns boolean)
        System.out.println(a == b);  // false
        System.out.println(a != b);  // true
        System.out.println(a > b);   // true
        System.out.println(a >= b);  // true

        // Logical
        System.out.println(true && false);  // false  (AND)
        System.out.println(true || false);  // true   (OR)
        System.out.println(!true);          // false  (NOT)

        // Increment / Decrement
        a++;  // a is now 11
        b--;  // b is now 2
    }
}
```

---

### 4.4 — Control Flow (if / else / switch)

```java
public class ControlFlow {
    public static void main(String[] args) {
        int score = 85;

        // === IF / ELSE IF / ELSE ===
        if (score >= 90) {
            System.out.println("Grade: A");
        } else if (score >= 80) {
            System.out.println("Grade: B");    // ← This runs
        } else if (score >= 70) {
            System.out.println("Grade: C");
        } else {
            System.out.println("Grade: F");
        }

        // === TERNARY OPERATOR (shorthand if/else) ===
        String result = (score >= 60) ? "PASS" : "FAIL";
        System.out.println(result);  // PASS

        // === SWITCH STATEMENT ===
        String day = "Monday";
        switch (day) {
            case "Monday":
            case "Tuesday":
            case "Wednesday":
            case "Thursday":
            case "Friday":
                System.out.println("Weekday");
                break;
            case "Saturday":
            case "Sunday":
                System.out.println("Weekend");
                break;
            default:
                System.out.println("Invalid day");
        }
    }
}
```

---

### 4.5 — Loops

```java
public class Loops {
    public static void main(String[] args) {

        // === FOR LOOP (when you know how many times) ===
        for (int i = 0; i < 5; i++) {
            System.out.println("Count: " + i);    // 0, 1, 2, 3, 4
        }

        // === WHILE LOOP (when you don't know how many times) ===
        int count = 0;
        while (count < 3) {
            System.out.println("While: " + count);
            count++;
        }

        // === DO-WHILE (runs at least once) ===
        int x = 10;
        do {
            System.out.println("Do-While: " + x);  // Runs once even though condition is false
            x++;
        } while (x < 5);

        // === FOR-EACH (iterating over arrays/collections) ===
        String[] fruits = {"Apple", "Banana", "Cherry"};
        for (String fruit : fruits) {
            System.out.println(fruit);
        }

        // === BREAK and CONTINUE ===
        for (int i = 0; i < 10; i++) {
            if (i == 3) continue;  // Skip 3
            if (i == 7) break;     // Stop at 7
            System.out.println(i); // Prints 0,1,2,4,5,6
        }
    }
}
```

---

### 4.6 — Methods (Functions)

```java
public class Methods {

    // Method with no return value
    static void greet(String name) {
        System.out.println("Hello, " + name + "!");
    }

    // Method with a return value
    static int add(int a, int b) {
        return a + b;
    }

    // Method with default-like behavior (overloading)
    static double multiply(double a, double b) {
        return a * b;
    }

    static double multiply(double a) {
        return a * a;  // Squares the number if only one arg
    }

    public static void main(String[] args) {
        greet("Brave Wolf");           // Hello, Brave Wolf!

        int sum = add(5, 3);
        System.out.println("Sum: " + sum);     // Sum: 8

        System.out.println(multiply(4, 5));     // 20.0
        System.out.println(multiply(4));        // 16.0 (overloaded version)
    }
}
```

---

### 4.7 — Arrays

```java
import java.util.Arrays;

public class ArrayBasics {
    public static void main(String[] args) {

        // Declaration + initialization
        int[] numbers = {10, 20, 30, 40, 50};

        // Access by index (0-based)
        System.out.println(numbers[0]);  // 10
        System.out.println(numbers[4]);  // 50

        // Modify an element
        numbers[2] = 99;

        // Length
        System.out.println("Length: " + numbers.length);  // 5

        // Loop through
        for (int num : numbers) {
            System.out.print(num + " ");  // 10 20 99 40 50
        }
        System.out.println();

        // Useful utility methods
        int[] copy = Arrays.copyOf(numbers, numbers.length);
        Arrays.sort(copy);
        System.out.println(Arrays.toString(copy));  // [10, 20, 40, 50, 99]

        // 2D Array
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        System.out.println(matrix[1][2]);  // 6
    }
}
```

---

### 4.8 — Strings

```java
public class StringBasics {
    public static void main(String[] args) {
        String name = "Brave Wolf";

        // Common methods
        System.out.println(name.length());            // 10
        System.out.println(name.toUpperCase());       // BRAVE WOLF
        System.out.println(name.toLowerCase());       // brave wolf
        System.out.println(name.charAt(0));           // B
        System.out.println(name.indexOf("Wolf"));     // 6
        System.out.println(name.substring(6));        // Wolf
        System.out.println(name.substring(0, 5));     // Brave
        System.out.println(name.contains("Wolf"));    // true
        System.out.println(name.replace("Wolf", "Lion")); // Brave Lion
        System.out.println(name.trim());              // Removes whitespace
        System.out.println(name.isEmpty());           // false

        // String comparison — NEVER use == for Strings!
        String a = "hello";
        String b = "hello";
        System.out.println(a.equals(b));              // true ✅
        System.out.println(a.equalsIgnoreCase("HELLO")); // true

        // String concatenation
        String full = "Hello" + " " + "World";       // Simple concat
        
        // StringBuilder (more efficient for many concatenations)
        StringBuilder sb = new StringBuilder();
        sb.append("Hello");
        sb.append(" ");
        sb.append("World");
        System.out.println(sb.toString());            // Hello World

        // String formatting
        String formatted = String.format("Name: %s, Age: %d", "Wolf", 21);
        System.out.println(formatted);
    }
}
```

---

### 4.9 — User Input (Scanner)

```java
import java.util.Scanner;

public class UserInput {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();      // Reads full line

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();           // Reads integer

        System.out.print("Enter your GPA: ");
        double gpa = scanner.nextDouble();     // Reads double

        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("GPA: " + gpa);

        scanner.close();  // Always close when done!
    }
}
```

---

## 5. Object-Oriented Programming (OOP) Essentials

### 5.1 — Classes & Objects

```java
// File: Car.java
public class Car {
    // Fields (attributes)
    String brand;
    String color;
    int year;

    // Constructor
    public Car(String brand, String color, int year) {
        this.brand = brand;
        this.color = color;
        this.year = year;
    }

    // Method
    public void displayInfo() {
        System.out.println(year + " " + color + " " + brand);
    }
}

// File: Main.java
public class Main {
    public static void main(String[] args) {
        Car car1 = new Car("Toyota", "Red", 2024);
        Car car2 = new Car("BMW", "Black", 2025);

        car1.displayInfo();  // 2024 Red Toyota
        car2.displayInfo();  // 2025 Black BMW
    }
}
```

### 5.2 — The Four Pillars of OOP

```
┌─────────────────────────────────────────────────────────┐
│                  4 PILLARS OF OOP                       │
├──────────────┬──────────────────────────────────────────┤
│ Encapsulation│ Hide data, expose via getters/setters    │
│ Inheritance  │ Child class inherits from parent class   │
│ Polymorphism │ Same method, different behavior          │
│ Abstraction  │ Hide complexity, show essentials         │
└──────────────┴──────────────────────────────────────────┘
```

### 5.3 — Encapsulation

```java
public class BankAccount {
    private double balance;  // Private — can't be accessed directly

    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    // Getter
    public double getBalance() {
        return balance;
    }

    // Controlled setter
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
        } else {
            System.out.println("Insufficient funds!");
        }
    }
}
```

### 5.4 — Inheritance

```java
// Parent class
public class Animal {
    String name;

    public Animal(String name) {
        this.name = name;
    }

    public void speak() {
        System.out.println(name + " makes a sound");
    }
}

// Child class
public class Dog extends Animal {

    public Dog(String name) {
        super(name);  // Call parent constructor
    }

    @Override
    public void speak() {
        System.out.println(name + " barks! 🐕");
    }

    public void fetch() {
        System.out.println(name + " fetches the ball!");
    }
}
```

### 5.5 — Access Modifiers

| Modifier | Same Class | Same Package | Subclass | Everywhere |
|---|---|---|---|---|
| `public` | ✅ | ✅ | ✅ | ✅ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| *(default)* | ✅ | ✅ | ❌ | ❌ |
| `private` | ✅ | ❌ | ❌ | ❌ |

---

## 6. VS Code Tips for Java

| Action | Shortcut / Method |
|---|---|
| Run Java file | Click **▶ Run** above `main()` |
| Open terminal | `` Ctrl + ` `` |
| Format code | `Shift + Option + F` |
| Quick fix / suggestions | `Cmd + .` |
| Go to definition | `Cmd + Click` |
| Find references | `Shift + F12` |
| Rename symbol | `F2` |
| Generate constructor/getters | Right-click → Source Action |

> [!TIP]
> The Java Extension Pack gives you **IntelliSense**, **debugging**, **test runner**, **Maven/Gradle support**, and **project management** out of the box. You're all set!

---

## 7. Common Beginner Mistakes to Avoid

| Mistake | Fix |
|---|---|
| File name doesn't match class name | `Hello.java` must contain `public class Hello` |
| Using `==` to compare Strings | Use `.equals()` instead |
| Forgetting `break` in switch | Each `case` needs `break` (or use arrow syntax) |
| Forgetting semicolons | Every statement ends with `;` |
| `int / int` gives int result | Cast to `double`: `(double) a / b` |
| Not closing Scanner | Always call `scanner.close()` |
| Array index out of bounds | Arrays are 0-indexed, max index is `length - 1` |

---

## 8. Quick Terminal Cheat Sheet

```bash
# Compile and run (two steps)
javac Hello.java && java Hello

# Direct run (single-file, Java 11+)
java Hello.java

# Compile all Java files in a directory
javac *.java

# Run with command-line arguments
java Hello arg1 arg2

# Run with a specific classpath
java -cp ./out MyClass

# Check your setup
java -version
javac -version
echo $JAVA_HOME
```

---

> [!NOTE]
> **Next steps:** Start practicing by creating the files in Section 4 — type them out rather than copy-pasting. Muscle memory is how you learn Java. When you're comfortable with the basics, move on to OOP concepts in Section 5.
