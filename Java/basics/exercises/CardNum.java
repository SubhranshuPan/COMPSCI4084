package basics.exercises;

public class CardNum {
    static boolean checkCardNumber(String cardNumber) {
        if (cardNumber == null || !cardNumber.matches("\\d{13,19}")) {
            return false;
        }
        return hasValidIssuerAndLength(cardNumber) && passesLuhn(cardNumber);
    }

    private static boolean hasValidIssuerAndLength(String num) {
        int len = num.length();
        if (num.startsWith("4")) {
            return len == 13 || len == 16 || len == 19;
        }
        if (num.startsWith("34") || num.startsWith("37")) {
            return len == 15;
        }
        int first2 = Integer.parseInt(num.substring(0, 2));
        int first4 = Integer.parseInt(num.substring(0, 4));
        boolean masterCard = (first2 >= 51 && first2 <= 55) ||
                (first4 >= 2221 && first4 <= 2720);
        return masterCard && len == 16;
    }

    private static boolean passesLuhn(String num) {
        int sum = 0;
        int len = num.length();
        boolean doubleIt = false;
        for (int i = len - 1; i >= 0; i--) {
            int digit = num.charAt(i) - '0';
            if (doubleIt) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            sum += digit;
            doubleIt = !doubleIt;
        }
        return sum % 10 == 0;
    }

    public static void main(String[] args) {
        String[] numbers = {
                "4111111111111111", // valid Visa (16)
                "4222222222222", // valid Visa (13)
                "378282246310005", // valid Amex (15)
                "5555555555554444", // valid MasterCard (51-55 prefix)
                "2223000048400011", // valid MasterCard (2221-2720 prefix)
                "4111111111111112", // Visa prefix + length OK, bad checksum
                "79927398713", // passes Luhn, but too short / no issuer
                "3782822463100", // Amex prefix, wrong length
                "6011111111111117", // valid Luhn, but unsupported issuer
                "4111-1111-1111-1111", // non-digit characters
                "" // empty
        };
        for (String n : numbers) {
            System.out.println(n + " -> " + checkCardNumber(n));
        }
    }
}
