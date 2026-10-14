package basics;

public class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public void move() {
        System.out.println(name + " can move");
    }

    public String getName() {
        return this.name;
    }

    public static void main(String[] args) {
        // 1. Base class object
        Animal genericAnimal = new Animal("Generic Animal");
        genericAnimal.move();

        // 2. Subclass object (inherits name and getName(), overrides move())
        Dog dog = new Dog("Buddy", "Golden Retriever");
        dog.move();
        dog.bark();
        System.out.println("Dog's inherited name: " + dog.getName());

        // 3. Polymorphism: Base class reference pointing to a Subclass object
        Animal polyDog = new Dog("Max", "German Shepherd");
        polyDog.move(); // Calls Dog's overridden move() method at runtime
    }
}

// Cannot be 'public' because file is Animal.java
class Dog extends Animal {
    private String breed;

    public Dog(String name, String breed) {
        super(name); // Call the parent constructor to set 'name'
        this.breed = breed;
    }

    @Override
    public void move() {
        System.out.println(name + " (" + breed + ") can walk and run");
    }

    public void bark() {
        System.out.println(name + " says: Woof!");
    }
}
