# import numpy as np 

# a = np.array([10, 20, 30, 40, 50])
# m = np.arange(1, 10).reshape(3,3)
# print(a.shape, m.shape, m.ndim, a.dtype)

# z = np.zeros(3)
# o = np.ones((2, 2))
# f = np.full(3, 5)
# r = np.arange(0, 10, 2)

# # print(a[0], a[-1], a[1:4], a[::2])
# # print(m[1, 2], m[0], m[:, 0], m[1, :])

# # print(m[0:2, 1:3])
# # print(m[-2:], m[:, :2])

# mask = a > 25
# print(a[mask])
# b = a.copy()
# b[b <= 20] = 0
# print(b)
# print(a)

# print(a[[0, 2, 4]])
# g = np.arange(1, 17).reshape(4,4)
# print(g[[0, 1, 2, 3], [0, 2, 3, 1]])

"""
COMPSCI4084 - practical assessment OPERATION DRILLS (one function per card).

Companion to Exam_Prep_Pack/Topics/T9_Checklist_Operation_Cards.md.
Each card_NN_*() function is SELF-CONTAINED: it builds its own tiny data in a
temporary folder (deleted afterwards - nothing is left in the project), runs
ONE checklist operation, and asserts that it worked.

Run everything :  python practical_operation_drills.py
Run one card   :  python -c "import practical_operation_drills as d; d.card_05_merge()"
Headless plots :  MPLBACKEND=Agg python practical_operation_drills.py
                  (otherwise each plot card opens a window - close it to go on)
Needs pandas, matplotlib; the PyTorch cards (20-27) also need torch
(they are reported as SKIP if torch is not installed).
"""
import contextlib
import csv
import functools
import os
import sqlite3
import sys
import tempfile
import traceback
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ----------------------------------------------------------------------------
# Helpers (the exam does NOT need these - they only build tiny test data)
# ----------------------------------------------------------------------------
SALES_CSV = """Date,Product,Quantity,Price
2023-01-05,Pen,10,1.5
2023-01-06,Book,2,12.0
2023-01-06,Book,2,12.0
2023-02-01,Bag,1,30.0
2023-02-03,Pen,5,1.5
2023-03-09,Cap,3,8.0
"""

PRODUCTS_CSV = """Product,Category
Pen,Stationery
Book,Stationery
Bag,Accessories
Ink,Stationery
"""


def in_tempdir(func):
    """Run the card inside a throw-away folder, then delete it."""
    @functools.wraps(func)
    def wrapper():
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                func()
            finally:
                os.chdir(old)
    return wrapper


def write_sales_csv():
    Path("sales.csv").write_text(SALES_CSV)


def write_products_csv():
    Path("products.csv").write_text(PRODUCTS_CSV)


def make_shop_db():
    """Create shop.db with table sales (6 rows) - the state after card 14."""
    write_sales_csv()
    conn = sqlite3.connect("shop.db")
    pd.read_csv("sales.csv").to_sql("sales", conn, index=False, if_exists="replace")
    conn.close()


def make_xy():
    """Synthetic data as in card 23: X (100, 3), y (100, 1)."""
    import torch
    torch.manual_seed(42)
    X = torch.randn(100, 3)
    w = torch.tensor([[2.0], [-1.0], [0.5]])
    y = X @ w + 1.0 + 0.1 * torch.randn(100, 1)
    return X, y


# ----------------------------------------------------------------------------
# PANDAS (cards 1-7)
# ----------------------------------------------------------------------------
@in_tempdir
def card_01_load_csv():
    write_sales_csv()
    # --- card code ---
    df = pd.read_csv("sales.csv")
    print(df.head())
    print(df.dtypes)
    # --- check ---
    assert list(df.columns) == ["Date", "Product", "Quantity", "Price"]
    assert len(df) == 6


@in_tempdir
def card_02_shape():
    write_sales_csv()
    df = pd.read_csv("sales.csv")
    # --- card code ---
    print(df.shape)                    # (6, 4)  -> (rows, columns)
    rows, cols = df.shape
    print(rows, cols, len(df))
    # --- check ---
    assert df.shape == (6, 4) and rows == 6 and cols == 4 and len(df) == 6


