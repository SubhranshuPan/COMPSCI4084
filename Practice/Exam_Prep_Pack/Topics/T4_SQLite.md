# T4 - SQLite with Python (`sqlite3`)

*Covers: connect / cursor / CREATE TABLE / INSERT / SELECT / UPDATE / DELETE, "no duplicates", year filtering with `strftime`, DataFrame <-> database, and the exact 2024 Tasks 2a + 2b. Earns marks in: 2024 Task 2 (15 marks), 2023 Task 1a/1b (ISBN check), 2022 (TravelPrice), 2021 (Users + duplicate usernames).*

---

## 1. What the exam asks

**2024 paper, Python Task 2: Python Database Management [15 marks]** - *"create a database to store and manage the sales data processed in Part 1."*

| Sub-task | Wording | Marks |
|---|---|---|
| 2a | Create an SQLite database named **SalesDB** | 2 |
| 2a | Create a table named **Sales** with appropriate columns (**Date, Product, Quantity, Price, Total**) | 3 |
| 2a | Insert the cleaned data from Part 1 into Sales. **Ensure no duplicate entries are added.** | 4 |
| 2b | Total Sales Calculation: query the **total sales for the year 2023** and display it | 3 |
| 2b | Product Sales Summary: list each product and its **total quantity sold in 2023**, **descending order of quantity** | 3 |

**Older papers (same patterns, shown here WITHOUT tkinter):**
- 2021 Task 1: database `Users`; save username + password; *"should not save duplicated usernames ... check if the username already exists"* [5]; password >= 8 characters AND contains a number [6]; "Clear" and "Display".
- 2022 Task 1b: database `TravelPrice`; save each passenger's age and ticket price; display ages, display prices, display total cost [5]; *"Clear All" deletes everything from the database* [2].
- 2023 Task 1a/1b: database `LibraryDB`; save ISBN/title/author/year; *no duplicate ISBNs*; year between 1450 and now; title and author not empty; then answer "Recommend me a book by [author]" and "When was [title] published" from the database.
- Lab 3 Exercises 17/18 (PhoneBook1, table Names: view / add / search surname / delete by ID); tAPP-3 Problem 1 (`employees` database, `contactDetails` table).

**The data file** (`sales_data.csv`, 151 rows) is deliberately messy:

| Problem | Where | Effect |
|---|---|---|
| Dates are `dd/mm/yyyy` | whole file | need `dayfirst=True`, then convert to `YYYY-MM-DD` text for SQLite |
| Years **2022, 2023, 2024** (29 / 100 / 22 rows) | whole file | the year filter really matters |
| Blank Product (6 rows), blank Price (1), blank Total (3) | e.g. rows for 24/02/2023, 12/03/2023 | clean *before* inserting |
| The week 04/04/2022 to 10/04/2022 appears **twice** | rows 123-129 and 145-151 | 6 exact duplicate rows (the 7th differs only by a blank Product) - the "no duplicates" rule is really tested |

---

## 2. Mental model (analogy)

| Idea | Analogy |
|---|---|
| Database file (`SalesDB.db`) | A **filing cabinet** in your folder. |
| Table (`Sales`) | One **drawer** with ruled index cards: every card has the same boxes (columns). |
| Row | One **index card** (one sale). |
| `sqlite3.connect("x.db")` | **Opening the cabinet** (creating it if it is not there). |
| `cursor = conn.cursor()` | The **clerk**. You hand the clerk written notes (`execute`) and ask them to fetch things. |
| `cursor.execute(sql)` | Handing the clerk a **note** in SQL language. |
| `?` placeholders | A **form with blanks**; the values are slotted in separately and safely. |
| `conn.commit()` | **Saving the form** / stamping "filed". No commit = the change is lost when you close. |
| `conn.close()` | Locking the cabinet and going home. |
| `fetchone()` / `fetchall()` | The clerk hands back **one card** / **the whole pile** (a list of tuples). |
| `UNIQUE` / `PRIMARY KEY` | A **bouncer** at the drawer: "a card with this Date + Product is already in here - rejected." |
| `INSERT OR IGNORE` | "If the bouncer rejects the card, **don't make a fuss** - just drop it." **No bouncer = nothing is ever rejected = nothing is ignored.** |
| `DELETE FROM Sales` | Emptying the drawer (drawer stays). `DROP TABLE` throws the drawer away. |

