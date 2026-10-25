# -*- coding: utf-8 -*-
"""
Final Lab Exam 2022 - Python Part: Simple Journey Fare Calculator
(tkinter + SQLite database called TravelPrice)
NOTE: tkinter is no longer assessed. The fare rule + database logic is what
still matters.  Run:  python 2022_bus_fare_travelprice_solution.py
"""
import sqlite3
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------- DATABASE
conn = sqlite3.connect("TravelPrice.db")         # Task 1b: DB 'TravelPrice'
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Passengers (
                      id    INTEGER PRIMARY KEY AUTOINCREMENT,
                      age   INTEGER NOT NULL,
                      price INTEGER NOT NULL)""")
conn.commit()


# ------------------------------------------------------------ THE FARE RULE
def ticket_price(age):
    """Return the ticket price (in pounds) for one passenger's age."""
    if age <= 2:                                 # 0-2 years: free
        return 0
    elif age <= 12:                              # 3-12 years: children
        return 7
    elif age >= 66:                              # 66 and over: seniors
        return 13
    else:                                        # everybody else (13-65)
        return 18


# ------------------------------------------------------- BUTTON CALLBACKS
def save_age():
    """Save Age: store age + its price, then clear the box (6 marks)."""
    text = age_entry.get().strip()
    try:
        age = int(text)                          # must be a whole number
    except ValueError:
        messagebox.showerror("Invalid age", "Please enter a whole number.")
        return
    if age < 0 or age > 120:                     # sensible range check
        messagebox.showerror("Invalid age", "Age must be between 0 and 120.")
        return

    cursor.execute("INSERT INTO Passengers (age, price) VALUES (?, ?)",
                   (age, ticket_price(age)))     # store age AND its price
    conn.commit()
    age_entry.delete(0, tk.END)                  # ready for next passenger
    age_entry.focus()                            # cursor back in the box


def display_age():
    """Display Age: list every saved age (3 marks)."""
    age_list.delete(0, tk.END)                   # Listbox: from 0 to END
    cursor.execute("SELECT age FROM Passengers ORDER BY id")
    for (age,) in cursor.fetchall():             # each row is a 1-item tuple
        age_list.insert(tk.END, age)


def display_ticket_price():
    """Display ticket price: one price per age, SAME ORDER (3 marks)."""
    price_list.delete(0, tk.END)
    cursor.execute("SELECT price FROM Passengers ORDER BY id")
    for (price,) in cursor.fetchall():
        price_list.insert(tk.END, price)


def display_cost():
    """Display Cost: total for the whole group (5 marks)."""
    cursor.execute("SELECT SUM(price) FROM Passengers")
    total = cursor.fetchone()[0]                 # None if table is empty
    if total is None:
        total = 0
    cost_box.delete("1.0", tk.END)
    cost_box.insert(tk.END, str(total))


def clear_all():
    """Clear All: empty 3 display windows AND the database (2 marks)."""
    cursor.execute("DELETE FROM Passengers")     # no WHERE = every row
    conn.commit()
    age_entry.delete(0, tk.END)
    age_list.delete(0, tk.END)
    price_list.delete(0, tk.END)
    cost_box.delete("1.0", tk.END)


# ------------------------------------------------------------- THE WINDOW
root = tk.Tk()
root.title("Simple Journey Fare Calculator")
root.geometry("620x520")

tk.Label(root, text="Enter the client's age, one at a time").place(x=15, y=30)
age_entry = tk.Entry(root, width=30)
age_entry.place(x=225, y=30)

tk.Button(root, text="Save Age", width=10, command=save_age).place(x=225, y=90)
tk.Button(root, text="Clear All", width=10, command=clear_all).place(x=330,
                                                                     y=90)

tk.Label(root, text="Client's age in years:").place(x=200, y=150)
age_list = tk.Listbox(root, width=12, height=8)
age_list.place(x=200, y=175)
tk.Button(root, text="Display Age", width=14,
          command=display_age).place(x=50, y=230)

tk.Label(root, text="Price per client £:").place(x=480, y=150)
price_list = tk.Listbox(root, width=12, height=8)
price_list.place(x=480, y=175)
tk.Button(root, text="Display ticket price", width=16,
          command=display_ticket_price).place(x=320, y=230)

tk.Label(root, text="Display total cost for the journey:").place(x=200, y=370)
cost_box = tk.Text(root, width=30, height=2)
cost_box.place(x=200, y=395)
tk.Button(root, text="Display  Cost £", width=14,
          command=display_cost).place(x=50, y=410)

if __name__ == "__main__":
    root.mainloop()
    conn.close()
