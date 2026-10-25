# -*- coding: utf-8 -*-
"""
2023 paper (library + simulated ChatGPT librarian, database LibraryDB)
re-done WITHOUT tkinter: a menu in the terminal.
"""
import datetime
import re
import sqlite3

conn = sqlite3.connect("LibraryDB.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
                      isbn   TEXT PRIMARY KEY,
                      title  TEXT NOT NULL,
                      author TEXT NOT NULL,
                      year   INTEGER NOT NULL)""")
conn.commit()


def add_book():
    isbn = input("ISBN: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_text = input("Year: ").strip()

    if isbn == "" or title == "" or author == "":
        print("Error: ISBN, title and author cannot be empty!")
        return
    if not year_text.isdigit():                  # also rejects '-5' and 'abc'
        print("Error: invalid year of publication!")
        return
    year = int(year_text)
    if year < 1450 or year > datetime.date.today().year:
        print("Error: invalid year of publication!")
        return
    cursor.execute("SELECT 1 FROM Books WHERE isbn = ?", (isbn,))
    if cursor.fetchone() is not None:
        print("Error: this ISBN already exists!")
        return

    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?)",
                   (isbn, title, author, year))
    conn.commit()
    print("Book added successfully!")


def display_books():
    cursor.execute("SELECT isbn, title, author, year FROM Books")
    for isbn, title, author, year in cursor.fetchall():
        print(f"ISBN: {isbn}, Title: {title}, Author: {author}, "
              f"Year: {year}")


def virtual_librarian(question):
    """Two sentence shapes only: recommend by author / publication year."""
    match = re.match(r"recommend me a book by (.+?)[.?!]*$", question.strip(),
                     re.IGNORECASE)
    if match:
        author = match.group(1).strip()
        cursor.execute("SELECT title, author FROM Books "
                       "WHERE LOWER(author) = LOWER(?) "
                       "ORDER BY RANDOM() LIMIT 1", (author,))
        row = cursor.fetchone()
        return (f"How about '{row[0]}' by {row[1]}?" if row
                else f"Sorry, I have no books by {author}.")

    match = re.match(r"when was (?:published )?(.+?)(?: published)?[.?!]*$",
                     question.strip(), re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        cursor.execute("SELECT title, year FROM Books "
                       "WHERE LOWER(title) = LOWER(?)", (title,))
        row = cursor.fetchone()
        return (f"{row[0]} was published in {row[1]}." if row
                else f"Sorry, I could not find '{title}'.")

    return "Sorry, I can only answer two kinds of question."


def main():
    choice = ""
    while choice != "4":
        print("\n1) Add book  2) Display books  3) Ask librarian  4) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            print(virtual_librarian(input("Ask the librarian: ")))
    conn.close()


if __name__ == "__main__":
    main()
