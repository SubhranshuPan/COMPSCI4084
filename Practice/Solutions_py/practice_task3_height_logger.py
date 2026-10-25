# -*- coding: utf-8 -*-
"""
Practice Exam Task 3 - Student Height Logger
(CSV files + pandas + numpy + matplotlib)

Run it from the folder where you want heights.csv to live.
Test input to type:  Amy 165 Ben 172 Ali 166 Yin 180 Mohammed 170 Gus 182 q
"""
import csv                       # standard library: read/write csv rows
import os.path                   # os.path.exists() = "is this file there?"
import pandas as pd              # DataFrame = spreadsheet in memory
import numpy as np               # fast maths: mean / min / max
import matplotlib.pyplot as plt  # drawing the histogram

CSV_FILE = "heights.csv"             # one place to change the file names
SUMMARY_FILE = "height_summary.txt"


# ---------------------------------------------------------------------
# Task 1 - CSV file setup
# ---------------------------------------------------------------------
def setup_csv(filename):
    """Create the csv with a header row if missing, else say we append."""
    if not os.path.exists(filename):         # first run (or file deleted)
        with open(filename, "w", newline="") as f:   # "w" = brand new file
            writer = csv.writer(f)
            writer.writerow(["Name", "Height"])      # header row
        print(f"{filename} was created with columns: Name, Height")
    else:                                    # file already there: keep it
        print(f"{filename} already exists and is open for appending")


# ---------------------------------------------------------------------
# Task 2 - Data entry
# ---------------------------------------------------------------------
def enter_data(filename):
    """Ask for name/height pairs until the user types 'q' as the name."""
    print("\n=== Task 2: Data Entry ===")
    with open(filename, "a", newline="") as f:       # "a" = add to the end
        writer = csv.writer(f)
        name = input("Enter name (or 'q' to quit): ").strip()
        while name.lower() != "q":                   # 'q' or 'Q' stops
            try:
                height = int(input("Enter height (cm): "))   # whole cm
                if height <= 0:                      # sanity check
                    print("Height must be a positive whole number.")
                elif name == "":                     # blank name = invalid
                    print("Name cannot be empty.")
                else:
                    writer.writerow([name, height])  # valid record saved
            except ValueError:                       # e.g. user typed 'abc'
                print("Invalid height - please enter a whole number.")
            name = input("Enter name (or 'q' to quit): ").strip()
    print(f"\nData saved to {filename}")


# ---------------------------------------------------------------------
# Task 3 - Summary statistics
# ---------------------------------------------------------------------
def summarise(filename, summary_filename):
    """Read the csv with pandas, print + save the summary, return the df."""
    print("\n=== Task 3: Summary Statistics ===")
    df = pd.read_csv(filename)                       # whole file -> table
    if df.empty:                                     # header only, no rows
        print("No records yet, nothing to summarise.")
        return df
    heights = df["Height"].to_numpy()                # column -> numpy array
    total = len(df)                                  # number of rows
    average = np.mean(heights)
    smallest = np.min(heights)
    largest = np.max(heights)

    lines = [                                        # build text once ...
        f"Total records: {total}",
        f"Average height: {average:.1f} cm",
        f"Minimum height: {smallest} cm",
        f"Maximum height: {largest} cm",
    ]
    for line in lines:                               # ... print it ...
        print(line)
    with open(summary_filename, "w") as f:           # ... and save it
        f.write("\n".join(lines) + "\n")
    print(f"Summary saved to {summary_filename}")
    return df


# ---------------------------------------------------------------------
# Task 4 - Visualisation
# ---------------------------------------------------------------------
def plot_histogram(df):
    """Histogram of the heights with the required title and labels."""
    if df.empty:                                     # nothing to draw
        return
    plt.hist(df["Height"], bins=5, edgecolor="black")
    plt.title("Height Distribution")
    plt.xlabel("Height (cm)")
    plt.ylabel("Frequency")
    plt.show()


# ---------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------
def main():
    print("=== Task 1: CSV File Setup ===")
    setup_csv(CSV_FILE)
    enter_data(CSV_FILE)
    df = summarise(CSV_FILE, SUMMARY_FILE)
    print("\n=== Task 4: Visualisation ===")
    plot_histogram(df)


main()
