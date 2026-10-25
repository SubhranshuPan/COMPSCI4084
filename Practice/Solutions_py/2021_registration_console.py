# -*- coding: utf-8 -*-
"""
2021 paper (Registration + validation) re-done WITHOUT tkinter:
a menu in the terminal.  Same database logic, same validation rules.
"""
import sqlite3

conn = sqlite3.connect("Users.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                      id       INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL)""")
conn.commit()


def username_exists(username):
    cursor.execute("SELECT id FROM Users WHERE LOWER(username) = LOWER(?)",
                   (username,))
    return cursor.fetchone() is not None


def password_is_valid(password):
    # at least 8 characters AND at least one digit
    return len(password) >= 8 and any(ch.isdigit() for ch in password)


def register():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")
    if username == "" or password == "":
        print("Username and password cannot be empty.")
    elif username_exists(username):
        print("Username already exists - choose another one.")
    elif not password_is_valid(password):
        print("The password requirements are not met "
              "(minimum 8 characters and at least one number).")
    else:
        cursor.execute("INSERT INTO Users (username, password) "
                       "VALUES (?, ?)", (username, password))
        conn.commit()
        print("Saved.")


def display_all():
    cursor.execute("SELECT id, username, password FROM Users ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("(no users saved yet)")
    for user_id, username, password in rows:
        print(user_id, username, password)


def main():
    choice = ""
    while choice != "3":
        print("\n1) Register   2) Display all   3) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            display_all()
        elif choice != "3":
            print("Please type 1, 2 or 3.")
    conn.close()


if __name__ == "__main__":
    main()
