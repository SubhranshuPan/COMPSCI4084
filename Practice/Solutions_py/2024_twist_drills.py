# -*- coding: utf-8 -*-
"""
TWIST DRILLS for the 2024 sales paper: the 'what if the examiner changes
the question slightly?' variations.  Each drill is short and independent.
Needs sales_data.csv in the same folder.  Run: python 2024_twist_drills.py
"""
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

# ---- shared set-up: the cleaned DataFrame + a SQLite database ----------
df = pd.read_csv("sales_data.csv")
df["Product"] = df["Product"].fillna("Unknown")
df["Price"] = df["Price"].fillna(df["Total"] / df["Quantity"])
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Total"] = df["Quantity"] * df["Price"]
df = df.drop_duplicates()

conn = sqlite3.connect(":memory:")               # throw-away database
cursor = conn.cursor()
cursor.execute("""CREATE TABLE Sales (Date TEXT, Product TEXT, Quantity INTEGER,
                  Price REAL, Total REAL,
                  UNIQUE (Date, Product, Quantity, Price, Total))""")
db_df = df.copy()
db_df["Date"] = db_df["Date"].dt.strftime("%Y-%m-%d")
cursor.executemany("INSERT OR IGNORE INTO Sales VALUES (?, ?, ?, ?, ?)",
                   db_df.itertuples(index=False, name=None))
conn.commit()

# ---- Drill 1: revenue per product, best first (pandas) ------------------
revenue = df.groupby("Product")["Total"].sum().sort_values(ascending=False)
print("1) Revenue per product:\n", revenue, sep="")
print("   Best seller:", revenue.idxmax(), "->", revenue.max())

# ---- Drill 2: average price per product (pandas) -----------------------
print("\n2) Average price:\n", df.groupby("Product")["Price"].mean().round(2),
      sep="")

# ---- Drill 3: add Month and Year columns, filter with a condition -------
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
big_sales = df[(df["Year"] == 2023) & (df["Total"] > 100)]   # & not 'and'
print("\n3) 2023 sales over 100:", len(big_sales), "rows")

# ---- Drill 4: SQL - sales per month, all years, in date order ----------
cursor.execute("""SELECT strftime('%Y-%m', Date) AS Month, SUM(Total)
                  FROM Sales GROUP BY Month ORDER BY Month""")
print("\n4) Sales per month (first 3):", cursor.fetchall()[:3])

# ---- Drill 5: SQL with a VARIABLE year (safe ? placeholder) ------------
year = 2023
cursor.execute("SELECT COUNT(*), SUM(Total) FROM Sales "
               "WHERE strftime('%Y', Date) = ?", (str(year),))
print("\n5) Rows and total for", year, ":", cursor.fetchone())

# ---- Drill 6: SQL - the single best product in 2023 (LIMIT 1) -----------
cursor.execute("""SELECT Product, SUM(Total) AS Revenue FROM Sales
                  WHERE strftime('%Y', Date) = '2023'
                  GROUP BY Product ORDER BY Revenue DESC LIMIT 1""")
print("\n6) Best product 2023:", cursor.fetchone())

# ---- Drill 7: SQL result straight into a DataFrame ---------------------
summary = pd.read_sql_query(
    "SELECT Product, SUM(Quantity) AS TotalQty FROM Sales "
    "GROUP BY Product ORDER BY TotalQty DESC", conn)
print("\n7) read_sql_query gives a DataFrame:\n", summary, sep="")

# ---- Drill 8: whole DataFrame -> SQLite in one line (to_sql) -----------
df[["Date", "Product", "Quantity", "Price", "Total"]].to_sql(
    "Sales2", conn, if_exists="replace", index=False)
print("\n8) to_sql rows:", cursor.execute(
    "SELECT COUNT(*) FROM Sales2").fetchone()[0])

# ---- Drill 9: pie chart + two charts side by side ----------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
revenue.plot(kind="bar", ax=left, title="Revenue per product")
left.set_ylabel("Revenue")
right.pie(revenue.values, labels=revenue.index, autopct="%1.1f%%")
right.set_title("Share of revenue")
plt.tight_layout()
plt.show()

# ---- Drill 10: save the cleaned data back to a CSV ---------------------
df.to_csv("cleaned_sales.csv", index=False)      # index=False: no 0,1,2 col
print("\n10) cleaned_sales.csv written")

# ---- Drill 11: PyTorch with nn.Sequential, 8 -> 4 -> 1, BCE + Adam ------
torch.manual_seed(0)                             # same numbers every run
X = torch.randn(200, 8)
y = (X.sum(dim=1, keepdim=True) > 0).float()     # a LEARNABLE target 0/1
net = nn.Sequential(nn.Linear(8, 4), nn.ReLU(),
                    nn.Linear(4, 1), nn.Sigmoid())
loss_fn = nn.BCELoss()
opt = optim.Adam(net.parameters(), lr=0.05)
history = []
for epoch in range(30):
    opt.zero_grad()
    loss = loss_fn(net(X), y)
    loss.backward()
    opt.step()
    history.append(loss.item())
accuracy = ((net(X) > 0.5).float() == y).float().mean().item()
print(f"\n11) loss {history[0]:.3f} -> {history[-1]:.3f}, "
      f"accuracy {accuracy:.0%}")
