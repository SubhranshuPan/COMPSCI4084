package basics;

public class OOPS {

    public static void main(String[] args) {
        BankAccount b = new BankAccount("Dave", 1000);
        System.out.println(b.name);
        System.out.println(b.balance);
        b.balance += 1000;
        b.name = "Eve";
        System.out.println(b.name);
        System.out.println(b.balance);
        System.out.println(b.toString());
        BankAccount b1 = new BankAccount("Som", 1000);
        BankAccount b2 = new BankAccount("Arya", 2000);
        System.out.println(b1.toString());
        System.out.println(b2.toString());
    }

}

class BankAccount {
    int balance;
    String name;
    int id;

    static int idCounter = 0;

    void deposit(int val) {
        this.balance += val;
    }

    void withdraw(int val) {
        this.balance -= val;
    }

    BankAccount(String name, int initialAmount) {
        this.name = name;
        this.balance = initialAmount;
        this.id = idCounter++;
    }

    public String toString() {
        return "Account #" + id
                + ", Name = " + name
                + ", balance = "
                + balance;
    }
}
