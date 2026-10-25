# -*- coding: utf-8 -*-
"""
Mock A - Campus Cafe orders: pandas -> matplotlib -> SQLite -> PyTorch
Needs cafe_orders.csv in the SAME folder as this script.
Run:  python MockA_solution.py
"""
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

# =====================================================================
# TASK 1a - DATA LOADING AND PREPROCESSING (9 marks)
# =====================================================================

# --- Load the data (2 marks) -----------------------------------------
df = pd.read_csv("cafe_orders.csv")
print("Rows, columns:", df.shape)
print(df.head())

# --- Missing values (2 marks) ----------------------------------------
print("\nMissing values per column BEFORE cleaning:")
print(df.isna().sum())

df["Item"] = df["Item"].fillna("Unknown")          # text: a label
# Quantity = Total / Price when both are known, else 0
df["Quantity"] = df["Quantity"].fillna((df["Total"] / df["Price"]).round())
df["Quantity"] = df["Quantity"].fillna(0).astype(int)   # NaN made it float
# Price = Total / Quantity when possible, else 0
df["Price"] = df["Price"].fillna(df["Total"] / df["Quantity"])
df["Price"] = df["Price"].fillna(0)
# Total = Quantity x Price
df["Total"] = df["Total"].fillna(df["Quantity"] * df["Price"])

print("\nMissing values per column AFTER cleaning:")
print(df.isna().sum())

# --- Remove exact duplicate orders (1 mark) --------------------------
before = len(df)
df = df.drop_duplicates()
print("Duplicate rows removed:", before - len(df))

# --- Convert OrderTime to datetime (2 marks) -------------------------
# Format is year/month/day hour:minute - say so explicitly (no guessing)
df["OrderTime"] = pd.to_datetime(df["OrderTime"], format="%Y/%m/%d %H:%M")

# --- Make sure Total = Quantity x Price (2 marks) --------------------
correct_total = (df["Quantity"] * df["Price"]).round(2)   # round: float dust
wrong = (df["Total"] - correct_total).abs() > 0.005
print("Rows where Total was wrong:", wrong.sum())
df["Total"] = correct_total

# =====================================================================
# TASK 1b - DATA VISUALISATION (4 marks)
# =====================================================================

# --- Bar chart: total quantity sold per item (2 marks) ---------------
qty_per_item = df.groupby("Item")["Quantity"].sum()

plt.figure(figsize=(8, 5))
plt.bar(qty_per_item.index, qty_per_item.values, color="steelblue")
plt.title("Total Quantity Sold per Item")
plt.xlabel("Item")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Line plot: total sales per month of 2024 (2 marks) --------------
df_2024 = df[df["OrderTime"].dt.year == 2024]               # keep 2024 only
monthly_sales = df_2024.groupby(df_2024["OrderTime"].dt.month)["Total"].sum()

