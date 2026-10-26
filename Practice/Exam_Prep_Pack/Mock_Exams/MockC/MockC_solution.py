# -*- coding: utf-8 -*-
"""
Mock C - Shop orders: pandas -> matplotlib -> SQLite -> PyTorch
Needs customers.csv and orders.csv in the SAME folder as this script.
Run:  python MockC_solution.py
Each block below is ONE independent operation - learn the operations,
not the whole file.
"""
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

# =====================================================================
# SECTION 1 - PANDAS (12 marks)
# =====================================================================

# --- 1a: load both CSV files (2) -------------------------------------
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")

# --- 1b: check the shape of each DataFrame (1) -----------------------
print("customers shape:", customers.shape)          # (rows, columns)
print("orders shape:   ", orders.shape)

# --- 1c: identify and remove duplicates (3) --------------------------
dup_c = customers.duplicated().sum()                 # True = repeat row
dup_o = orders.duplicated().sum()
print("duplicate customer rows:", dup_c)
print("duplicate order rows:   ", dup_o)
customers = customers.drop_duplicates()              # keeps first copy
orders = orders.drop_duplicates()
print("after removal:", customers.shape, orders.shape)

# --- 1d: merge on the common column CustomerID (3) -------------------
# INNER join: keep only orders whose CustomerID is found in customers
merged = orders.merge(customers, on="CustomerID", how="inner")
print("merged (inner join) shape:", merged.shape)
print("orders with no matching customer:", len(orders) - len(merged))

# --- 1e: select columns and filter rows (2) --------------------------
north_big = merged[(merged["Region"] == "North") & (merged["Amount"] > 50)]
north_big = north_big[["OrderID", "Name", "Region", "Category", "Amount"]]
print("\nNorth orders over 50:", len(north_big), "rows")
print(north_big.head())

# --- 1f: save the merged, cleaned DataFrame to CSV (1) ---------------
merged.to_csv("merged_orders.csv", index=False)      # index=False: no 0,1,2
print("saved merged_orders.csv")

# =====================================================================
# SECTION 2 - MATPLOTLIB (8 marks, 2 per plot)
# =====================================================================

# --- 2a: scatter plot - items in order vs amount ---------------------
plt.figure(figsize=(7, 5))
plt.scatter(merged["Items"], merged["Amount"], alpha=0.7)
plt.title("Order Amount against Number of Items")
plt.xlabel("Items in order")
plt.ylabel("Amount (GBP)")
plt.show()

