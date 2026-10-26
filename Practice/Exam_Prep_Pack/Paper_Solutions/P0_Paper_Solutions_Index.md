# Paper Solutions - index

| Doc | Paper | Style | Status in your exam |
|---|---|---|---|
| **P1** | 2024 final (Sales, SQLite, PyTorch) | pandas + charts + DB + NN, 40 marks | **MAIN TEMPLATE for the mock** |
| (T3) | Practice Exam Task 3 (Height logger) | CSV append, numpy, histogram | likely PyTorch replacement; solved in `Topics/T3_Files_CSV_Exceptions` and `Solutions_py/practice_task3_height_logger.py` |
| P2 | 2021 Registration | DB + validation | GUI removed; logic reusable (console version provided) |
| P3 | 2022 Bus fare | DB + fare rule | GUI removed; logic reusable |
| P4 | 2023 Library + "ChatGPT" | DB + validation + text parsing | GUI removed; logic reusable |

**All runnable solutions live in `Practice/Solutions_py/`:**

| File | What |
|---|---|
| `2024_sales_sqlite_pytorch_solution.py` | the full 2024 paper (tested; re-runnable) |
| `2024_twist_drills.py` | 11 "what if the question changes" variations |
| `practice_task3_height_logger.py` | Practice Task 3 |
| `2021_registration_users_solution.py` + `_console.py` | 2021 (window / terminal) |
| `2022_bus_fare_travelprice_solution.py` + `_console.py` | 2022 |
| `2023_library_librarian_solution.py` + `_console.py` | 2023 |

**How to study a paper solution (do not just read it):**
1. Read the paper's wording and cover the solution. Write your own plan as comments.
2. Write the code from your plan. Run it.
3. Compare with the solution; for each difference ask "is mine wrong, or just different?"
4. Read the line-by-line explanation for every line you could not write alone.
5. Next day, write ONE operation from it (e.g. just the SQLite part) from a blank line. Your instructor's advice: practise the *individual operations*; do not try to memorise a whole solution.

**Findings that go beyond the official solution** (all tested; explained in P1):
- the official 2024 solution under-reports 2023 sales by £50 (blank Price filled with 0), plots all years instead of 2023, and does not prevent duplicates (re-running doubles the DB);
- `sales_data.csv` contains 6 exact duplicate rows.
