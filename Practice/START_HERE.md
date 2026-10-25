# START HERE - Python exam preparation pack

Everything is in `Practice/Exam_Prep_Pack/`. Printable PDFs are in `Exam_Prep_Pack/PDF_Print/` (one per document, A4, black & white friendly). Runnable, tested solutions are in `Practice/Solutions_py/`.

## Situation in one paragraph
Your Python assessment next week is a **mock of the final lab exam**: one `.py` file, uploaded. **tkinter is no longer examined.** The newest paper (2024) is pandas -> matplotlib -> SQLite -> PyTorch, and the practice sheet "Task 3" shows PyTorch possibly being **replaced by CSV + pandas + numpy + matplotlib**. SQLite and "do the right thing when data is wrong" have appeared in every paper since 2021. So prepare for **both** variants of task 3.

## The reading order

| # | Document | Why |
|---|---|---|
| 1 | `00_Exam_Pattern_Analysis` | how the papers are built and marked; the 10 commandments; study plan |
| 2 | `Paper_Solutions/P1_2024_Paper_Explained` | the closest thing to your mock, every line explained with analogies |
| 3 | `Topics/T4_SQLite` | highest-yield topic |
| 4 | `Topics/T5_Pandas_NumPy`, `T6_Matplotlib` | Task 1 of any data paper |
| 5 | `Topics/T3_Files_CSV_Exceptions` | the Practice Task 3 solution + file handling |
| 6 | `Topics/T7_PyTorch_Basics` | the network task |
| 7 | `Mock_Exams/MockA`, then `MockB` | sit them timed, then self-mark |
| 8 | `Paper_Solutions/P2-P4` (2021-2023) | extra database/validation practice, console versions |
| 9 | `Topics/T1_Python_Core`, `T2_OOP_Python` | fill gaps; `T8_Tkinter_Legacy` only if you have spare time |
| 10 | `Exam_Day_Cheat_Sheet` | **print this; take it into the exam** |

## What to print (suggested, about 35 pages)
`Exam_Day_Cheat_Sheet` (3-4 pp), `P1` (~9 pp), `T4`, `T5`, `T6` (the rest as you wish). **Also hand-write the "Quick-reference box" from each topic onto your own notes sheet** - it is allowed and it is the best revision there is.

## Folder map
```text
Practice/
  START_HERE.md                    <- this file
  Solutions_py/                    <- all tested .py solutions
  Exam_Prep_Pack/
    00_Exam_Pattern_Analysis.md
    Exam_Day_Cheat_Sheet.md
    Paper_Solutions/  P0 index, P1 2024, P2 2021, P3 2022, P4 2023
    Topics/           T1 core, T2 OOP, T3 files/CSV, T4 SQLite, T5 pandas/numpy,
                      T6 matplotlib, T7 PyTorch, T8 tkinter (legacy)
    Mock_Exams/       README, MockA (2024-style), MockB (Practice-Task-3-style)
    PDF_Print/        printable PDFs of every .md above
    _tools/build_pdfs.py   rebuilds the PDFs (needs: pip install markdown pygments)
  (your original uploaded exam papers are untouched)
```

## Exam environment checklist
- Know whether the exam machine has `pandas`, `matplotlib`, `torch` (open a terminal and `python -c "import pandas, matplotlib, torch"` in the first minute; if torch is missing, tell the invigilator).
- File name `your_name_python_task.py`; data files in the same folder as the script.
- Run the whole file from a clean start before uploading.

*When you upload your own coursework code, tell me which parts and I will fold your own idioms into the topic documents.*