# --- 2b: line plot - total amount per month --------------------------
months = pd.to_datetime(merged["OrderDate"]).dt.strftime("%Y-%m")
monthly = merged.groupby(months)["Amount"].sum()     # sorted by month
plt.figure(figsize=(8, 5))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Total Order Amount per Month (2024)")
plt.xlabel("Month")
plt.ylabel("Total Amount (GBP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- 2c: bar chart - total amount per category -----------------------
per_cat = merged.groupby("Category")["Amount"].sum()
plt.figure(figsize=(7, 5))
plt.bar(per_cat.index, per_cat.values, color="steelblue")
plt.title("Total Amount per Category")
plt.xlabel("Category")
plt.ylabel("Total Amount (GBP)")
plt.show()

# --- 2d: box plot - amount for each region ---------------------------
regions = sorted(merged["Region"].unique())
groups = [merged.loc[merged["Region"] == r, "Amount"] for r in regions]
plt.figure(figsize=(7, 5))
plt.boxplot(groups)                         # one box per region
plt.xticks(range(1, len(regions) + 1), regions)   # name the boxes (any version)
plt.title("Order Amount by Region")
plt.xlabel("Region")
plt.ylabel("Amount (GBP)")
plt.show()

# =====================================================================
# SECTION 3 - SQLITE (10 marks)
# =====================================================================

# --- 3a: create/connect, store the DataFrame as a table (3) ----------
conn = sqlite3.connect("ShopDB.db")                  # creates if missing
cursor = conn.cursor()                               # the clerk
merged.to_sql("Orders", conn, if_exists="replace", index=False)
# "replace" = start the table afresh every run, so re-running the
# program never duplicates rows (and never discounts twice)
cursor.execute("SELECT COUNT(*) FROM Orders")
print("\nRows stored in Orders:", cursor.fetchone()[0])

# --- 3b: SELECT + WHERE + ORDER BY with ? placeholders (2) -----------
cursor.execute(
    "SELECT OrderID, Name, Category, Amount FROM Orders "
    "WHERE Region = ? AND Amount > ? ORDER BY Amount DESC",
    ("North", 50))
rows = cursor.fetchall()
print("North orders over 50 (biggest first):", len(rows))
for row in rows[:3]:
    print("  ", row)

# --- 3c: UPDATE with ? placeholders, show before/after, commit (3) ---
def books_total():
    cursor.execute("SELECT ROUND(SUM(Amount), 2) FROM Orders "
                   "WHERE Category = ?", ("Books",))
    return cursor.fetchone()[0]

before = books_total()
cursor.execute("UPDATE Orders SET Amount = ROUND(Amount - ?, 2) "
               "WHERE Category = ?", (2.0, "Books"))   # 2 GBP voucher
print("rows updated:", cursor.rowcount)
conn.commit()                                        # save the changes
after = books_total()
print(f"Books total BEFORE: {before}   AFTER: {after}")

# --- 3d: retrieve results and export them to CSV (2) -----------------
cursor.execute("SELECT OrderID, Name, Category, Amount FROM Orders "
               "WHERE Category = ? ORDER BY Amount DESC", ("Books",))
result = cursor.fetchall()
columns = [d[0] for d in cursor.description]         # column names
pd.DataFrame(result, columns=columns).to_csv("books_after_update.csv",
                                             index=False)
print("exported", len(result), "rows to books_after_update.csv")
conn.close()

# =====================================================================
# SECTION 4 - PYTORCH (10 marks)
# =====================================================================

# --- 4a: seed FIRST, then generate y = X @ w + b + noise (3) ---------
torch.manual_seed(42)                       # reproducible every run
N, F = 200, 3                               # samples, features
w = torch.tensor([[2.0], [-1.0], [0.5]])    # true weights, shape (3, 1)
b = 0.7                                     # true bias
X = torch.randn(N, F)                       # inputs
noise = 0.1 * torch.randn(N, 1)             # noise level 0.1
y = X @ w + b + noise                       # continuous target

# --- 4b: shapes of X and y (1) ---------------------------------------
print("\nX shape:", tuple(X.shape), " y shape:", tuple(y.shape))


# --- 4c: the network (2) ---------------------------------------------
class RegNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3, 8)          # 3 features -> 8 neurons
        self.fc2 = nn.Linear(8, 1)          # 8 neurons -> 1 number

    def forward(self, x):
        x = torch.relu(self.fc1(x))         # hidden layer + ReLU
        return self.fc2(x)                  # no activation: any real number


# --- 4d: loss function and optimiser (1) -----------------------------
model = RegNet()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.05)

# --- 4e: training loop, record the loss (2) --------------------------
losses = []
for epoch in range(100):
    optimizer.zero_grad()                   # clear old gradients
    pred = model(X)                         # forward pass
    loss = criterion(pred, y)               # how wrong?
    loss.backward()                         # backpropagation
    optimizer.step()                        # update weights
    losses.append(loss.item())              # remember as a number
    if epoch % 20 == 0 or epoch == 99:
        print(f"Epoch {epoch + 1:3d}/100  loss = {loss.item():.4f}")

# --- 4f: plot the training loss (1) ----------------------------------
plt.figure(figsize=(7, 5))
plt.plot(range(1, 101), losses)
plt.title("Training Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss (MSE)")
plt.grid(True)
plt.show()
