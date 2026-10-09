# tAPP 5: Data Visualisation — Concept Notes

The concept behind each question. Short answers are in [tAPP5_answers.md](tAPP5_answers.md).

## Task 1: choosing a chart (A→3, B→1, C→2, D→4)

The chart follows from the type of data and the question being asked:

- **Change over time:** use a line chart. The line joining the points implies an order and a trend.
- **Comparing separate categories:** use a bar chart. Each category gets a bar and you compare heights.
- **Distribution of one numerical variable:** use a histogram. It shows where values cluster and how spread out they are.
- **Relationship between two numerical variables:** use a scatter plot. Each observation is a point, and the pattern of points shows the correlation.

## Task 2: bar chart vs histogram (B)

The two look alike but answer different questions.

- **Bar chart:** the x-axis holds categories with no numerical scale (programmes, countries). Bars have gaps and can be reordered.
- **Histogram:** the x-axis is a continuous number line cut into bins. Bars touch, and the order is fixed.

Marks in ranges are binned numerical data, so this is a histogram. In matplotlib you pass the raw marks and the bin edges:

```python
ax.hist(marks, bins=[0, 40, 50, 60, 70, 100])
```

## Task 3: undefined names (B)

Python only knows names you have assigned. The lists are called `study_hours` and `marks`, so `ax.scatter(x, y)` fails with `NameError: name 'x' is not defined`. The fix is:

```python
ax.scatter(study_hours, marks)
```

The other options are false: scatter needs numerical data, axis labels work on any Axes, and `plt.show()` comes last.

## Task 4: limits of pie charts (C)

A pie chart shows parts of a whole, and people judge angles and areas poorly. It works for about 2–5 slices with clear differences. With 12 programmes the slices are thin and similar. Bars on a common baseline turn the comparison into comparing lengths, which people do accurately.

## Task 5: error bars need a definition (D)

`yerr=errors` draws a line of that length above and below each bar, and `capsize=5` adds the small end caps. Matplotlib plots whatever numbers you give it. They could be:

- **Standard deviation:** the spread of the data.
- **Standard error:** the uncertainty of the mean (SD / √n), which is much smaller.
- **95% confidence interval:** roughly ±1.96 × SE.

These give very different bar lengths for the same data, so a chart that doesn't say which one is used can't be interpreted.

## Task 6: grouped vs stacked bars (A)

- **Grouped:** bars sit side by side and all start at zero, so individual values are easy to compare.
- **Stacked:** segments sit on top of each other. This shows the total and the composition, but only the bottom segment starts at zero, so the others are hard to compare.

The question asks for accurate comparison of individual products, so grouped is the choice. If it asked about total sales per region, stacked would be.

## Task 7: `plt.subplots(nrows, ncols)` (B)

The first number is rows and the second is columns.

- **`subplots(2, 1)`:** 2 rows and 1 column, so the plots are stacked vertically.
- **`subplots(1, 2)`:** 1 row and 2 columns, so the plots are side by side.

A Figure is the whole canvas and an Axes is one plot on it. In both cases `axs` is a 1-D array of two Axes, indexed `axs[0]` and `axs[1]`. Only a grid like `subplots(2, 2)` gives a 2-D array, indexed `axs[row, col]`.

## Task 8: legend location codes (B)

`loc` accepts a string or a number.

| Code | Position |
|---|---|
| 0 | best (automatic) |
| 1 | upper right |
| 2 | upper left |
| 3 | lower left |
| 4 | lower right |

Codes 1–4 run anticlockwise from the top right, like the quadrants of a graph. `loc="upper left"` is the readable equivalent of `loc=2`.

## Task 9: date formatting (B)

An axis has a locator, which decides where ticks go, and a formatter, which decides what text each tick shows. `set_major_formatter(mdates.DateFormatter("%b %Y"))` only changes the text: `%b` is the short month name and `%Y` is the four-digit year, giving "Jan 2024". It does not convert, sort or rotate anything.

Rotation is the job of `fig.autofmt_xdate()`, which tilts the date labels (30° by default) and right-aligns them so they don't overlap.

## Task 10: inset Axes (B)

`ax.inset_axes([x0, y0, width, height])` creates a small Axes inside `ax`. The numbers are fractions of the parent Axes, not data values. So `[0.62, 0.58, 0.3, 0.3]` puts the inset's lower-left corner 62% across and 58% up, with 30% of the width and height, which lands in the upper-right area. It is not a new Figure.

The usual use is zooming in on a crowded region while keeping the full view visible.

## Task 11: `ax.pie` parameters (A)

- **`values`:** the slice sizes, as shares of the total. Here they sum to 100, so the percentages equal the values.
- **`explode`:** one number per slice, giving how far to push it out from the centre as a fraction of the radius. Only B has 0.15, so only B moves.
- **`autopct="%1.1f%%"`:** prints the percentage on each slice. `%1.1f` means one decimal place and `%%` is a literal percent sign.
- **`startangle=90`:** the first slice starts at the top (12 o'clock) instead of the right, and slices go anticlockwise.

Setting `explode` to all zeros gives a normal pie with every slice touching the centre; nothing else changes.
