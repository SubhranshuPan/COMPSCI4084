# tAPP 5: Data Visualisation — Answers

## Task 1 — Choose the most appropriate chart

| Scenario | Chart | Why |
|---|---|---|
| A. Monthly attendance over 12 months | 3. Line chart | The months are in time order, so a line shows the trend in attendance across the year. |
| B. Students enrolled in five degree programmes | 1. Bar chart | The programmes are separate categories, and bar heights make the five counts easy to compare. |
| C. Distribution of marks for 200 students | 2. Histogram | Marks are numerical values, so grouping them into bins shows the shape of the distribution. |
| D. Hours studied vs assessment mark | 4. Scatter plot | Each student is one point with two numerical values, which reveals any relationship between hours and marks. |

## Task 2 — Bar chart or histogram?

**Answer: B. Histogram.** The marks are numerical values grouped into ranges (bins), and a histogram shows how many students fall in each range. A bar chart is for comparing separate categories.

## Task 3 — Identify the problem in the code

**Answer: B. `x` and `y` have not been defined.** The data is stored in `study_hours` and `marks`, but `scatter()` is called with `x` and `y`, so Python raises a `NameError`.

**Follow-up:** the corrected line is

```python
ax.scatter(study_hours, marks)
```

## Task 4 — Pie chart judgement

**Answer: C.** With 12 slices the angles are hard to judge and many look alike. Bars share a common baseline, so the 12 counts can be compared accurately.

## Task 5 — What do these error bars mean?

**Answer: D.** `yerr` only draws the numbers stored in `errors`. Matplotlib does not know or state whether they are standard deviation, standard error or a confidence interval, so the chart must say which one it is.

## Task 6 — Grouped or stacked bars?

**Answer: A. Grouped bar chart.** The three products sit side by side on the same baseline in each region, so their heights can be compared directly. In a stacked bar only the bottom segment starts at zero, so the other segments are hard to compare.

## Task 7 — Multiple Axes

**Answer: B. Two plots stacked vertically.** `subplots(2, 1)` means 2 rows and 1 column, so there are two Axes, one above the other.

**Follow-up:** `plt.subplots(1, 2)` gives 1 row and 2 columns, so the two plots sit side by side. `axs` is still an array of two Axes: `axs[0]` is the left plot and `axs[1]` is the right plot.

## Task 8 — Legend location

**Answer: B. `ax.legend(loc=2)`.** Location code 2 means upper left (1 = upper right, 3 = lower left, 4 = lower right). It is the same as `loc="upper left"`.

## Task 9

**Answer: B. It changes the way date labels are displayed.** `DateFormatter("%b %Y")` sets how the major tick labels on the x-axis are written: short month name and four-digit year, for example "Jan 2024". The data itself is not changed.

**Follow-up:** `fig.autofmt_xdate()` rotates and right-aligns the date labels on the x-axis so that long date labels do not overlap.

## Task 10

**Answer: B. To place a smaller Axes inside the main Axes.** The list is `[x, y, width, height]` as fractions of the main Axes: the lower-left corner of the inset is 62% across and 58% up, and it is 30% wide and 30% high.

**Follow-up:** an inset can show a zoomed-in view of a small region of the data next to the full picture, without needing a separate figure.

## Task 11 — Predict the output: pie chart with explode

**Answer: A.** All four values are drawn, so there are four slices. `explode = (0, 0.15, 0, 0)` moves only the second slice (B) outwards, and `autopct="%1.1f%%"` prints each percentage to one decimal place (25.0%, 35.0%, 20.0%, 20.0%).

**Follow-up:** with `explode = (0, 0, 0, 0)` slice B is no longer pulled out, so all four slices meet at the centre as an ordinary pie chart. The slice sizes, labels and percentages stay the same.
