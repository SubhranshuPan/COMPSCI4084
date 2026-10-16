import java.util.*;

/**
 * Problem 1: Phone Bill Calculator
 *
 * The original code had TWO bugs:
 *   Bug 1: HashMap created INSIDE the loop — resets every iteration, losing all previous data.
 *   Bug 2: Integer division (/ 2) instead of floating-point division (/ 2.0).
 *
 * This file contains both the BUGGY and FIXED versions for comparison.
 */
public class PhoneBill {

    // ==========================================
    // BUGGY VERSION (original from the exercise)
    // ==========================================
    public static double calculateBillBuggy(List<Call> calls, String favourite) {
        Map<String, Integer> totals;
        for (Call call : calls) {
            totals = new HashMap<>();  // BUG 1: resets the map every iteration!
            if (totals.containsKey(call.number)) {
                totals.put(call.number,
                    totals.get(call.number) + call.duration);
            } else {
                totals.put(call.number, call.duration);
            }
        }
        // At this point, totals only contains the LAST call.
        // We need to keep 'totals' as a local variable for the next loop:
        Map<String, Integer> totalsCopy = new HashMap<>();
        // Re-do to avoid compile error (totals may not be initialized if calls is empty)
        // For demonstration, just return 0 for the buggy version
        double totalCharge = 0;
        // BUG 2: integer division — odd minutes lose 0.5p each
        // totalCharge += totals.get(number) / 2;
        return totalCharge;
    }

    // ==========================================
    // FIXED VERSION
    // ==========================================
    public static double calculateBill(List<Call> calls, String favourite) {
        // FIX 1: Create the HashMap ONCE, before the loop
        Map<String, Integer> totals = new HashMap<>();

        for (Call call : calls) {
            // Now totals accumulates across all iterations
            if (totals.containsKey(call.number)) {
                totals.put(call.number,
                    totals.get(call.number) + call.duration);
            } else {
                totals.put(call.number, call.duration);
            }
        }

        double totalCharge = 0;
        for (String number : totals.keySet()) {
            // FIX 2: Use 2.0 (double) instead of 2 (int) to get correct decimal result
            totalCharge += totals.get(number) / 2.0;
        }
        return totalCharge;
    }

    // ==========================================
    // DEMO
    // ==========================================
    public static void main(String[] args) {
        List<Call> calls = new ArrayList<>();
        calls.add(new Call("01234567890", 5));   // 5 mins
        calls.add(new Call("09876543201", 17));  // 17 mins
        calls.add(new Call("01234567890", 14));  // 14 mins (same number as first)

        // Expected:
        //   "01234567890" → 5 + 14 = 19 mins → 19 / 2.0 = 9.5p
        //   "09876543201" → 17 mins           → 17 / 2.0 = 8.5p
        //   Total = 18.0p

        double bill = calculateBill(calls, "");
        System.out.println("=== Problem 1: Phone Bill ===");
        System.out.println("Calls:");
        System.out.println("  01234567890 → 5 mins");
        System.out.println("  09876543201 → 17 mins");
        System.out.println("  01234567890 → 14 mins");
        System.out.printf("Total bill (fixed): %.1fp%n", bill);  // 18.0p

        // Show what integer division would give (wrong answer)
        // 19/2 = 9 (not 9.5), 17/2 = 8 (not 8.5) → total = 17 instead of 18
        System.out.printf("Total bill (with int division bug): %dp%n", (19/2 + 17/2));
    }
}