@in_tempdir
def card_03_find_duplicates():
    write_sales_csv()
    df = pd.read_csv("sales.csv")
    # --- card code ---
    print(df.duplicated().sum())
    print(df[df.duplicated(keep=False)])
    print(df.duplicated(subset=["Product"]).sum())   # 2  repeated Products
    # --- check ---
    assert df.duplicated().sum() == 1
    assert len(df[df.duplicated(keep=False)]) == 2
    assert df.duplicated(subset=["Product"]).sum() == 2


@in_tempdir
def card_04_drop_duplicates():
    write_sales_csv()
    df = pd.read_csv("sales.csv")
    # --- card code ---
    clean = df.drop_duplicates()                      # whole row must match
    by_key = df.drop_duplicates(subset=["Product"], keep="first")
    clean = clean.reset_index(drop=True)
    print(df.shape, clean.shape, by_key.shape)      # (6, 4) (5, 4) (4, 4)
    # --- check ---
    assert df.shape == (6, 4)                         # original untouched
    assert clean.shape == (5, 4) and clean.duplicated().sum() == 0
    assert by_key.shape == (4, 4)
    assert list(clean.index) == [0, 1, 2, 3, 4]


@in_tempdir
def card_05_merge():
    write_sales_csv()
    write_products_csv()
    # --- card code ---
    sales = pd.read_csv("sales.csv")
    products = pd.read_csv("products.csv")
    inner = sales.merge(products, on="Product", how="inner")
    left = pd.merge(sales, products, on="Product", how="left", indicator=True)
    print(sales.shape, products.shape, inner.shape, left.shape)
    print(left["_merge"].value_counts())
    # --- check ---
    assert sales.shape == (6, 4) and products.shape == (4, 2)
    assert inner.shape == (5, 5)          # Cap has no match -> dropped
    assert left.shape == (6, 6)           # Cap kept (Category NaN) + _merge
    assert (left["_merge"] == "left_only").sum() == 1
    assert left["Category"].isna().sum() == 1


@in_tempdir
def card_06_select_filter():
    write_sales_csv()
    df = pd.read_csv("sales.csv")
    # --- card code ---
    two = df[["Product", "Price"]]                                   # 2 columns
    big = df[df["Quantity"] > 2]                                     # one condition
    both = df[(df["Product"] == "Pen") & (df["Price"] > 1)]          # AND
    either = df[(df["Product"] == "Bag") | (df["Quantity"] >= 3)]    # OR
    sub = df.loc[df["Price"] > 10, ["Product", "Price"]]             # rows + columns
    pick = df[df["Product"].isin(["Pen", "Cap"])]                    # in a list
    # --- check ---
    assert two.shape == (6, 2) and big.shape == (3, 4)
    assert both.shape == (2, 4) and either.shape == (4, 4)
    assert sub.shape == (3, 2) and pick.shape == (3, 4)


@in_tempdir
def card_07_save_csv():
    write_sales_csv()
    df = pd.read_csv("sales.csv")
    clean = df.drop_duplicates()
    # --- card code ---
    clean.to_csv("clean_sales.csv", index=False)
    back = pd.read_csv("clean_sales.csv")
    print(back.shape)                               # (5, 4)
    # --- check ---
    assert back.shape == (5, 4)
    assert "Unnamed: 0" not in back.columns
    assert Path("clean_sales.csv").exists()


# ----------------------------------------------------------------------------
# MATPLOTLIB (cards 8-12) - checks run BEFORE plt.show()
# ----------------------------------------------------------------------------
@in_tempdir
def card_08_scatter():
    # --- card code ---
    hours = [1, 2, 3, 4, 5, 6]
    marks = [48, 55, 61, 70, 74, 85]
    plt.scatter(hours, marks)
    plt.title("Study time vs marks")
    plt.xlabel("Hours studied")
    plt.ylabel("Mark (%)")
    # --- check ---
    ax = plt.gca()
    assert len(ax.collections) == 1 and len(ax.lines) == 0   # dots, no line
    assert ax.get_title() == "Study time vs marks"
    assert ax.get_xlabel() == "Hours studied" and ax.get_ylabel() == "Mark (%)"
    # --- card code ---
    plt.show()


