# CHANGELOG - version 2 (after the instructor's checklist)

*Version 1 PDFs were printed before the instructor's checklist arrived. This list says exactly what changed so you can reprint only what you need. Page numbers refer to the NEW PDFs in `PDF_Print/`.*

## Why it changed
The instructor's checklist for the practical assessment names: pandas **merge**, **duplicates**, **shape**, **save to CSV**; matplotlib **box plots**; SQLite **`to_sql`**, **UPDATE**, **export results to CSV**; PyTorch **seed**, **`y = X @ w + b + noise`**, **shapes**, regression with Linear + ReLU. Version 1 covered some of these thinly and some not at all, and advised retyping a whole solution, which contradicts the instructor's "practise the individual operations".

## Documents you must REPLACE (reprint fully)
| Document | Pages (old -> new) | What changed |
|---|---|---|
| `Exam_Day_Cheat_Sheet` | 3 -> 4 | Rewritten (v2). Added: shape, `duplicated()` and `drop_duplicates(subset=)`, **merge** (inner/left/right/outer, `left_on/right_on`, `indicator`), filter/select/sort, `to_csv`; **scatter** and **box plot**; **`to_sql`**, **UPDATE** with `rowcount`, `?` parameters, **export query results to CSV** (2 ways); **seeded regression network** (`y = X @ w + b + noise`, no sigmoid) replacing the old classification block; new error rows (merge dtype, `(N,N)` shape bug, bindings, UPDATE without commit). Whole script tested twice. A bug found during testing was fixed (`cursor.description` is `None` after an UPDATE). |

## New documents (print if you want them)
| Document | Pages | What it is |
|---|---|---|
| `Topics/T9_Checklist_Operation_Cards` | 17 | 27 small "operation cards", one per checklist bullet: analogy, minimal code, what each part does, check, common slip, self-test. Plus a tracker and answer key. |
| `Mock_Exams/MockC/*` | 4 + 7 | A mock written to the checklist (two CSVs to merge, duplicates, 4 plots, SQLite with UPDATE and export, seeded regression). |
| `Solutions_py/practical_operation_drills.py` | - | all 27 cards as runnable functions with PASS/FAIL |
| `Solutions_py/pytorch_regression_practical.py` | - | the full regression program, heavily commented |

## READY-MADE PRINT FILES for the new pages
The folder `Print_New_Pages/` holds exactly the pages listed below as three small PDFs (42 pages in total), each page stamped top-right with its document and page:
- `Print_1_SQLite_T4_new_pages.pdf` (10 pages)
- `Print_2_Pandas_and_Matplotlib_T5_T6_new_pages.pdf` (18 pages)
- `Print_3_CheatSheet_v2_and_PyTorch_T7_new_pages.pdf` (14 pages, includes the new cheat sheet)
Page 1 of each document replaces your old page 1; the other new pages go BEHIND your old copy, in order. `T2` and `T3` did not change, so there is nothing new to print for them. Rebuild with `_tools/make_print_extracts.py`.

## Documents you can KEEP and just add pages to
These only had material ADDED (plus two small corrections marked below). Reprint the pages shown and slot them in.

| Document | New length | Reprint these pages | What is new |
|---|---|---|---|
| `T4_SQLite` | 11 -> 18 | **1**, **10-18** | p1: instructor checklist box. p10: 12 new trap rows (UPDATE without WHERE, rowcount, NumPy values in WHERE, `LIKE`, export index column). p11: Q11-Q16. p12: extra quick-reference box and **new section 8**: 8.1 connect, 8.2 `to_sql`, 8.3 SELECT/WHERE/ORDER BY/LIMIT, 8.4 **UPDATE** (full worked), 8.5 `?` parameters, 8.6 commit, 8.7 **export to CSV (3 ways)**, 8.8 ten statements to know. |
| `T5_Pandas_NumPy` | 10 -> 15 | **1**, **5-8**, **11-15** | p1: checklist box + **CORRECTION** (below). p5-8: new 3.11 shape, 3.12 duplicates, **3.13 merge**, 3.14 select/filter, 3.15 save to CSV. p11-15: traps 5.1, questions Q10-Q15, extra quick-reference lines. |
| `T6_Matplotlib` | 11 -> 14 | **1**, **6-8**, **11-14** | p1: checklist box + **CORRECTION** (below). p6: 3.11 scatter/line/bar templates. p7: **3.12 box plots**. p8: 3.13 which plot for which question. p11-14: traps 5.1, questions Q11-Q17, extra quick-reference lines. |
| `T7_PyTorch_Basics` | 11 -> 17 | **1**, **6-11**, **15-17** | p1: instructor checklist (1b). p6-11: **3.8 REGRESSION step by step** (seed + reproducibility proof, data and shapes, model, loss/optimiser/learning-rate table, loop, plot, evaluation + the single-Linear check that recovers `w` and `b`). p15-17: traps 5.11-5.16, questions Q11-Q17, extra quick-reference box. |
| `00_Exam_Pattern_Analysis` | 4 -> 5 | **1** (section 0), **3** (section 4), **5** (section 8) | new section 0 (checklist map); likelihood table re-weighted to the checklist; study plan changed to operations-first. |
| `Paper_Solutions/P1_2024_Paper_Explained` | 12 -> 12 | **1** | one note at the top: the 2024 paper uses a sigmoid network; your assessment is regression; read P1 for understanding, do not memorise. |
| `Mock_Exams/README_How_to_use_mocks` | 2 -> 3 | **2-3** | Mock C section appended. |

## Corrections of earlier text (old pages contain these errors)
1. **T5 page 1 / T6 page 1:** the 2024 `sales_data.csv` has **6 exact duplicate rows** (04/04/2022 to 10/04/2022 appear twice). Earlier T5/T6 text did not say so, and the "expected numbers" in T6 template K (Biscuits 203, Orange Juice 248, Sweets 261, ...) were computed WITH the duplicates left in. After `drop_duplicates()` the quantities are Biscuits 196, Chocolate 120, Orange Juice 232, Sweets 252, Unknown 33, Water 90 (the 2023 chart is unchanged).
2. **T4, `(username)` trap row:** the message "uses 1, and there are 2 supplied" now says N, because the number depends on the length of the string.
3. **Cheat sheet v1:** its PyTorch block (sigmoid output, random targets) is replaced by the regression recipe, and its `w` shape error row now says the shape silently becomes `(N, N)`.

## Documents with NO change
`T1`, `T2`, `T3`, `T8`, `P2`, `P3`, `P4`, Mock A and B papers and marking schemes.

## One version warning that applies to everything
Naming box-plot boxes: `labels=` was **removed in matplotlib 3.11**; `tick_labels=` only exists in **3.9+**. The version-proof way, used in the cheat sheet, T9 and Mock C, is `plt.boxplot(groups)` then `plt.xticks(range(1, n + 1), names)`. (T6 shows all three and explains the differences.)