plt.figure(figsize=(8, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Total Sales per Month (2024)")
plt.xlabel("Month")
plt.ylabel("Total Sales (GBP)")
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================================
# TASK 2a - DATABASE CREATION AND DATA INSERTION (9 marks)
# =====================================================================

# --- Create the database CafeDB (2 marks) ----------------------------
conn = sqlite3.connect("CafeDB.db")
cursor = conn.cursor()

# --- Create the table Orders (3 marks) -------------------------------
# UNIQUE(...) is what really stops duplicates; INSERT OR IGNORE needs it
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        OrderTime TEXT,
        Item      TEXT,
        Quantity  INTEGER,
        Price     REAL,
        Total     REAL,
        UNIQUE (OrderTime, Item, Quantity, Price, Total)
    )
""")

# --- Insert the cleaned data, no duplicates (4 marks) ----------------
df_db = df.copy()
# SQLite date functions need  YYYY-MM-DD HH:MM:SS  (hyphens, not slashes)
df_db["OrderTime"] = df_db["OrderTime"].dt.strftime("%Y-%m-%d %H:%M:%S")

for _, row in df_db.iterrows():
    cursor.execute(
        "INSERT OR IGNORE INTO Orders (OrderTime, Item, Quantity, Price, "
        "Total) VALUES (?, ?, ?, ?, ?)",
        (row["OrderTime"], row["Item"], int(row["Quantity"]),
         float(row["Price"]), float(row["Total"])))   # plain Python types
conn.commit()

cursor.execute("SELECT COUNT(*) FROM Orders")
print("\nRows now in Orders table:", cursor.fetchone()[0])

# =====================================================================
# TASK 2b - QUERYING THE DATABASE (6 marks)
# =====================================================================

# --- Total sales for 2024 (3 marks) ----------------------------------
cursor.execute(
    "SELECT ROUND(SUM(Total), 2) FROM Orders "
    "WHERE strftime('%Y', OrderTime) = '2024'")
total_2024 = cursor.fetchone()[0]
print(f"\nTotal sales in 2024: {total_2024:.2f}")

# --- Quantity sold per item in 2024, biggest first (3 marks) ----------
cursor.execute("""
    SELECT Item, SUM(Quantity) AS TotalQty
    FROM Orders
    WHERE strftime('%Y', OrderTime) = '2024'
    GROUP BY Item
    ORDER BY TotalQty DESC, Item
""")
print("\nItem sales summary for 2024:")
for item, qty in cursor.fetchall():
    print(f"  {item:<12} {qty}")

conn.close()


# =====================================================================
# TASK 3 - NEURAL NETWORK WITH PYTORCH (12 marks)
# =====================================================================

# --- Define the network (part of 3a) ---------------------------------
class CafeNN(nn.Module):
    def __init__(self):
        super().__init__()                  # set up nn.Module machinery
        self.fc1 = nn.Linear(6, 8)          # 6 input features -> 8 neurons
        self.fc2 = nn.Linear(8, 4)          # 8 -> 4 neurons
        self.fc3 = nn.Linear(4, 1)          # 4 -> 1 output neuron

    def forward(self, x):                   # how data flows through
        x = torch.relu(self.fc1(x))         # hidden layer 1 + ReLU
        x = torch.relu(self.fc2(x))         # hidden layer 2 + ReLU
        x = torch.sigmoid(self.fc3(x))      # output: a probability 0..1
        return x


# --- 3a: model, loss, optimiser (3 marks) ----------------------------
torch.manual_seed(42)                       # same numbers every run
model = CafeNN()
criterion = nn.BCELoss()                    # binary cross-entropy
optimizer = optim.Adam(model.parameters(), lr=0.01)

# --- 3b: synthetic data (2 marks) ------------------------------------
data = torch.randn(200, 6)                  # 200 samples, 6 features
# learnable rule: label is 1 when x0 + x1 - x2 is positive, else 0
target = (data[:, 0] + data[:, 1] - data[:, 2] > 0).float().unsqueeze(1)

# --- 3c: train for 30 epochs, record the loss (3 marks) --------------
losses = []
for epoch in range(30):
    optimizer.zero_grad()                # 1. clear old gradients
    output = model(data)                 # 2. forward pass
    loss = criterion(output, target)     # 3. how wrong are we?
    loss.backward()                      # 4. backpropagation
    optimizer.step()                     # 5. update the weights
    losses.append(loss.item())           # remember the loss as a number
    print(f"Epoch {epoch + 1:2d}/30  loss = {loss.item():.4f}")

# --- 3d: plot the loss (2 marks) -------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(range(1, 31), losses, marker="o")
plt.title("Training Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss (BCE)")
plt.grid(True)
plt.tight_layout()
plt.show()

# --- 3e: accuracy on the training data (2 marks) ---------------------
with torch.no_grad():                        # no learning, just predicting
    predictions = (model(data) > 0.5).float()      # prob > 0.5 -> class 1
    accuracy = (predictions == target).float().mean().item()
print(f"\nTraining accuracy: {accuracy * 100:.1f}%")