@in_tempdir
def card_09_line():
    # --- card code ---
    months = ["Jan", "Feb", "Mar", "Apr"]
    total = [120, 150, 90, 180]
    plt.plot(months, total, marker="o")
    plt.title("Monthly sales")
    plt.xlabel("Month")
    plt.ylabel("Total sales")
    # --- check ---
    ax = plt.gca()
    assert len(ax.lines) == 1 and list(ax.lines[0].get_ydata()) == total
    assert ax.get_title() == "Monthly sales"
    assert ax.get_xlabel() == "Month" and ax.get_ylabel() == "Total sales"
    # --- card code ---
    plt.show()


@in_tempdir
def card_10_bar():
    write_sales_csv()
    # --- card code ---
    df = pd.read_csv("sales.csv")
    totals = df.groupby("Product")["Quantity"].sum()     # index = Product
    plt.bar(totals.index, totals.values)
    plt.title("Quantity sold per product")
    plt.xlabel("Product")
    plt.ylabel("Total quantity")
    # --- check ---
    ax = plt.gca()
    assert len(ax.patches) == 4                           # Bag Book Cap Pen
    assert [p.get_height() for p in ax.patches] == [1, 4, 3, 15]
    assert ax.get_title() == "Quantity sold per product"
    assert ax.get_xlabel() == "Product" and ax.get_ylabel() == "Total quantity"
    # --- card code ---
    plt.show()


@in_tempdir
def card_11_box():
    # --- card code ---
    group_a = [55, 60, 62, 65, 70, 98]
    group_b = [40, 52, 58, 61, 63, 66]
    plt.boxplot([group_a, group_b])                 # one box per list
    plt.xticks([1, 2], ["A", "B"])                  # name the boxes (works on every version)
    plt.title("Marks by group")
    plt.xlabel("Group")
    plt.ylabel("Mark (%)")
    # --- check ---
    ax = plt.gca()
    names = [t.get_text() for t in ax.get_xticklabels()]
    assert names == ["A", "B"], names
    assert len(ax.lines) > 0                              # whiskers, medians
    assert ax.get_title() == "Marks by group"
    assert ax.get_xlabel() == "Group" and ax.get_ylabel() == "Mark (%)"
    # older-matplotlib-safe way to name the boxes (works on every version)
    plt.figure()
    plt.boxplot([group_a, group_b])
    plt.xticks([1, 2], ["A", "B"])
    assert [t.get_text() for t in plt.gca().get_xticklabels()] == ["A", "B"]
    plt.figure(1)
    # --- card code ---
    plt.show()


