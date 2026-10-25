# -*- coding: utf-8 -*-
"""
Programming and Systems Development - Final Lab Exam (Dec 2024) - Python Part
Corner-shop sales: pandas -> matplotlib -> SQLite -> PyTorch

Needs sales_data.csv in the SAME folder as this script.
Run:  python 2024_sales_sqlite_pytorch_solution.py
"""
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

# =====================================================================
# TASK 1a - DATA LOADING AND PREPROCESSING  (9 marks)
# =====================================================================

# --- Load the data (2 marks) -----------------------------------------
df = pd.read_csv("sales_data.csv")
print("Rows, columns:", df.shape)
print(df.head())

# --- Data cleaning: missing values (3 marks) -------------------------
print("\nMissing values per column BEFORE cleaning:")
print(df.isna().sum())

# Text column: a missing product name becomes 'Unknown'
df["Product"] = df["Product"].fillna("Unknown")

# Quantity: a missing quantity can only sensibly be 0
df["Quantity"] = df["Quantity"].fillna(0)

# Price: if Total is known we can WORK OUT the price (Total / Quantity),
# otherwise fall back to 0.  (Never just blindly fill 0 first - that
# would wipe out a real sale when Total is later recalculated.)
df["Price"] = df["Price"].fillna(df["Total"] / df["Quantity"])
df["Price"] = df["Price"].fillna(0)

# Total: a missing total = Quantity * Price
df["Total"] = df["Total"].fillna(df["Quantity"] * df["Price"])

print("\nMissing values per column AFTER cleaning:")
print(df.isna().sum())

# --- Convert Date to a datetime object (2 marks) ---------------------
# The file stores dates as dd/mm/yyyy, so tell pandas the DAY comes first
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# --- Make sure Total = Quantity x Price (2 marks) --------------------
wrong = df["Total"] != df["Quantity"] * df["Price"]
print("\nRows where Total was wrong:", wrong.sum())
df["Total"] = df["Quantity"] * df["Price"]

# --- Remove exact duplicate rows (needed for 'no duplicates' in 2a) ---
before = len(df)
df = df.drop_duplicates()
print("Duplicate rows removed:", before - len(df))

# =====================================================================
# TASK 1b - DATA VISUALISATION  (4 marks)
# =====================================================================

# --- Product sales distribution: bar chart (2 marks) -----------------
qty_per_product = df.groupby("Product")["Quantity"].sum()

plt.figure(figsize=(8, 5))
plt.bar(qty_per_product.index, qty_per_product.values, color="steelblue")
plt.title("Product Sales Distribution")
plt.xlabel("Product")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Sales over time: line plot, months of 2023 only (2 marks) --------
df_2023 = df[df["Date"].dt.year == 2023]                 # keep 2023 rows
monthly_sales = df_2023.groupby(df_2023["Date"].dt.month)["Total"].sum()

plt.figure(figsize=(8, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Total Sales per Month (2023)")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(monthly_sales.index)
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================================
# TASK 2a - DATABASE CREATION AND DATA INSERTION  (9 marks)
# =====================================================================

# --- Create the database SalesDB (2 marks) ---------------------------
conn = sqlite3.connect("SalesDB.db")
cursor = conn.cursor()

# --- Create the table Sales (3 marks) --------------------------------
# UNIQUE(...) is what really stops duplicates - INSERT OR IGNORE alone
# does nothing unless the table has a UNIQUE / PRIMARY KEY rule to break.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sales (
        Date     TEXT,
        Product  TEXT,
        Quantity INTEGER,
        Price    REAL,
        Total    REAL,
        UNIQUE (Date, Product, Quantity, Price, Total)
    )
""")

# --- Insert the cleaned data, no duplicates (4 marks) ----------------
df_db = df.copy()
df_db["Date"] = df_db["Date"].dt.strftime("%Y-%m-%d")    # SQLite wants text

for _, row in df_db.iterrows():
    cursor.execute(
        "INSERT OR IGNORE INTO Sales (Date, Product, Quantity, Price, Total) "
        "VALUES (?, ?, ?, ?, ?)",
        (row["Date"], row["Product"], int(row["Quantity"]),
         float(row["Price"]), float(row["Total"])))
conn.commit()

cursor.execute("SELECT COUNT(*) FROM Sales")
print("\nRows now in Sales table:", cursor.fetchone()[0])

# =====================================================================
# TASK 2b - QUERYING THE DATABASE  (6 marks)
# =====================================================================

# --- Total sales for 2023 (3 marks) ----------------------------------
cursor.execute(
    "SELECT SUM(Total) FROM Sales WHERE strftime('%Y', Date) = '2023'")
total_2023 = cursor.fetchone()[0]
print(f"\nTotal sales in 2023: {total_2023}")

# --- Quantity sold per product in 2023, biggest first (3 marks) -------
cursor.execute("""
    SELECT Product, SUM(Quantity) AS TotalQty
    FROM Sales
    WHERE strftime('%Y', Date) = '2023'
    GROUP BY Product
    ORDER BY TotalQty DESC
""")
print("\nProduct sales summary for 2023:")
for product, qty in cursor.fetchall():
    print(f"  {product:<15} {qty}")

conn.close()


# =====================================================================
# TASK 3 - BASIC NEURAL NETWORK WITH PYTORCH  (12 marks)
# =====================================================================

# --- Define the network (part of 3a) ---------------------------------
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()                  # set up the nn.Module machinery
        self.fc1 = nn.Linear(10, 5)         # 10 input features -> 5 neurons
        self.fc2 = nn.Linear(5, 3)          # 5 -> 3 neurons
        self.fc3 = nn.Linear(3, 1)          # 3 -> 1 output neuron

    def forward(self, x):                   # how data flows through
        x = torch.relu(self.fc1(x))         # hidden layer 1 + ReLU
        x = torch.relu(self.fc2(x))         # hidden layer 2 + ReLU
        x = torch.sigmoid(self.fc3(x))      # output layer + Sigmoid
        return x


# --- 3a: model, loss, optimiser (4 marks) ----------------------------
model = SimpleNN()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# --- 3b: synthetic data (2 marks) ------------------------------------
data = torch.randn(100, 10)      # 100 samples, 10 features each
target = torch.randn(100, 1)     # 100 target values (shape matches output)

# --- 3c: train for 20 epochs, record the loss (3 marks) --------------
losses = []
for epoch in range(20):
    optimizer.zero_grad()                # 1. clear old gradients
    output = model(data)                 # 2. forward pass
    loss = criterion(output, target)     # 3. how wrong are we?
    loss.backward()                      # 4. backpropagation
    optimizer.step()                     # 5. update the weights
    losses.append(loss.item())           # remember the loss as a number
    print(f"Epoch {epoch + 1:2d}/20  loss = {loss.item():.4f}")

# --- 3d: plot the loss (3 marks) -------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(range(1, 21), losses, marker="o")
plt.title("Training Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss (MSE)")
plt.grid(True)
plt.tight_layout()
plt.show()
