# Problem 1 — Explanations for Each Fragment

---

## (ii) Variable Shadowing

```java
public class A {
    public int i = 3;          // FIELD — belongs to the object
    public A(int val) {
        int i = val;           // LOCAL variable — only exists inside this constructor
    }
}
A a = new A(5);
System.out.println(a.i);
```

### What happens?
✅ **Compiles and runs. Output: `3`**

### Why?
- The class has a **field** called `i`, which is set to `3` when the object is created.
- Inside the constructor, `int i = val;` creates a **brand-new local variable** also called `i`. This is called **variable shadowing** — the local `i` hides the field `i`.
- The local `i` gets the value `5`, but it **disappears** when the constructor finishes. The **field** `i` was never touched — it stays `3`.
- So `a.i` prints `3`, not `5`.

### How to fix it (if you wanted it to print `5`)?
Use `this.i` to refer to the field instead of creating a local variable:
```java
public A(int val) {
    this.i = val;    // now it modifies the FIELD
}
```

---

## (iii) Lossy Conversion (double → int)

```java
int i = 5.0;
int j = 10.0;
System.out.println(i / j);
```

### What happens?
❌ **Will NOT compile.**

**Error:** `incompatible types: possible lossy conversion from double to int`

### Why?
- `5.0` and `10.0` are **double** literals (they have a decimal point).
- `int` can only hold whole numbers (like `5`, `10`).
- Java **refuses** to automatically convert a `double` to an `int` because you could lose the decimal part (e.g., `5.7` → `5` loses the `.7`). This is called a **narrowing conversion**, and Java won't do it without you explicitly asking.

### How to fix it?
**Option A** — Use `int` literals (remove the `.0`):
```java
int i = 5;
int j = 10;
```

**Option B** — Use `double` variables instead:
```java
double i = 5.0;
double j = 10.0;
```

**Option C** — Explicit cast (tells Java "I know I might lose data, do it anyway"):
```java
int i = (int) 5.0;
int j = (int) 10.0;
```

---

## (iv) Unreachable Statement

```java
try {
    throw new Exception("Hello!");
    System.out.println("World!");    // ← this line is the problem
} catch (Exception ex) {
    System.out.println(ex.getMessage());
}
```

### What happens?
❌ **Will NOT compile.**

**Error:** `unreachable statement`

### Why?
- `throw` immediately exits the current block — it jumps straight to the `catch`.
- The `System.out.println("World!")` line comes **after** the `throw`, so it can **never** be reached. There's no possible way for Java to execute that line.
- Java's compiler detects this and **refuses to compile** — it treats unreachable code as an error, not just a warning.

### How to fix it?
Remove the unreachable line, or move it **before** the `throw`:
```java
try {
    System.out.println("World!");    // moved BEFORE throw
    throw new Exception("Hello!");
} catch (Exception ex) {
    System.out.println(ex.getMessage());
}
// Output: World!
//         Hello!
```

---

## (v) Missing No-Arg Constructor in Superclass

```java
// File A.java
public class A {
    public A(int value) {                        // only constructor — takes an int
        System.out.println("Value is " + value);
    }
}

// File B.java
public class B extends A {                       // B extends A, but has NO constructor
    public static void main(String[] args) {
        A a = new A(10);
    }
}
```

### What happens?
❌ **Will NOT compile.**

**Error:** `constructor A in class A cannot be applied to given types; required: int; found: no arguments`

### Why?
Think of it step by step:

1. `B extends A` — so `B` is a child of `A`.
2. `B` has **no constructor** written, so Java **auto-generates** a default one:
   ```java
   public B() {
       super();   // Java adds this automatically — calls A's no-arg constructor
   }
   ```
3. But `A` does **not have** a no-arg constructor `A()`. It only has `A(int value)`.
4. When a class defines **any** constructor, Java **stops** providing the free default `A()` constructor.
5. So `super()` has nothing to call → **compilation error**.

> [!TIP]
> **Key rule:** If a parent class only has constructors with parameters, every child class **must** explicitly call one of those constructors using `super(...)`.

### How to fix it?

**Option A** — Add a no-arg constructor to `A`:
```java
public class A {
    public A() { }                  // now super() works
    public A(int value) { ... }
}
```

**Option B** — Add a constructor to `B` that calls `super(int)`:
```java
public class B extends A {
    public B() {
        super(0);   // explicitly calls A(int) with a default value
    }
}
```

---

## Quick Summary Table

| Fragment | Compiles? | Result | Core Concept |
|----------|-----------|--------|--------------|
| **(ii)** | ✅ Yes | Output: `3` | **Variable shadowing** — local variable hides the field |
| **(iii)** | ❌ No | Lossy conversion error | **Narrowing conversion** — `double` can't auto-convert to `int` |
| **(iv)** | ❌ No | Unreachable statement error | **Unreachable code** — nothing can run after `throw` |
| **(v)** | ❌ No | No matching constructor error | **Implicit `super()`** — parent needs a no-arg constructor |
