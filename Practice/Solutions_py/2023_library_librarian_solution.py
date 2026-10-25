# -*- coding: utf-8 -*-
"""
Final Lab Exam 2023 - Python Part: Library Management System with a
simulated "ChatGPT" virtual librarian (tkinter + SQLite database LibraryDB)
NOTE: tkinter is no longer assessed. The DB, validation and the text-parsing
'librarian' function are the parts that still matter.
Run:  python 2023_library_librarian_solution.py
"""
import datetime
import re
import sqlite3
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------- DATABASE
conn = sqlite3.connect("LibraryDB.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
                      isbn   TEXT PRIMARY KEY,   -- PRIMARY KEY = no repeats
                      title  TEXT NOT NULL,
                      author TEXT NOT NULL,
                      year   INTEGER NOT NULL)""")
conn.commit()

FIRST_PRINTED_BOOK = 1450                        # earliest allowed year


# ---------------------------------------- TASK 1b: VALIDATION (no GUI code)
def isbn_exists(isbn):
    """Duplicate-ISBN check (1 mark)."""
    cursor.execute("SELECT 1 FROM Books WHERE isbn = ?", (isbn,))
    return cursor.fetchone() is not None


def year_is_valid(year):
    """Year not in the future AND not earlier than 1450 (1 mark)."""
    this_year = datetime.date.today().year       # today's year, automatically
    return FIRST_PRINTED_BOOK <= year <= this_year


# --------------------------------- TASK 1c: THE SIMULATED VIRTUAL LIBRARIAN
def virtual_librarian(question):
    """Answer the two supported sentence shapes using LibraryDB (7 marks)."""
    question = question.strip()

    # Shape 1: "Recommend me a book by <author>."
    match = re.match(r"recommend me a book by (.+?)[.?!]*$", question,
                     re.IGNORECASE)
    if match:
        author = match.group(1).strip()          # the text inside (.+?)
        cursor.execute("SELECT title, author FROM Books "
                       "WHERE LOWER(author) = LOWER(?) "
                       "ORDER BY RANDOM() LIMIT 1", (author,))
        row = cursor.fetchone()
        if row is None:
            return f"Sorry, I have no books by {author}."
        return f"How about '{row[0]}' by {row[1]}?"

    # Shape 2: "When was <title> published?"  (also accepts the order
    # "when was published <title>?" which the sample screenshot uses)
    match = re.match(r"when was (?:published )?(.+?)(?: published)?[.?!]*$",
                     question, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        cursor.execute("SELECT title, year FROM Books "
                       "WHERE LOWER(title) = LOWER(?)", (title,))
        row = cursor.fetchone()
        if row is None:
            return f"Sorry, I could not find '{title}'."
        return f"{row[0]} was published in {row[1]}."

    return "Sorry, I can only answer two kinds of question."


# ------------------------------------------------------- BUTTON CALLBACKS
def save_book():
    """Save: validate, store, show a success message (4 marks + Task 1b)."""
    isbn = isbn_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    year_text = year_entry.get().strip()

    if title == "" or author == "" or isbn == "":      # 1b.3 (1 mark)
        messagebox.showerror("Error",
                             "Title and Author fields cannot be empty!")
        return
    try:
        year = int(year_text)                    # year must be a number
    except ValueError:
        messagebox.showerror("Error", "Invalid year of publication!")
        return
    if not year_is_valid(year):                  # 1b.2 (1 mark)
        messagebox.showerror("Error", "Invalid year of publication!")
        return
    if isbn_exists(isbn):                        # 1b.1 (1 mark)
        messagebox.showerror("Error", "This ISBN already exists!")
        return

    cursor.execute("INSERT INTO Books (isbn, title, author, year) "
                   "VALUES (?, ?, ?, ?)", (isbn, title, author, year))
    conn.commit()
    messagebox.showinfo("Success", "Book added successfully!")


def clear_all():
    """Clear: empty EVERY window - entries, display area, chat (2 marks)."""
    for box in (isbn_entry, title_entry, author_entry, year_entry,
                chat_entry):
        box.delete(0, tk.END)
    display_label.config(text="")
    answer_label.config(text="")


def display_books():
    """Display Books: show every stored book (3 marks)."""
    cursor.execute("SELECT isbn, title, author, year FROM Books")
    lines = [f"ISBN: {i}, Title: {t}, Author: {a}, Year: {y}"
             for i, t, a, y in cursor.fetchall()]     # list comprehension
    display_label.config(text="\n".join(lines))        # one line per book


def ask_librarian():
    """Ask Librarian button: send the typed question to the function."""
    answer_label.config(text=virtual_librarian(chat_entry.get()))


# ------------------------------------------------------------- THE WINDOW
root = tk.Tk()
root.title("Library Management System")

for row_number, name in enumerate(["ISBN", "Title", "Author", "Year"]):
    tk.Label(root, text=name).grid(row=row_number, column=0, padx=10)
isbn_entry = tk.Entry(root, width=30)
title_entry = tk.Entry(root, width=30)
author_entry = tk.Entry(root, width=30)
year_entry = tk.Entry(root, width=30)
for row_number, box in enumerate([isbn_entry, title_entry, author_entry,
                                  year_entry]):
    box.grid(row=row_number, column=1, pady=2)

tk.Button(root, text="Save", command=save_book).grid(row=4, column=0)
tk.Button(root, text="Clear", command=clear_all).grid(row=4, column=1)
tk.Button(root, text="Display Books",
          command=display_books).grid(row=5, column=0, columnspan=2)
tk.Label(root, text="Display Area").grid(row=6, column=0, columnspan=2)
display_label = tk.Label(root, text="", justify="center")
display_label.grid(row=7, column=0, columnspan=2)

chat_entry = tk.Entry(root, width=50)
chat_entry.grid(row=8, column=0, columnspan=2, pady=10)
tk.Button(root, text="Ask Librarian",
          command=ask_librarian).grid(row=9, column=0, columnspan=2)
answer_label = tk.Label(root, text="", wraplength=350)
answer_label.grid(row=10, column=0, columnspan=2, pady=5)

if __name__ == "__main__":
    root.mainloop()
    conn.close()