---

## 3. Copy-paste templates

**3.1 WHEN: start of ANY database task (connect + create table)**
```python
import sqlite3

conn = sqlite3.connect("SalesDB.db")     # creates the file if missing
cursor = conn.cursor()                   # the clerk
cursor.execute("""CREATE TABLE IF NOT EXISTS Sales (
                      Date     TEXT NOT NULL,
                      Product  TEXT NOT NULL,
                      Quantity INTEGER,
                      Price    REAL,
                      Total    REAL,
                      UNIQUE (Date, Product)
                  )""")
```
Data types: `INTEGER` whole numbers, `REAL` decimals, `TEXT` strings **and dates**, `BLOB` raw bytes. `NOT NULL` = must be filled. Key choices: `id INTEGER PRIMARY KEY AUTOINCREMENT` (auto numbers; the lab's phonebook), `username TEXT UNIQUE`, `ISBN TEXT PRIMARY KEY`.

**3.2 WHEN: insert one row (values come from variables / input)**
```python
cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
               (username, password))     # a TUPLE, one ? per value
conn.commit()                            # save
```
Never build the SQL with f-strings (`'{name}'`): a quote in the data (`O'Brien`) breaks it. Use `?`.

**3.3 WHEN: "ensure no duplicates" - the RIGHT way (UNIQUE + OR IGNORE)**
```python
# table created with  UNIQUE (Date, Product)  (template 3.1)
cursor.execute("""INSERT OR IGNORE INTO Sales
                  (Date, Product, Quantity, Price, Total)
                  VALUES (?, ?, ?, ?, ?)""",
               ("2023-01-01", "Chocolate", 5, 10.0, 50.0))
conn.commit()
if cursor.rowcount == 0:                 # 0 = ignored, 1 = inserted
    print("Duplicate - not added")
```
Bouncer in the table (`UNIQUE`/`PRIMARY KEY`) + `OR IGNORE` = silent skip. Without `OR IGNORE`, the same insert raises `sqlite3.IntegrityError: UNIQUE constraint failed: Sales.Date, Sales.Product`; you can catch that instead:
```python
try:
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()
except sqlite3.IntegrityError:
    print("Username already exists!")
```

**3.4 WHEN: "check whether it exists first, then insert" (2021 username, 2023 ISBN)**
```python
def username_exists(cursor, username):
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    return cursor.fetchone() is not None     # None = no matching row
```
Use this when you need a *custom message* or when the table has no UNIQUE column. `(username,)` - the comma makes a one-item tuple.

**3.5 WHEN: reading data back (SELECT)**
```python
cursor.execute("SELECT * FROM Sales")                        # all columns
rows = cursor.fetchall()                 # list of tuples; [] if none
cursor.execute("SELECT * FROM Sales WHERE Price > ? ORDER BY Date DESC",
               (9,))                     # filter + sort (DESC = high->low)
for row in cursor.fetchall():
    print(row)                           # ('2023-01-01', 'Chocolate', ...)
cursor.execute("SELECT COUNT(*), SUM(Total), AVG(Price) FROM Sales")
count, total, average = cursor.fetchone()    # ONE row, unpack it
```
`fetchone()` gives one tuple (or `None` if nothing matched); `fetchall()` gives a list. Aggregates: `COUNT(*)` rows, `SUM(col)`, `AVG(col)`, `MIN`, `MAX`. `SUM` of no rows is `None`, not 0.

**3.6 WHEN: "for the year 2023" / any date part (`strftime`)**
```python
cursor.execute("""SELECT SUM(Total) FROM Sales
                  WHERE strftime('%Y', Date) = '2023'""")
total_2023 = cursor.fetchone()[0]        # [0] = first (only) column
cursor.execute("""SELECT strftime('%m', Date) AS Month, SUM(Total)
                  FROM Sales WHERE strftime('%Y', Date) = ?
                  GROUP BY Month ORDER BY Month""", ("2023",))
```
`strftime('%Y', Date)` returns the year **as TEXT** (so compare with `'2023'`, quoted). `%m` month `01`-`12`, `%d` day. It only works if `Date` is stored as `YYYY-MM-DD` text.

**3.7 WHEN: "total per product / per group, biggest first" (GROUP BY)**
```python
cursor.execute("""SELECT Product, SUM(Quantity) AS TotalQty
                  FROM Sales
                  WHERE strftime('%Y', Date) = '2023'
                  GROUP BY Product
                  ORDER BY TotalQty DESC""")
for product, qty in cursor.fetchall():   # unpack each 2-column tuple
    print(f"Product: {product}, Total Quantity Sold: {qty}")
```
Order of the clauses is fixed: `SELECT ... FROM ... WHERE ... GROUP BY ... ORDER BY`. `WHERE` filters rows *before* grouping.

**3.8 WHEN: change or remove rows (UPDATE / DELETE / "Clear All")**
```python
cursor.execute("UPDATE Sales SET Price = ? WHERE Product = ?",
               (12.0, "Chocolate"))      # ALWAYS keep a WHERE!
cursor.execute("DELETE FROM Names WHERE ID = ?", (2,))   # one record
cursor.execute("DELETE FROM Sales")      # CLEAR ALL rows (table remains)
conn.commit()
print(cursor.rowcount, "row(s) affected")    # count from the last statement
```
`DELETE FROM Sales` with no WHERE deletes every row - that is the "Clear All" button of 2022.

**3.9 WHEN: a whole DataFrame goes into the table - loop version (marked in 2024)**
```python
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")   # Timestamp -> TEXT first!
for index, row in df.iterrows():                  # one row at a time
    cursor.execute("""INSERT OR IGNORE INTO Sales
                      (Date, Product, Quantity, Price, Total)
                      VALUES (?, ?, ?, ?, ?)""",
                   (row["Date"], row["Product"], int(row["Quantity"]),
                    float(row["Price"]), float(row["Total"])))
conn.commit()
```
`int(...)` / `float(...)` strip NumPy types - see Traps (NumPy integers are stored as unreadable BLOBs).

**3.10 WHEN: a whole DataFrame goes in - one-line version and reading back**
```python
import pandas as pd
df.drop_duplicates(subset=["Date", "Product"]).to_sql(
    "Sales", conn, if_exists="append", index=False)   # table must exist
result = pd.read_sql_query(
    "SELECT Product, SUM(Total) AS Revenue FROM Sales GROUP BY Product",
    conn)                                # returns a DataFrame
print(result)
```
- `if_exists="append"` adds rows; the default `"fail"` raises `ValueError: Table 'Sales' already exists.`; `"replace"` **drops your table and recreates it WITHOUT your UNIQUE rule**.
- `to_sql` has no `OR IGNORE`: with a UNIQUE table, inserting a row twice raises `pandas.errors.DatabaseError: Execution failed ...` (cause: `IntegrityError`). To be safe on re-runs, drop rows already in the table:
```python
existing = pd.read_sql_query("SELECT Date, Product FROM Sales", conn)
merged = df.merge(existing, on=["Date", "Product"], how="left",
                  indicator=True)
new_rows = merged[merged["_merge"] == "left_only"].drop(columns="_merge")
new_rows.to_sql("Sales", conn, if_exists="append", index=False)
```
For the exam the **loop + INSERT OR IGNORE** (3.9) is simpler and re-run safe.

**3.11 WHEN: clean the CSV first (recap of Task 1a so Task 2 has good data)**
```python
df = pd.read_csv("sales_data.csv", parse_dates=["Date"], dayfirst=True)
df["Product"] = df["Product"].fillna("Unknown")          # blank name
df["Quantity"] = df["Quantity"].fillna(0)                # blank qty
df["Price"] = df["Price"].fillna(df["Total"] / df["Quantity"])  # rebuild
df["Total"] = df["Quantity"] * df["Price"]               # always recompute
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")          # TEXT for SQLite
```

<div class="pb"></div>

---

## 4. Line-by-line walkthrough

### 4.1 The 2024 Tasks 2a + 2b - complete worked solution
(Task 1a cleaning from template 3.11 comes first; this is everything after it. Tested on the real `sales_data.csv`.)

```python
import sqlite3
import pandas as pd

# ---- Task 2a: create DB + table (UNIQUE stops duplicates) ----
conn = sqlite3.connect("SalesDB.db")     # open/create cabinet SalesDB
cursor = conn.cursor()                   # hire the clerk
cursor.execute("""CREATE TABLE IF NOT EXISTS Sales (
                      Date     TEXT NOT NULL,
                      Product  TEXT NOT NULL,
                      Quantity INTEGER,
                      Price    REAL,
                      Total    REAL,
                      UNIQUE (Date, Product)
                  )""")                  # the drawer + the bouncer rule

added = 0                                # counters for a friendly report
skipped = 0
for index, row in df.iterrows():         # df = the cleaned DataFrame
    cursor.execute("""INSERT OR IGNORE INTO Sales
                      (Date, Product, Quantity, Price, Total)
                      VALUES (?, ?, ?, ?, ?)""",
                   (row["Date"], row["Product"], int(row["Quantity"]),
                    float(row["Price"]), float(row["Total"])))
    if cursor.rowcount == 1:             # 1 = card filed
        added += 1
    else:                                # 0 = bouncer said no
        skipped += 1
conn.commit()                            # save everything at once
print(f"Inserted {added} rows, ignored {skipped} duplicates.")

# ---- Task 2b: queries ----
cursor.execute("""SELECT SUM(Total) FROM Sales
                  WHERE strftime('%Y', Date) = '2023'""")
total_2023 = cursor.fetchone()[0]        # one row, first column
print(f"Total sales in 2023: {total_2023:.2f}")

cursor.execute("""SELECT Product, SUM(Quantity) AS TotalQty FROM Sales
                  WHERE strftime('%Y', Date) = '2023'
                  GROUP BY Product
                  ORDER BY TotalQty DESC""")
print("Product summary 2023:")
for product, qty in cursor.fetchall():   # list of (product, qty) tuples
    print(f"  {product:<14}{qty}")
conn.close()                             # lock the cabinet
```
Output (first run; a re-run prints `Inserted 0 rows, ignored 151 duplicates.` and the **same** answers):
```text
Inserted 145 rows, ignored 6 duplicates.
Total sales in 2023: 8950.00
Product summary 2023:
  Sweets        180
  Orange Juice  152
  Biscuits      140
  Chocolate     95
  Water         60
  Unknown       13
```
Line notes:
- `UNIQUE (Date, Product)` = "no two cards may have the same date AND product". The 6 repeated 2022 rows are rejected (151 - 6 = 145 rows stored).
- `cursor.rowcount` after an `INSERT OR IGNORE` is 1 if a row went in and 0 if it was ignored - handy proof for the marker.
- `strftime('%Y', Date) = '2023'` keeps only 2023 cards; `SUM(Total)` adds them; `fetchone()[0]` extracts the single number.
- `GROUP BY Product` makes one pile per product; `SUM(Quantity)` totals each pile; `ORDER BY TotalQty DESC` puts the biggest first.
- Answers (checked independently in pandas): 2023 total **8950.0**.

### 4.2 IMPORTANT subtlety - `INSERT OR IGNORE` does nothing without a UNIQUE rule
The official 2024 solution (`ProgSD-Python-Solution.py`) does this:
```python
cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
        Date TEXT, Product TEXT, Quantity INTEGER, Price REAL, Total REAL)''')
...
cursor.execute('''INSERT OR IGNORE INTO Sales (Date, Product, Quantity,
        Price, Total) VALUES (?, ?, ?, ?, ?)''', (...))
```
There is **no UNIQUE or PRIMARY KEY**, so nothing can ever conflict and `OR IGNORE` ignores nothing. Proof (run on the real data): the table holds 151 rows after run 1 (including the 6 duplicate rows), **302** after run 2, and the 2023 total doubles from 8900 to **17800**. Small demo you can paste and run:
```python
import sqlite3
conn = sqlite3.connect(":memory:")                  # throw-away database
cursor = conn.cursor()
cursor.execute("CREATE TABLE NoRule (Date TEXT, Product TEXT)")
cursor.execute("""CREATE TABLE WithRule (Date TEXT, Product TEXT,
                  UNIQUE (Date, Product))""")
for table in ["NoRule", "WithRule"]:
    for attempt in range(3):                        # same row, 3 times
        cursor.execute(f"INSERT OR IGNORE INTO {table} VALUES (?, ?)",
                       ("2023-01-01", "Chocolate"))
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(table, "->", cursor.fetchone()[0], "row(s)")
```
```text
NoRule -> 3 row(s)
WithRule -> 1 row(s)
```
**Four correct ways to "ensure no duplicate entries"** (give the marker one of them, and say which in a comment):

| Way | How | Catch |
|---|---|---|
| 1. UNIQUE key + `INSERT OR IGNORE` | `UNIQUE (Date, Product)` in CREATE TABLE | **Best.** Works across re-runs. |
| 2. Natural primary key | `ISBN TEXT PRIMARY KEY`, `username TEXT UNIQUE` | Only when the data has a real unique field. |
| 3. Check first | `SELECT 1 ... WHERE ...` then `fetchone() is None` -> insert | Custom messages; slower; two steps. |
| 4. `df.drop_duplicates()` before inserting | `df = df.drop_duplicates(subset=["Date", "Product"])` | Only removes duplicates *inside the DataFrame*. Re-run the program and they all go in again - combine with way 1. |

**TRAP:** an `id INTEGER PRIMARY KEY AUTOINCREMENT` column does **not** prevent duplicates - every duplicated sale just gets a new id. The key must be made of the data that defines "the same".

**Other cleaning observations** (the official file fills Price with `0.0`, then recomputes `Total = Quantity * Price`): the Chocolate row of 12/03/2023 has a blank Price but Total 50, so the official method turns it into Total 0 and the 2023 total becomes **8900** instead of the correct **8950**. Rebuilding Price as `Total / Quantity` (template 3.11) keeps it right. Also, the blank-Product rows become `Unknown`; one of them (06/04/2022) is really a repeat of a Chocolate sale, so UNIQUE does not catch it (different Product text) - harmless for the 2023 questions.

### 4.3 Console versions of the old validation tasks (no tkinter)
**2021 - Users, duplicate username, password rule** (`save_user` replaces the Save button):
```python
import sqlite3

conn = sqlite3.connect("Users.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                      id       INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)""")

def password_ok(password):
    """At least 8 characters AND at least one digit."""
    has_digit = any(ch.isdigit() for ch in password)
    return len(password) >= 8 and has_digit

def save_user(username, password):
    """Return a message telling the user what happened."""
    if not password_ok(password):
        return "Password must be 8+ characters and include a number."
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:             # found = duplicate
        return "Username already exists!"
    cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()
    return "User saved."

def display_users():                              # the "Display" button
    cursor.execute("SELECT id, username, password FROM Users")
    for row in cursor.fetchall():
        print(row)

def clear_users():                                # the "Clear" button
    cursor.execute("DELETE FROM Users")
    conn.commit()
```
Try: `save_user("mireilla", "password1")` gives `User saved.`; again gives `Username already exists!`; `"short1"` / `"longpassword"` give the password message.

**2023 - Library: ISBN duplicate, year range, empty fields, the two "librarian" questions**
```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect("LibraryDB.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
                      ISBN   TEXT PRIMARY KEY,
                      Title  TEXT NOT NULL,
                      Author TEXT NOT NULL,
                      Year   INTEGER)""")

def add_book(isbn, title, author, year_text):
    """Validate, then save. Returns the message to show the user."""
    if title.strip() == "" or author.strip() == "":
        return "Title and Author fields cannot be empty!"
    try:
        year = int(year_text)                     # text -> number
    except ValueError:
        return "Invalid year of publication!"
    if year < 1450 or year > datetime.now().year:
        return "Invalid year of publication!"
    cursor.execute("SELECT ISBN FROM Books WHERE ISBN = ?", (isbn,))
    if cursor.fetchone() is not None:
        return "This ISBN already exists!"
    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?)",
                   (isbn, title.strip(), author.strip(), year))
    conn.commit()
    return "Book added successfully!"

def librarian(question):
    """Understands exactly the two sentence shapes in the exam."""
    q = question.lower().strip().rstrip("?.! ")
    if q.startswith("recommend me a book by "):
        author = q.replace("recommend me a book by ", "", 1)
        cursor.execute("SELECT Title, Author FROM Books "
                       "WHERE LOWER(Author) = ?", (author,))
        row = cursor.fetchone()
        if row is None:
            return "Sorry, I have no books by that author."
        return f"How about '{row[0]}' by {row[1]}?"
    if q.startswith("when was ") and q.endswith(" published"):
        title = q[len("when was "):-len(" published")]
        cursor.execute("SELECT Title, Year FROM Books "
                       "WHERE LOWER(Title) = ?", (title,))
        row = cursor.fetchone()
        if row is None:
            return "Sorry, that book is not in the library."
        return f"{row[0]} was published in {row[1]}."
    return "Sorry, I only understand two kinds of question."
```
Results: `add_book("1-86092-038-1","The Signalman","Charles Dickens","1812")` -> `Book added successfully!`; same ISBN again -> `This ISBN already exists!`; year `2999` -> `Invalid year of publication!`; `librarian("when was The Signalman published?")` -> `The Signalman was published in 1812.` `LOWER(...)` makes the match case-insensitive (the screenshots type lower case).

**2022 - TravelPrice: save ages + prices, display, total, Clear All**
```python
import sqlite3

conn = sqlite3.connect("TravelPrice.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Tickets (
                      id    INTEGER PRIMARY KEY AUTOINCREMENT,
                      age   INTEGER NOT NULL,
                      price INTEGER NOT NULL)""")

def ticket_price(age):
    if age <= 2:
        return 0                       # free
    elif age <= 12:
        return 7                       # children 3-12
    elif age >= 66:
        return 13                      # seniors
    return 18                          # everyone else

for age in [2, 78, 68, 45, 2]:         # the exam's example group
    cursor.execute("INSERT INTO Tickets (age, price) VALUES (?, ?)",
                   (age, ticket_price(age)))
conn.commit()
cursor.execute("SELECT age, price FROM Tickets")
for age, price in cursor.fetchall():   # age and price on the same row
    print(age, price)
cursor.execute("SELECT SUM(price) FROM Tickets")
print("Total cost:", cursor.fetchone()[0])        # 44 (as in the paper)
cursor.execute("DELETE FROM Tickets")             # Clear All
conn.commit()
conn.close()
```
Prices come out `0 13 13 18 0`, total 44 - matches the screenshot in the 2022 paper. After `DELETE`, `SUM(price)` is `None` (print `or 0` if you want zero).

**Lab 3 Ex 18 (phone book) - safe re-runnable setup**
```python
people = [(1, "Simon", "Pierre", "0142678 9056"),
          (2, "Katarina", "Iglesias", "0203456 7078")]
cursor.executemany("INSERT OR IGNORE INTO Names VALUES (?, ?, ?, ?)", people)
conn.commit()      # works because ID is a PRIMARY KEY: re-runs skip rows
```
`executemany` runs the same statement once per tuple in the list.

<div class="pb"></div>

---

## 5. Traps & debugging

| Mistake | What you see | Fix |
|---|---|---|
| `INSERT OR IGNORE` on a table with no UNIQUE/PRIMARY KEY | No error - **duplicates silently stored**, row count doubles on each run | Add `UNIQUE (cols)` / `PRIMARY KEY` (4.2). |
| Date stored as `05/03/2023` (dd/mm/yyyy) | `strftime('%Y', Date)` returns `None`; `SUM` is `None` | Store `YYYY-MM-DD`: `df["Date"].dt.strftime("%Y-%m-%d")`. |
| Inserting a pandas `Timestamp` | `ProgrammingError: Error binding parameter 1: type 'Timestamp' is not supported` | Convert to a string first (`.dt.strftime`). |
| Inserting a NumPy number (`np.int64`) | **No error** - stored as `BLOB` bytes `b'\x07\x00...'`, so `SUM` is wrong | Wrap: `int(x)`, `float(x)`, `str(x)`. (In the version tested, `iterrows()` on a mixed-type frame gave plain Python numbers, but cast anyway.) |
| Forgot `conn.commit()` | Rows vanish after the program ends (other connections see 0 rows) | Commit after every INSERT/UPDATE/DELETE batch. |
| `(username)` instead of `(username,)` | `ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 2 supplied.` (a string is treated as a sequence of characters) | One-item tuple needs the trailing comma. |
| Wrong number of `?` vs values | `ProgrammingError: Incorrect number of bindings supplied. The current statement uses 4, and there are 3 supplied.` | Count them. |
| Misspelt table / column | `OperationalError: no such table: Sale` / `no such column: Prod` | Match the CREATE TABLE names exactly. |
| f-string SQL with a quote in the data | `OperationalError: near "Brien": syntax error` | Use `?` placeholders. |
| `fetchone()` found nothing, then `[0]` | `TypeError: 'NoneType' object is not subscriptable` | Test `if row is not None:` first. (`SUM`/`COUNT` always return a row, but `SUM` can be `None`.) |
| Using the cursor after `conn.close()` | `ProgrammingError: Cannot operate on a closed database.` | Close at the very end only. |
| Duplicate on a UNIQUE column without OR IGNORE | `IntegrityError: UNIQUE constraint failed: U.name` | `INSERT OR IGNORE`, or `try/except sqlite3.IntegrityError`, or check first. |
| Missing value in `NOT NULL` column | `IntegrityError: NOT NULL constraint failed: U.name` | Clean/fill the data first. |
| `df.to_sql(...)` on an existing table | `ValueError: Table 'Sales' already exists.` | `if_exists="append"`. (`"replace"` deletes your UNIQUE rule.) |
| `to_sql` a second time into a UNIQUE table | `DatabaseError: Execution failed ...` (an IntegrityError inside) | Filter out existing rows (3.10) or use the loop with `OR IGNORE`. |
| `UPDATE`/`DELETE` without `WHERE` | **Every** row changed/deleted | Always write the `WHERE`. (`DELETE FROM t` alone is the deliberate "clear all".) |
| Hard-coded IDs inserted on every run (Lab 3 `ex_18.py`) | Second run: `IntegrityError: UNIQUE constraint failed: Names.ID` | `INSERT OR IGNORE`, or only insert when the table is empty. |
| `with sqlite3.connect(...) as db:` and expecting it to close | Connection stays open (the `with` only commits) | Still call `db.close()` at the end. |
| Comparing year to a number: `strftime(...) = 2023` | No rows (text vs number) | Quote it: `= '2023'`. |

---

## 6. Anticipated exam questions

**Q1 [2 marks]** *Create an SQLite database named SalesDB and a connection/cursor.*
```python
conn = sqlite3.connect("SalesDB.db")
cursor = conn.cursor()
```

**Q2 [3 marks]** *Create a table Sales with columns Date, Product, Quantity, Price, Total.* Template 3.1 (TEXT, TEXT, INTEGER, REAL, REAL; add `UNIQUE (Date, Product)`).

**Q3 [4 marks]** *Insert the cleaned DataFrame into Sales; ensure no duplicate entries are added.* Template 3.9 with the table from 3.1 and a one-line comment: `# UNIQUE(Date, Product) + OR IGNORE prevent duplicates`.

**Q4 [3 marks]** *Display the total sales for 2023.*
```python
cursor.execute("""SELECT SUM(Total) FROM Sales
                  WHERE strftime('%Y', Date) = '2023'""")
print("Total sales 2023:", cursor.fetchone()[0])
```

**Q5 [3 marks]** *List each product and its total quantity sold in 2023, highest first.* Template 3.7.

**Q6 [3 marks]** *Why does `INSERT OR IGNORE` not stop duplicates in this table?* (a table without UNIQUE/PRIMARY KEY) Because "ignore" only applies when a constraint is violated; with no constraint, every insert succeeds. Fix: add `UNIQUE (Date, Product)`.

**Q7 [3 marks]** *Before saving a new user, check whether the username already exists and print a message if it does.* Template 3.4 + `if username_exists(...): print("Username already exists!")`.

**Q8 [2 marks]** *Delete everything from the database (Clear All).* `cursor.execute("DELETE FROM Tickets")` then `conn.commit()`.

**Q9 [3 marks]** *Read all rows of Sales into a DataFrame and print the average Price per product.*
```python
df2 = pd.read_sql_query("SELECT * FROM Sales", conn)
print(df2.groupby("Product")["Price"].mean())
```
(or in SQL: `SELECT Product, AVG(Price) FROM Sales GROUP BY Product`).

**Q10 [3 marks]** *Why must dates be stored as `YYYY-MM-DD` text?* SQLite has no date type; its `strftime`/`date` functions only understand ISO text, and it sorts correctly alphabetically. `dd/mm/yyyy` gives `None` from `strftime`.

---

## 7. Quick-reference box (copy onto your notes sheet)

```text
import sqlite3            conn = sqlite3.connect("X.db"); cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS T (id INTEGER PRIMARY KEY
   AUTOINCREMENT, name TEXT NOT NULL, d TEXT, q INTEGER, p REAL,
   UNIQUE (d, name))""")      types: INTEGER REAL TEXT BLOB
INSERT: cur.execute("INSERT INTO T (a,b) VALUES (?,?)", (x, y)); conn.commit()
NO DUPES: needs UNIQUE/PRIMARY KEY in table + INSERT OR IGNORE (rowcount 0/1)
          (OR IGNORE alone, no constraint = NOTHING prevented!) or check first
          SELECT 1 FROM T WHERE k=? -> cur.fetchone() is not None
SELECT: SELECT cols FROM T WHERE c=? GROUP BY g ORDER BY x DESC
        fetchone() -> tuple/None | fetchall() -> list of tuples
AGG: COUNT(*) SUM(c) AVG(c) MIN(c) MAX(c)  (SUM of no rows = None)
YEAR: WHERE strftime('%Y', Date) = '2023'   (Date must be YYYY-MM-DD text)
UPDATE T SET c=? WHERE k=?    DELETE FROM T WHERE k=?    DELETE FROM T = clear
ALWAYS conn.commit() after changes; conn.close() at the end
Single param needs comma: (x,)   cast numpy: int(x) float(x)   no f-string SQL
DF -> table: loop df.iterrows() + INSERT OR IGNORE ... int()/float()
             or df.to_sql("T", conn, if_exists="append", index=False)
Table -> DF: pd.read_sql_query("SELECT * FROM T", conn)
Dates: df["Date"].dt.strftime("%Y-%m-%d") BEFORE inserting
```
