package basics;

public class JavaBasics {

    public static void main(String[] args) {
        int a = 10;
        System.out.println(a);

        String[] fruits = new String[] { "Apple", "Banana", "Cherry" };

        for (int i = 0; i < fruits.length; i++) {
            System.out.println(fruits[i]);
        }

        for (String fruit : fruits) {
            System.out.println(fruit);
        }
    }
}