@in_tempdir
def card_12_titles_labels():
    # --- card code ---
    plt.plot([1, 2, 3], [2, 4, 8], label="trial 1")
    plt.title("Growth")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.legend()
    # --- check ---
    ax = plt.gca()
    assert (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == ("Growth", "Step", "Value")
    # --- card code ---
    # object style (same result): fig, ax = plt.subplots(); ax.set_title(...)
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [2, 4, 8])
    ax.set_title("Growth")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    # --- check ---
    assert (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == ("Growth", "Step", "Value")
    # --- card code ---
    plt.show()


# ----------------------------------------------------------------------------
# SQLITE (cards 13-19)
# ----------------------------------------------------------------------------
@in_tempdir
def card_13_create_connect():
    # --- card code ---
    conn = sqlite3.connect("shop.db")      # creates the file if missing
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sales "
                "(Product TEXT, Quantity INTEGER, Price REAL)")
    conn.commit()
    print(cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    conn.close()
    # --- check ---
    assert Path("shop.db").exists()
    chk = sqlite3.connect("shop.db")
    assert chk.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() == [("sales",)]
    chk.close()


@in_tempdir
def card_14_dataframe_to_table():
    write_sales_csv()
    # --- card code ---
    df = pd.read_csv("sales.csv")
    conn = sqlite3.connect("shop.db")
    df.to_sql("sales", conn, index=False, if_exists="replace")
    print(pd.read_sql_query("SELECT COUNT(*) AS n FROM sales", conn))
    conn.close()
    # --- check ---
    chk = sqlite3.connect("shop.db")
    assert chk.execute("SELECT COUNT(*) FROM sales").fetchone() == (6,)
    assert [r[1] for r in chk.execute("PRAGMA table_info(sales)")] == \
        ["Date", "Product", "Quantity", "Price"]          # no 'index' column
    chk.close()


@in_tempdir
def card_15_select_where_order():
    make_shop_db()
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    # --- card code ---
    cur.execute("SELECT Product, Quantity FROM sales "
                "WHERE Quantity >= 3 ORDER BY Quantity DESC")
    rows = cur.fetchall()
    print(rows)                       # [('Pen', 10), ('Pen', 5), ('Cap', 3)]
    # --- check ---
    assert rows == [("Pen", 10), ("Pen", 5), ("Cap", 3)]
    cur.execute("SELECT Product FROM sales WHERE Product = 'Pen' AND Price > 1")
    assert len(cur.fetchall()) == 2
    cur.execute("SELECT Product FROM sales ORDER BY Price ASC, Product")
    assert cur.fetchall()[0] == ("Pen",)
    conn.close()


@in_tempdir
def card_16_update_rowcount():
    make_shop_db()
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    # --- card code ---
    cur.execute("UPDATE sales SET Price = ? WHERE Product = ?", (2.0, "Pen"))
    print(cur.rowcount)     # 2 rows changed
    conn.commit()
    # --- check ---
    assert cur.rowcount == 2
    cur.execute("SELECT Price FROM sales WHERE Product = ?", ("Pen",))
    assert cur.fetchall() == [(2.0,), (2.0,)]
    cur.execute("UPDATE sales SET Price = ? WHERE Product = ?", (9.0, "Nothing"))
    assert cur.rowcount == 0          # no match -> 0, not an error
    conn.close()


@in_tempdir
def card_17_parameterised_query():
    make_shop_db()
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    # --- card code ---
    name = "Pen"
    min_qty = 6
    cur.execute("SELECT Product, Quantity FROM sales "
                "WHERE Product = ? AND Quantity >= ?", (name, min_qty))   # tuple
    print(cur.fetchall())             # [('Pen', 10)]
    cur.execute("SELECT * FROM sales WHERE Product = ?", (name,))        # 1 value
    print(len(cur.fetchall()))        # 2
    # --- check ---
    cur.execute("SELECT Product, Quantity FROM sales "
                "WHERE Product = ? AND Quantity >= ?", (name, min_qty))
    assert cur.fetchall() == [("Pen", 10)]
    cur.execute("SELECT * FROM sales WHERE Product = ?", ("x' OR '1'='1",))
    assert cur.fetchall() == []       # a nasty string is just a harmless value
    conn.close()


@in_tempdir
def card_18_commit():
    make_shop_db()
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    # --- card code ---
    cur.execute("UPDATE sales SET Quantity = ? WHERE Product - ?", (99, "Bag"))
    other = sqlite3.connect("shop.db")                    # a second "viewer"
    print(other.execute("SELECT Quantity FROM sales WHERE Product='Bag'").fetchone())  # (1,)
    conn.commit()                                         # now it is saved
    print(other.execute("SELECT Quantity FROM sales WHERE Product='Bag'").fetchone())  # (99,)
    conn.close()
    other.close()
    # --- check ---
    chk = sqlite3.connect("shop.db")
    assert chk.execute("SELECT Quantity FROM sales WHERE Product='Bag'").fetchone() == (99,)
    chk.close()
    # without commit(), closing throws the change away
    c2 = sqlite3.connect("shop.db")
    c2.execute("UPDATE sales SET Quantity = 7 WHERE Product = 'Bag'")
    c2.close()
    chk = sqlite3.connect("shop.db")
    assert chk.execute("SELECT Quantity FROM sales WHERE Product='Bag'").fetchone() == (99,)
    chk.close()


@in_tempdir
def card_19_fetch_export_csv():
    make_shop_db()
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    # --- card code ---
    cur.execute("SELECT Product, Quantity FROM sales ORDER BY Quantity DESC")
    rows = cur.fetchall()                              # list of tuples
    cols = [d[0] for d in cur.description]             # column names
    pd.DataFrame(rows, columns=cols).to_csv("result.csv", index=False)
    pd.read_sql_query("SELECT * FROM sales", conn).to_csv("all.csv", index=False)
    with open("result2.csv", "w", newline="") as f:    # csv module version
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    conn.close()
    # --- check ---
    assert cols == ["Product", "Quantity"] and len(rows) == 6
    assert pd.read_csv("result.csv").shape == (6, 2)
    assert pd.read_csv("all.csv").shape == (6, 4)
    assert pd.read_csv("result2.csv").equals(pd.read_csv("result.csv"))
    assert pd.read_csv("result.csv")["Quantity"].tolist() == [10, 5, 3, 2, 2, 1]


# ----------------------------------------------------------------------------
# PYTORCH (cards 20-27)
# ----------------------------------------------------------------------------
@in_tempdir
def card_20_seed():
    # --- card code ---
    import torch
    torch.manual_seed(42)
    a = torch.randn(3)
    torch.manual_seed(42)              # same seed again ...
    b = torch.randn(3)
    print(torch.equal(a, b))           # True -> identical numbers
    # --- check ---
    assert torch.equal(a, b)
    c = torch.randn(3)                 # no re-seed -> different numbers
    assert not torch.equal(a, c)


@in_tempdir
def card_21_nn_module():
    # --- card code ---
    import torch
    import torch.nn as nn

    class Net(nn.Module):
        def __init__(self):
            super().__init__()                 # MUST be first
            self.fc1 = nn.Linear(3, 8)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(8, 1)

        def forward(self, x):
            return self.fc2(self.relu(self.fc1(x)))

    model = Net()
    print(model(torch.randn(5, 3)).shape)      # torch.Size([5, 1])
    # --- check ---
    assert model(torch.randn(5, 3)).shape == (5, 1)
    assert len(list(model.parameters())) == 4  # 2 weights + 2 biases


@in_tempdir
def card_22_linear_relu():
    # --- card code ---
    import torch
    import torch.nn as nn
    lin = nn.Linear(3, 8)                      # 3 numbers in, 8 numbers out
    x = torch.tensor([[1.0, -2.0, 0.5]])       # shape (1, 3)
    h = lin(x)                                 # shape (1, 8)
    r = nn.ReLU()(h)                           # negatives -> 0
    print(lin.weight.shape, lin.bias.shape, h.shape)
    print((r >= 0).all())                      # tensor(True)
    # --- check ---
    assert tuple(lin.weight.shape) == (8, 3) and tuple(lin.bias.shape) == (8,)
    assert tuple(h.shape) == (1, 8)
    assert torch.equal(r, h.clamp(min=0)) and bool((r >= 0).all())
    seq = nn.Sequential(nn.Linear(3, 8), nn.ReLU(), nn.Linear(8, 1))
    assert seq(x).shape == (1, 1)


@in_tempdir
def card_23_synthetic_data():
    # --- card code ---
    import torch
    torch.manual_seed(42)                      # seed BEFORE generating
    n, d = 100, 3
    X = torch.randn(n, d)                      # (100, 3)
    w = torch.tensor([[2.0], [-1.0], [0.5]])   # (3, 1)  column!
    b = 1.0
    noise = 0.1 * torch.randn(n, 1)            # (100, 1)
    y = X @ w + b + noise                      # (100, 1)
    print(X.shape, w.shape, y.shape)
    # --- check ---
    assert X.shape == (100, 3) and w.shape == (3, 1) and y.shape == (100, 1)
    resid = y - (X @ w + b)
    assert abs(resid.std().item() - 0.1) < 0.03       # noise really is small
    torch.manual_seed(42)
    assert torch.equal(torch.randn(n, d), X)          # reproducible


@in_tempdir
def card_24_shapes():
    import torch
    import torch.nn as nn
    X, y = make_xy()
    model = nn.Linear(3, 1)
    # --- card code ---
    print(X.shape, y.shape)                    # [100, 3] [100, 1]
    n_samples, n_features = X.shape
    pred = model(X)
    print(pred.shape == y.shape)               # True -> safe for MSELoss
    y_flat = y.squeeze()                       # (100,)  drop the size-1 axis
    y_col = y_flat.reshape(-1, 1)              # (100, 1) back to a column
    # --- check ---
    assert (n_samples, n_features) == (100, 3)
    assert pred.shape == y.shape
    assert y_flat.shape == (100,) and y_col.shape == (100, 1)


@in_tempdir
def card_25_loss_optimiser():
    import torch
    import torch.nn as nn
    X, y = make_xy()
    # --- card code ---
    model = nn.Linear(3, 1)
    loss_fn = nn.MSELoss()                     # continuous target -> MSE
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
    # optimizer = torch.optim.Adam(model.parameters(), lr=0.05)   # alternative
    loss = loss_fn(model(X), y)
    print(loss.item())
    # --- check ---
    assert loss.ndim == 0 and loss.item() > 0
    adam = torch.optim.Adam(model.parameters(), lr=0.05)
    assert len(optimizer.param_groups[0]["params"]) == 2 == len(adam.param_groups[0]["params"])


@in_tempdir
def card_26_training_loop():
    import torch
    import torch.nn as nn
    X, y = make_xy()
    torch.manual_seed(0)
    model = nn.Linear(3, 1)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
    start = loss_fn(model(X), y).item()
    # --- card code ---
    for epoch in range(100):
        pred = model(X)                        # 1 forward pass
        loss = loss_fn(pred, y)                # 2 how wrong?
        optimizer.zero_grad()                  # 3 clear old gradients
        loss.backward()                        # 4 new gradients
        optimizer.step()                       # 5 nudge the weights
    print(loss.item())
    # --- check ---
    assert loss.item() < start / 10
    assert loss.item() < 0.1


@in_tempdir
def card_27_record_plot_loss():
    import torch
    import torch.nn as nn
    X, y = make_xy()
    torch.manual_seed(0)
    model = nn.Linear(3, 1)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
    # --- card code ---
    losses = []
    for epoch in range(100):
        loss = loss_fn(model(X), y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())             # .item() -> plain float
    plt.plot(losses)
    plt.title("Training loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE loss")
    # --- check ---
    ax = plt.gca()
    assert len(losses) == 100 and all(isinstance(v, float) for v in losses)
    assert losses[-1] < losses[0]
    assert len(ax.lines) == 1 and len(ax.lines[0].get_ydata()) == 100
    assert (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == \
        ("Training loss", "Epoch", "MSE loss")
    # --- card code ---
    plt.show()


# ----------------------------------------------------------------------------
# Runner
# ----------------------------------------------------------------------------
def main():
    cards = sorted((n, f) for n, f in globals().items()
                   if n.startswith("card_") and callable(f))
    results = []
    # Headless backends (Agg) warn that show() is a no-op - hide that noise.
    warnings.filterwarnings("ignore", message=".*non-interactive.*")
    for name, func in cards:
        try:
            func()
            results.append((name, "PASS", ""))
        except ImportError as exc:
            results.append((name, "SKIP", str(exc)))
        except Exception:
            results.append((name, "FAIL", traceback.format_exc(limit=3)))
        finally:
            plt.close("all")
    print("\n" + "=" * 60)
    for name, status, info in results:
        print(f"{status}  {name}")
        if status != "PASS" and info:
            print(info)
    n_pass = sum(s == "PASS" for _, s, _ in results)
    print("=" * 60)
    print(f"{n_pass}/{len(results)} cards passed")
    return 0 if all(s != "FAIL" for _, s, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())


