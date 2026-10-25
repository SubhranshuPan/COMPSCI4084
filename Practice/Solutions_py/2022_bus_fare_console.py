# -*- coding: utf-8 -*-
"""
2022 paper (bus fare calculator, database TravelPrice) re-done WITHOUT
tkinter: ages typed one at a time, then a menu.
"""
import sqlite3

conn = sqlite3.connect("TravelPrice.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Passengers (
                      id    INTEGER PRIMARY KEY AUTOINCREMENT,
                      age   INTEGER NOT NULL,
                      price INTEGER NOT NULL)""")
conn.commit()


def ticket_price(age):
    if age <= 2:
        return 0
    elif age <= 12:
        return 7
    elif age >= 66:
        return 13
    else:
        return 18


def enter_ages():
    """Keep asking for ages until the user types q."""
    while True:
        text = input("Enter the client's age (q to stop): ").strip()
        if text.lower() == "q":
            break
        try:
            age = int(text)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if age < 0 or age > 120:
            print("Age must be between 0 and 120.")
            continue
        cursor.execute("INSERT INTO Passengers (age, price) VALUES (?, ?)",
                       (age, ticket_price(age)))
        conn.commit()


def show_ages_and_prices():
    cursor.execute("SELECT age, price FROM Passengers ORDER BY id")
    print("Client's age in years | Price per client (GBP)")
    for age, price in cursor.fetchall():
        print(f"{age:>21} | {price:>6}")


def show_total():
    cursor.execute("SELECT SUM(price) FROM Passengers")
    total = cursor.fetchone()[0] or 0            # None -> 0 when empty
    print(f"Total cost for the journey: GBP {total}")


def clear_all():
    cursor.execute("DELETE FROM Passengers")
    conn.commit()
    print("Database cleared.")


def main():
    choice = ""
    while choice != "0":
        print("\n1) Add ages  2) Show ages+prices  3) Total cost  "
              "4) Clear all  0) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            enter_ages()
        elif choice == "2":
            show_ages_and_prices()
        elif choice == "3":
            show_total()
        elif choice == "4":
            clear_all()
    conn.close()


if __name__ == "__main__":
    main()
