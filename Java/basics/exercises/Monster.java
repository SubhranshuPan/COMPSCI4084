package basics.exercises;

public abstract class Monster {
    private final String type;
    private int hitPoints;
    private final int attackPoints;
    private final String[] weaknesses;

    public Monster(String type, int hitPoints, int attackPoints, String[] weaknesses) {
        this.type = type;
        this.hitPoints = hitPoints;
        this.attackPoints = attackPoints;
        this.weaknesses = weaknesses;
    }

    public String getType() {
        return this.type;
    }

    public int getHitPoints() {
        return this.hitPoints;
    }

    public int getAttackPoints() {
        return this.attackPoints;
    }

    public boolean isWeakAgainst(String otherType) {
        for (String w : weaknesses) {
            if (w.equals(otherType)) {
                return true;
            }
        }
        return false;
    }

    public void removeHitPoints(int amount) {
        hitPoints = Math.max(0, hitPoints - amount);
    }

    protected abstract boolean dodge();

    public boolean attack(Monster otherMonster) {
        if (otherMonster == this) {
            return false;
        }
        if (hitPoints == 0 || otherMonster.hitPoints == 0) {
            return false;
        }
        if (otherMonster.dodge()) {
            this.removeHitPoints(10);
        } else if (otherMonster.isWeakAgainst(type)) {
            otherMonster.removeHitPoints(attackPoints + 20);
        } else {
            otherMonster.removeHitPoints(attackPoints);
        }
        return true;
    }

    private static void status(String label, Monster... monsters) {
        StringBuilder sb = new StringBuilder(label).append(":");
        for (Monster m : monsters) {
            sb.append("  ").append(m.getType()).append("=").append(m.getHitPoints());
        }
        System.out.println(sb);
    }

    public static void main(String[] args) {
        Monster fire = new FireMonster(100, 30);
        Monster water = new WaterMonster(120, 25);
        Monster electric = new ElectricMonster(80, 40);
        status("Start", fire, water, electric);

        // Water has >= 100 HP so it dodges; the attacker (Fire) loses 10 HP.
        System.out.println("fire attacks water -> " + fire.attack(water));
        status("After", fire, water, electric);

        // Fire's 1st dodge() is true; the attacker (Water) loses 10 HP.
        System.out.println("water attacks fire -> " + water.attack(fire));
        status("After", fire, water, electric);

        // Fire's 2nd dodge() is false; Fire is weak to Water, so 25 + 20 = 45 damage.
        System.out.println("water attacks fire -> " + water.attack(fire));
        status("After", fire, water, electric);

        // Water still has >= 100 HP, so it dodges Electric's attack.
        System.out.println("electric attacks water -> " + electric.attack(water));
        status("After", fire, water, electric);

        // Drop Water below 100 HP so it can no longer dodge.
        water.removeHitPoints(20);
        // Water is weak to Electric, so 40 + 20 = 60 damage.
        System.out.println("electric attacks water -> " + electric.attack(water));
        status("After", fire, water, electric);

        // A monster cannot attack itself.
        System.out.println("fire attacks fire -> " + fire.attack(fire));

        // A knocked-out monster cannot be attacked (and cannot attack).
        water.removeHitPoints(1000);
        System.out.println("fire attacks knocked-out water -> " + fire.attack(water));
        System.out.println("knocked-out water attacks fire -> " + water.attack(fire));
        status("End", fire, water, electric);

        // isWeakAgainst checks
        System.out.println("fire weak against Water? " + fire.isWeakAgainst("Water"));
        System.out.println("fire weak against Electric? " + fire.isWeakAgainst("Electric"));
        System.out.println("electric weak against Fire? " + electric.isWeakAgainst("Fire"));
    }
}

class FireMonster extends Monster {
    private boolean dodgeNext = true;

    public FireMonster(int hitPoints, int attackPoints) {
        super("Fire", hitPoints, attackPoints, new String[] { "Water" });
    }

    @Override
    protected boolean dodge() {
        boolean result = dodgeNext;
        dodgeNext = !dodgeNext;
        return result;
    }
}

class WaterMonster extends Monster {
    public WaterMonster(int hitPoints, int attackPoints) {
        super("Water", hitPoints, attackPoints, new String[] { "Fire", "Electric" });
    }

    @Override
    protected boolean dodge() {
        return getHitPoints() >= 100; // use getter (private)
    }
}

class ElectricMonster extends Monster {
    public ElectricMonster(int hitPoints, int attackPoints) {
        super("Electric", hitPoints, attackPoints, new String[0]);
    }

    @Override
    protected boolean dodge() {
        return false;
    }
}