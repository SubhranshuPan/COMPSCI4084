# -*- coding: utf-8 -*-
"""
Final Lab Exam 2021 - Python Part: Registration Page (tkinter + SQLite)
NOTE: tkinter is no longer assessed. The DATABASE + VALIDATION logic in the
middle of this file is what still matters (see the console version in the
prep pack).  Run:  python 2021_registration_users_solution.py
"""
import sqlite3
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------- DATABASE
conn = sqlite3.connect("Users.db")               # opens (or creates) Users.db
cursor = conn.cursor()                           # the 'clerk' who runs SQL
cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                      id       INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL)""")
conn.commit()                                    # make the table permanent


# ------------------------------------------------- VALIDATION (no GUI code)
def username_exists(username):
    """True if this username is already stored (Task 1b, 5 marks).
    LOWER() on both sides: 'Mireilla' and 'mireilla' count as the SAME."""
    cursor.execute("SELECT id FROM Users WHERE LOWER(username) = LOWER(?)",
                   (username,))
    return cursor.fetchone() is not None         # a row came back -> exists


def password_is_valid(password):
    """Task 1b, 6 marks: at least 8 characters AND contains a digit."""
    long_enough = len(password) >= 8             # criterion (a)
    has_number = any(ch.isdigit() for ch in password)  # criterion (b)
    return long_enough and has_number            # BOTH must be true


# ------------------------------------------------------- BUTTON CALLBACKS
def save_user():
    """Save button: validate, then store (Task 1a 4 marks + Task 1b)."""
    username = username_entry.get().strip()      # text typed in the box
    password = password_entry.get()

    if username == "" or password == "":         # nothing typed?
        messagebox.showwarning("Missing details",
                               "Please enter a username and a password.")
        return                                   # stop - do NOT save

    if username_exists(username):                # duplicate username?
        messagebox.showwarning("Username already exists",
                               "That username is taken. Choose another.")
        return

    if not password_is_valid(password):          # weak password?
        messagebox.showwarning("The password requirements not met",
                               "Password needs at least 8 characters "
                               "and must include a number.")
        return

    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                   (username, password))         # ? = safe placeholders
    conn.commit()                                # SAVE the form permanently
    messagebox.showinfo("Saved", "Registration saved.")
    username_entry.delete(0, tk.END)             # empty the two boxes
    password_entry.delete(0, tk.END)


def clear_windows():
    """Clear button: empty ALL windows (Task 1a, 2 marks). DB is untouched."""
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    display_box.delete("1.0", tk.END)            # Text widget: line.char


def display_users():
    """Display button: show every saved user (Task 1a, 3 marks)."""
    display_box.delete("1.0", tk.END)            # wipe old text first
    cursor.execute("SELECT id, username, password FROM Users "
                   "ORDER BY id DESC")           # newest first (as sample)
    for user_id, username, password in cursor.fetchall():
        display_box.insert(tk.END, f"{user_id} {username} {password}\n")


# ------------------------------------------------------------- THE WINDOW
root = tk.Tk()                                   # the main window
root.title("Registration Page")
root.geometry("520x400")

tk.Label(root, text="Enter your username:").grid(row=0, column=0, padx=10,
                                                 pady=10, sticky="e")
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, columnspan=2, sticky="w")

tk.Label(root, text="Enter your password:").grid(row=1, column=0, padx=10,
                                                 pady=10, sticky="e")
password_entry = tk.Entry(root, width=30)        # add show="*" to hide text
password_entry.grid(row=1, column=1, columnspan=2, sticky="w")

save_button = tk.Button(root, text="Save", width=8, command=save_user)
save_button.grid(row=2, column=1, pady=5)
clear_button = tk.Button(root, text="Clear", width=8, command=clear_windows)
clear_button.grid(row=2, column=2, pady=5)

tk.Label(root, text="Display all usernames and associated passwords "
                    "in the database").grid(row=3, column=1, columnspan=2,
                                            pady=(20, 0), sticky="w")
display_button = tk.Button(root, text="Display", width=8,
                           command=display_users)
display_button.grid(row=4, column=0, padx=10)
display_box = tk.Text(root, width=40, height=10)
display_box.grid(row=4, column=1, columnspan=2)

if __name__ == "__main__":                       # only when run directly
    root.mainloop()                              # keep window alive
    conn.close()
