# START HERE - Python assessment preparation pack (version 2)

Everything is in `Practice/Exam_Prep_Pack/`. Printable PDFs are in `Exam_Prep_Pack/PDF_Print/`. Runnable, tested solutions are in `Practice/Solutions_py/`. **What changed since version 1: see `Exam_Prep_Pack/CHANGELOG.md`.**

## Situation in one paragraph
Your instructor says the practical assessment (15% of the course) covers the same areas as the final-exam Python question, and gave an explicit checklist: **pandas** (load, shape, duplicates, merge, filter, save to CSV), **matplotlib** (scatter, line, bar, box plots with titles and labels), **SQLite** (create/connect, store a DataFrame, SELECT/WHERE/ORDER BY/UPDATE, `?` parameters, commit, export results to CSV) and **PyTorch** (seed first, `nn.Module` with Linear + ReLU, synthetic data `y = X @ w + b + noise`, shapes of X and y, loss + optimiser, training loop, record and plot the loss). tkinter is gone. The instructor's advice: **practise the individual operations and understand each line; do not memorise one complete solution.** This pack is now organised around exactly that.

## Test logistics (from the instructor's latest message) - read `Exam_Prep_Pack/Test_Day_Card_60_Minutes`
The mid-term programming test is **ONE HOUR** (start attempt -> upload the `.py`), three tasks "very similar to the 2024/25 paper" (Task 3 = PyTorch), ONE file named `student_name_python_task.py`, late upload = two minor bands, Moodle + paper notes only, **no Copilot/AI tools**, notebooks must be exported as an executable script. Set up PyTorch **before** clicking "Start attempt". **Print the Test Day Card (2 pages) and keep it on the desk.**

## How to start (in this order)

| Step | Do this | File |
|---|---|---|
| 1 | Read the checklist map and the study plan (10 min) | `00_Exam_Pattern_Analysis` sections 0 and 8 |
| 2 | **Daily 20-minute routine:** pick 5 operation cards, cover the code, write each from memory, run it, tick the tracker | `Topics/T9_Checklist_Operation_Cards` and `Solutions_py/practical_operation_drills.py` (runs all 27 cards: `python practical_operation_drills.py`) |
| 3 | Learn the weak areas properly, in the order: pandas merge/duplicates -> box plot -> SQLite UPDATE and export -> PyTorch regression | `T5` (3.11-3.15), `T6` (3.11-3.13), `T4` (section 8), `T7` (3.8) |
| 4 | Sit **Mock C** (written to the checklist) timed, then self-mark | `Mock_Exams/MockC` |
| 5 | More whole-program practice: Mock A, Mock B | `Mock_Exams/` |
| 6 | Read P1 (2024 paper) *for understanding only* | `Paper_Solutions/P1` |
| 7 | Fill gaps in Python basics, files/CSV, OOP | `T1`, `T3`, `T2` |
| last | Hand-write the quick-reference boxes; print the cheat sheet | `Exam_Day_Cheat_Sheet` (version 2) |

## What to print
**Core (take into the exam):** `Test_Day_Card_60_Minutes` (2 pp) + `Exam_Day_Cheat_Sheet` v2 (4 pp) + `T9_Checklist_Operation_Cards` (17 pp). If you already printed v1 of T4, T5, T6, T7: print the three ready-made files in `Exam_Prep_Pack/Print_New_Pages/` (only the new pages, 42 pp including the cheat sheet; page 1 replaces your old page 1, the rest goes behind your old copy). T2 and T3 did not change.
**For study, not for the exam:** `00_Exam_Pattern_Analysis`, the three Mock papers (then the marking schemes afterwards).
**Skip:** `T8_Tkinter_Legacy`, `P2-P4` (old GUI papers), `T1`/`T2` unless weak.
**Also hand-write** one page of your own notes (allowed): copy the quick-reference box of each topic in your own words.

## Folder map
```text
Practice/
  START_HERE.md                    <- this file
  Solutions_py/                    <- all tested .py solutions + 27-card drills file
  Exam_Prep_Pack/
    CHANGELOG.md                   <- what changed in version 2, which pages to reprint
    Print_New_Pages/               <- 3 small PDFs: ONLY the new pages to print (stamped)
    00_Exam_Pattern_Analysis.md    <- checklist map, exam patterns, study plan
    Exam_Day_Cheat_Sheet.md        <- v2, one tested script covering every checklist item
    Paper_Solutions/  P0 index, P1 2024, P2 2021, P3 2022, P4 2023
    Topics/           T1 core, T2 OOP, T3 files/CSV, T4 SQLite, T5 pandas/numpy,
                      T6 matplotlib, T7 PyTorch, T8 tkinter (legacy),
                      T9 operation cards (the checklist, one card per operation)
    Mock_Exams/       README, MockA (2024 style), MockB (Practice Task 3 style),
                      MockC (the instructor's checklist)
    PDF_Print/        printable PDF of every .md above
    _tools/build_pdfs.py   rebuilds the PDFs (needs: pip install markdown pygments)
  (your original uploaded exam papers are untouched)
```

## Exam environment checklist
- First minute: `python -c "import pandas, matplotlib, torch"`. If something is missing, tell the invigilator.
- **Matplotlib version trap:** name box-plot boxes with `plt.xticks(...)` (works everywhere); `labels=` and `tick_labels=` depend on the version.
- Put the seed on the first line of the PyTorch part (before the data and before the model).
- Run the whole file from a clean start before uploading; check the file name the paper asks for.

*When you upload your own coursework code, tell me which parts and I will fold your own idioms into the documents.*
