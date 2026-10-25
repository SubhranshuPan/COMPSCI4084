# -*- coding: utf-8 -*-
"""
Mock B - Module Score Logger (console logger, pandas/numpy, SQLite)
Needs module_scores.csv in the SAME folder as this script (or it creates it).
Run:  python MockB_solution.py
"""
import csv                       # standard library: write csv rows
import os.path                   # os.path.exists() = "is this file there?"
import sqlite3                   # the database
import numpy as np               # fast maths on arrays
import pandas as pd              # DataFrame = spreadsheet in memory
import matplotlib.pyplot as plt  # drawing

CSV_FILE = "module_scores.csv"         # names kept in ONE place
SUMMARY_FILE = "score_summary.txt"
DB_FILE = "ScoresDB.db"


# =====================================================================
# TASK 1 - CONSOLE DATA LOGGER (14 marks)
# =====================================================================

# --- 1a: create the file if missing, otherwise say we append (4) -----
def setup_csv(filename):
    """Create the csv with a header row if missing, else just report."""
    if not os.path.exists(filename):             # first run / file deleted
        with open(filename, "w", newline="") as f:   # "w" = brand new file
            csv.writer(f).writerow(["Student", "Module", "Score", "Hours"])
        print(f"{filename} was created with columns: "
              "Student, Module, Score, Hours")
    else:                                        # file there: keep it
        print(f"{filename} already exists and is open for appending")


# --- 1c: validated number input (5) ----------------------------------
def ask_score():
    """Keep asking until the user types a whole number from 0 to 100."""
    while True:
        try:
            score = int(input("Enter score (0-100): "))
            if 0 <= score <= 100:
                return score                     # good value: leave loop
        except ValueError:                       # e.g. 'abc' or '7.5'
            pass
        print("Invalid score - please enter a whole number from 0 to 100.")


def ask_hours():
    """Keep asking until the user types a positive number (may be decimal)."""
    while True:
        try:
            hours = float(input("Enter study hours: "))
            if hours > 0:
                return hours
        except ValueError:
            pass
        print("Invalid hours - please enter a positive number.")


def ask_text(prompt):
    """Ask for a non-empty text; return it tidy ('maths ' -> 'Maths')."""
    while True:
        text = input(prompt).strip().title()
        if text != "":
            return text
        print("This cannot be empty.")


# --- 1b: the entry loop, append to the file (5) ----------------------
def enter_data(filename):
    """Append records typed by the user until 'q' is typed as the name."""
    print("\n=== Task 1: Data Entry ===")
    with open(filename, "a", newline="") as f:   # "a" = add to the end
        writer = csv.writer(f)
        name = input("Enter student name (or 'q' to quit): ").strip()
        while name.lower() != "q":               # 'q' or 'Q' stops
            if name == "":
                print("This cannot be empty.")
            else:
                module = ask_text("Enter module: ")
                score = ask_score()
                hours = ask_hours()
                writer.writerow([name.title(), module, score, hours])
                print(f"Record saved: {name.title()}, {module}, "
                      f"{score}, {hours}")
            name = input("Enter student name (or 'q' to quit): ").strip()
    print(f"\nData saved to {filename}")


# =====================================================================
# TASK 2 - SUMMARY STATISTICS AND FIGURE (12 marks)
# =====================================================================

# --- 2a: read, remove duplicate rows, count (3) ----------------------
def load_clean(filename):
    df = pd.read_csv(filename)                   # whole file -> table
    before = len(df)
    df = df.drop_duplicates()                    # exact duplicate rows go
    print(f"Records read: {before}, duplicates removed: {before - len(df)}")
    print(f"Total records: {len(df)}")
    print(f"Number of modules: {df['Module'].nunique()}")
    return df


# --- 2b + 2c: numpy statistics, print and save (3 + 2) ---------------
def summarise(df, summary_filename):
    scores = df["Score"].to_numpy()              # column -> numpy array
    lines = [
        f"Total records: {len(df)}",
        f"Mean score:    {np.mean(scores):.2f}",
        f"Median score:  {np.median(scores):.2f}",
        f"Std deviation: {np.std(scores):.2f}",   # np.std: ddof=0
        f"Minimum score: {np.min(scores)}",
        f"Maximum score: {np.max(scores)}",
    ]
    print("\n=== Task 2: Summary Statistics ===")
    for line in lines:
        print(line)
    with open(summary_filename, "w") as f:       # "w": overwrite = same
        f.write("\n".join(lines) + "\n")         # file every run
    print(f"Summary saved to {summary_filename}")


# --- 2d: one figure, two subplots (4) --------------------------------
def make_figure(df):
    means = df.groupby("Module")["Score"].mean()         # mean per module
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.hist(df["Score"], bins=6, edgecolor="black")     # left: histogram
    ax1.set_title("Score Distribution")
    ax1.set_xlabel("Score")
    ax1.set_ylabel("Frequency")

    ax2.bar(means.index, means.values, color="steelblue")  # right: bars
    ax2.set_title("Mean Score per Module")
    ax2.set_xlabel("Module")
    ax2.set_ylabel("Mean score")

    fig.tight_layout()                                   # stop overlaps
    plt.show()


# =====================================================================
# TASK 3 - SQLITE (14 marks)
# =====================================================================

# --- 3a: database + table (4) ----------------------------------------
def create_db():
    conn = sqlite3.connect(DB_FILE)              # creates file if missing
    cursor = conn.cursor()
    # UNIQUE is what really blocks duplicates (INSERT OR IGNORE needs it)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Results (
            Student TEXT,
            Module  TEXT,
            Score   INTEGER,
            Hours   REAL,
            UNIQUE (Student, Module, Score, Hours)
        )
    """)
    return conn, cursor


# --- 3b: insert the csv rows, no duplicates (4) ----------------------
def insert_rows(conn, cursor, df):
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT OR IGNORE INTO Results (Student, Module, Score, Hours) "
            "VALUES (?, ?, ?, ?)",
            (row["Student"], row["Module"], int(row["Score"]),
             float(row["Hours"])))               # int()/float(): not numpy
    conn.commit()                                # save the changes


# --- 3c: three queries (2 + 2 + 2) -----------------------------------
def run_queries(cursor):
    print("\n=== Task 3: Queries ===")
    cursor.execute("SELECT COUNT(*) FROM Results")
    print("Records in Results:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT Module, ROUND(AVG(Score), 2) AS AvgScore
        FROM Results
        GROUP BY Module
        ORDER BY AvgScore DESC
    """)
    print("Average score per module:")
    for module, avg in cursor.fetchall():
        print(f"  {module:<10} {avg:.2f}")

    cursor.execute("""
        SELECT Student, Module, Score
        FROM Results
        ORDER BY Score DESC
        LIMIT 3
    """)
    print("Top 3 scores:")
    for student, module, score in cursor.fetchall():
        print(f"  {student:<8} {module:<10} {score}")


# =====================================================================
# MAIN PROGRAM
# =====================================================================
def main():
    print("=== Task 1: CSV File Setup ===")
    setup_csv(CSV_FILE)
    enter_data(CSV_FILE)

    df = load_clean(CSV_FILE)
    if df.empty:                                 # header only: stop politely
        print("No records yet - nothing to summarise.")
        return
    summarise(df, SUMMARY_FILE)
    make_figure(df)

    conn, cursor = create_db()
    insert_rows(conn, cursor, df)
    run_queries(cursor)
    conn.close()


main()
