/**
 * Problem 2 & 3: Employee class
 *
 * Models a company employee with pay calculation.
 * Workers are paid 1.5x their normal rate for hours above contracted.
 */
public class Employee {

    // Attributes (private for encapsulation)
    private int employeeNumber;
    private String familyName;
    private String givenName;
    private double hourlyRate;
    private int contractedHours; // per month
    private int hoursWorked;     // actual hours worked this month

    /**
     * Constructor: initialises all fields.
     * Hours actually worked is initialised to zero.
     */
    public Employee(int employeeNumber, String familyName, String givenName,
                    double hourlyRate, int contractedHours) {
        this.employeeNumber = employeeNumber;
        this.familyName = familyName;
        this.givenName = givenName;
        this.hourlyRate = hourlyRate;
        this.contractedHours = contractedHours;
        this.hoursWorked = 0; // initial value is zero
    }

    /**
     * Problem 3: computePay()
     *
     * Computes and returns the employee's monthly pay.
     * - Normal hours (up to contracted): paid at hourlyRate
     * - Overtime hours (above contracted): paid at 1.5 * hourlyRate
     */
    public double computePay() {
        if (hoursWorked <= contractedHours) {
            // No overtime
            return hoursWorked * hourlyRate;
        } else {
            // Overtime: contracted hours at normal rate + extra hours at 1.5x
            int overtimeHours = hoursWorked - contractedHours;
            return (contractedHours * hourlyRate) + (overtimeHours * hourlyRate * 1.5);
        }
    }

    // Simple setter for testing
    public void setHoursWorked(int hours) {
        this.hoursWorked = hours;
    }

    // --- Main method to demonstrate ---
    public static void main(String[] args) {
        Employee emp = new Employee(1001, "Smith", "John", 15.00, 160);

        System.out.println("=== Employee Pay Calculator ===");

        // Test 1: No overtime (worked exactly contracted hours)
        emp.setHoursWorked(160);
        System.out.println("Hours worked: 160 (no overtime)");
        System.out.printf("Pay: £%.2f%n", emp.computePay()); // 160 * 15 = 2400.00

        // Test 2: Overtime (worked 180, contracted 160 → 20 hours overtime)
        emp.setHoursWorked(180);
        System.out.println("\nHours worked: 180 (20 hours overtime)");
        System.out.printf("Pay: £%.2f%n", emp.computePay()); // (160*15) + (20*15*1.5) = 2400 + 450 = 2850.00

        // Test 3: Under hours
        emp.setHoursWorked(100);
        System.out.println("\nHours worked: 100 (under contracted)");
        System.out.printf("Pay: £%.2f%n", emp.computePay()); // 100 * 15 = 1500.00
    }
}
