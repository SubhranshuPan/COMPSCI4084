package basics.exercises;

public class Exercises {

    static void printPrimes(int max) {

        for (int i = 2; i < max; i++) {
            boolean isPrime = true;
            for (int j = 2; j < i; j++) {
                if (i % j == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) {
                System.out.println(i);
            }
        }
    }

    static int computeFibonacci(int n) {
        int prev = 0, curr = 1;
        for (int i = 0; i < n; i++) {
            int next = prev + curr;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    private static final int[] SCORES = {
            1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10
    };

    static int computeScore(String word) {
        int total = 0;
        for (char ch : word.toUpperCase().toCharArray()) {
            if (ch >= 'A' && ch <= 'Z') {
                total += SCORES[ch - 'A'];
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // Task 1 :
        System.out.println("Primes below 50:");
        printPrimes(50);
        // Task 2 :
        System.out.println("Fibonacci 0..10:");
        for (int i = 0; i <= 10; i++) {
            System.out.print(computeFibonacci(i) + " ");
        }
        System.out.println();
        // Task 3:
        System.out.println("Score of \"Hello, World!\": " + computeScore("Hello, World!")); // 17
        System.out.println("Score of \"\": " + computeScore("")); // 0
        System.out.println("Score of \"quiz\": " + computeScore("quiz")); // 10+1+1+10 = 22
        // Task 4 and 5: run Monster.main
        // Task 6: run CardNum.main
    }

}
