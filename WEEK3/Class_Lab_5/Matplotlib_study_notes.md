# Data Visualisation with Matplotlib — Study Notes

Section-by-section walkthrough of the lecture deck, with the code from the slides. Slide numbers are in each heading.

| # | Section | Slides |
|---|---|---|
| 1 | Matplotlib basics: Figure and Axes | 2–4 |
| 2 | Choosing the right chart | 5 |
| 3 | First plots, multiple series, keyword arguments | 6–9 |
| 4 | Multiple Axes (subplots) | 10–11 |
| 5 | Text, annotations, grid and legend | 12–15 |
| 6 | Saving figures and handling dates | 16–18 |
| 7 | Line charts | 19–20 |
| 8 | Histograms | 21–22 |
| 9 | Bar charts | 23–31 |
| 10 | Pie charts | 32–33 |
| 11 | Scatter plots | 34 |
| 12 | Box plots | 35–36 |
| 13 | Inset Axes | 37 |
| 14 | Quiz traps | — |

---

## 1. Matplotlib basics: Figure and Axes (slides 2–4)

Matplotlib is the standard Python plotting library. You nearly always use its `pyplot` module, imported as `plt`.

Everything is built on two objects:

- **Figure (`fig`):** the whole canvas or page.
- **Axes (`ax`):** one plotting area on that canvas. A Figure can hold one or several Axes.

Almost every command you write is a method on the Axes: one call to draw the data, then calls to label it.

```python
import matplotlib.pyplot as plt

months = [1, 2, 3, 4, 5, 6]
sales = [210, 180, 225, 220, 205, 200]

fig, ax = plt.subplots()        # create one Figure containing one Axes

ax.plot(months, sales)          # draw the data as a line

ax.set_title("Monthly Sales")   # what the chart shows
ax.set_xlabel("Month")          # what the x-axis means
ax.set_ylabel("Units Sold")     # what the y-axis means

plt.show()                      # display the finished figure
```

The plotting methods to know:

| Method | Chart |
|---|---|
| `ax.plot(x, y)` | line chart |
| `ax.scatter(x, y)` | scatter plot |
| `ax.bar(x, height)` | vertical bar chart |
| `ax.barh(y, width)` | horizontal bar chart |
| `ax.hist(data)` | histogram |
| `ax.boxplot(data)` | box plot |

Note that "Axes" is not the plural of "axis" here. An Axes is the whole plot; it contains an x-axis and a y-axis.

---

## 2. Choosing the right chart (slide 5)

Pick the chart from the question you want the reader to answer.

| Question | Chart | Method |
|---|---|---|
| How does a value change over an ordered sequence, such as time? | Line chart | `ax.plot()` |
| How do separate categories compare? | Bar chart | `ax.bar()` |
| How are numerical values distributed? | Histogram | `ax.hist()` |
| Is there a relationship between two numerical variables? | Scatter plot | `ax.scatter()` |

The slide's four examples:

```python
# How does profit change from month to month?  -> line
months = [1, 2, 3, 4, 5, 6]
profit = [210, 183, 225, 223, 210, 201]
ax.plot(months, profit)

# Which product sold the most?  -> bar
products = ["Toothpaste", "Shampoo", "Soap"]
sales = [5200, 1200, 9200]
ax.bar(products, sales)

# How are the marks distributed?  -> histogram
marks = [42, 55, 61, 68, 72, 74, 79, 83, 85, 91]
ax.hist(marks, bins=5)

# Do students who study more hours get higher marks?  -> scatter
study_hours = [2, 3, 4, 5, 6, 7]
marks = [48, 55, 61, 69, 75, 82]
ax.scatter(study_hours, marks)
```

The clue is in the data: time or order means line, category names mean bar, one list of numbers means histogram, and two lists of numbers paired per observation mean scatter.

---

## 3. First plots, multiple series, keyword arguments (slides 6–9)

### Line vs scatter with the same data (slide 6)

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

fig, ax = plt.subplots()
ax.plot(x, y)        # joins (1,1), (2,4), (3,9), (4,16) with a line
plt.show()
```

```python
fig, ax = plt.subplots()

ax.scatter(x, y)     # the same four points, drawn separately with no line

ax.set_title("Square Numbers")
ax.set_xlabel("Number")
ax.set_ylabel("Square")

plt.show()
```

`plot` pairs each x with the y at the same position and connects the points in order. `scatter` draws the same pairs as separate markers.

### Several series on one Axes (slide 7)

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 2.5, 0.1)               # 0, 0.1, 0.2, ... 2.4 (stop value excluded)

y1 = np.sin(np.pi * t)
y2 = np.sin(np.pi * t + np.pi / 2)       # same wave shifted left
y3 = np.sin(np.pi * t - np.pi / 2)       # same wave shifted right

fig, ax = plt.subplots()

ax.plot(t, y1, label="Series 1")         # each plot() call adds one more line
ax.plot(t, y2, label="Series 2")
ax.plot(t, y3, label="Series 3")

ax.set_title("Three Sinusoidal Trends")
ax.set_xlabel("t")
ax.set_ylabel("Value")
ax.legend()                              # shows the label= names

plt.show()
```

- Calling `ax.plot()` again on the same `ax` adds a line; it does not replace the old one.
- `label=` names a series. The name only appears once you call `ax.legend()`.
- Matplotlib gives each line a different colour automatically.

### Keyword arguments (slides 8–9)

Keyword arguments (kwargs) are optional `name=value` settings that change how a plot looks without changing the data.

```python
fig, ax = plt.subplots()

ax.plot(
    [1, 2, 4, 2, 1, 0, 1, 2, 1, 4],   # only one list: it is used as y, and x becomes 0, 1, 2, ...
    color="red",
    linewidth=3,
    linestyle="--",
    marker="o",
    label="Series 1"
)

ax.legend()
plt.show()
```

| Keyword | Purpose | Example |
|---|---|---|
| `linewidth` | line thickness | `linewidth=3` |
| `linestyle` | line style | `linestyle="--"` |
| `color` | line or marker colour | `color="red"` |
| `marker` | marker at each data point | `marker="o"` |
| `markersize` | marker size | `markersize=8` |
| `label` | name for the legend | `label="Profit"` |

Common style codes: `"-"` solid, `"--"` dashed, `"-."` dash-dot, `":"` dotted. Common markers: `"o"` circle, `"s"` square, `"^"` triangle.

---

## 4. Multiple Axes (slides 10–11)

`plt.subplots(rows, columns)` puts several Axes in one Figure, arranged in a grid.

```python
fig, axs = plt.subplots(2, 1)   # 2 rows, 1 column: two plots stacked vertically
fig, axs = plt.subplots(1, 2)   # 1 row, 2 columns: two plots side by side
```

With more than one Axes, `axs` is an array, and you pick each plot by index.

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 5, 0.1)
y1 = np.sin(2 * np.pi * t)
y2 = np.cos(2 * np.pi * t)

fig, axs = plt.subplots(2, 1, figsize=(8, 6))   # figsize = (width, height) in inches

axs[0].plot(t, y1, linestyle="-.", color="blue")   # top plot
axs[0].set_title("Sine")

axs[1].plot(t, y2, linestyle="--", color="red")    # bottom plot
axs[1].set_title("Cosine")

plt.tight_layout()   # adjusts spacing so titles and labels don't overlap
plt.show()
```

The side-by-side version changes only the layout line:

```python
fig, axs = plt.subplots(1, 2, figsize=(10, 4))   # axs[0] is left, axs[1] is right
```

- The first number is always rows and the second is columns.
- Each Axes has its own title, labels and data, so every `set_` call goes on `axs[0]` or `axs[1]`.
- For a grid such as `plt.subplots(2, 2)`, `axs` is 2-D and you index it as `axs[row, col]`.

---

## 5. Text, annotations, grid and legend (slides 12–15)

### Titles, labels and free text (slide 12)

The slide text says `label()` and `title()`, but the Axes methods are `set_xlabel()`, `set_ylabel()` and `set_title()`.

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

fig, ax = plt.subplots()

ax.scatter(x, y)

ax.set_title("Square Numbers")
ax.set_xlabel("Number")
ax.set_ylabel("Square")

ax.text(1, 1.5, "First")      # ax.text(x_position, y_position, "Text")
ax.text(2, 4.5, "Second")
ax.text(3, 9.5, "Third")
ax.text(4, 16.5, "Fourth")

plt.show()
```

The position in `ax.text()` is in data coordinates, the same numbers as on the axes. Each label here sits 0.5 above its point.

### Annotations (slide 13)

`ax.annotate()` adds text and an arrow pointing at a data point.

```python
fig, ax = plt.subplots()

ax.plot(x, y, marker="o")

ax.annotate(
    "Highest value",
    xy=(4, 16),                       # the point being highlighted (arrow tip)
    xytext=(3, 13),                   # where the text is written
    arrowprops={"arrowstyle": "->"}   # how the arrow looks
)

plt.show()
```

Use `text` for a plain label and `annotate` when you want to point at something.

### Grid and legend (slide 14)

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
squares = [1, 4, 9, 16]
cubes = [1, 8, 27, 64]

fig, ax = plt.subplots()

ax.plot(x, squares, marker="o", label="Squares")
ax.plot(x, cubes, marker="s", label="Cubes")

ax.set_title("Squares and Cubes")
ax.set_xlabel("Number")
ax.set_ylabel("Value")

ax.grid(True, linestyle="--", alpha=0.6)   # dashed, slightly transparent gridlines
ax.legend()

plt.show()
```

- Use a legend when there are several series to tell apart.
- Use gridlines when they help the reader estimate values, not as decoration.
- Setting `label=` on each `plot()` call is the clearest way to feed the legend.

### Legend position (slide 15)

The default is `loc="best"`, where Matplotlib picks a spot that avoids the data. You can set `loc` with a string or a number.

| Code | String | Code | String |
|---|---|---|---|
| 0 | best | 6 | center left |
| 1 | upper right | 7 | center right |
| 2 | upper left | 8 | lower center |
| 3 | lower left | 9 | upper center |
| 4 | lower right | 10 | center |
| 5 | right | | |

```python
ax.legend(loc="upper left")   # same as ax.legend(loc=2)
ax.legend(loc=10)             # the slide's example: centre of the plot
```

Codes 1–4 go anticlockwise from the top right. Strings are easier to read, so prefer them in your own code.

---

## 6. Saving figures and handling dates (slides 16–18)

### Saving (slide 16)

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

fig, ax = plt.subplots()

ax.plot(x, y, marker="o")
ax.set_title("Square Numbers")
ax.set_xlabel("Number")
ax.set_ylabel("Square")

fig.savefig(
    "square_numbers.png",
    dpi=300,                # resolution, for raster formats such as PNG
    bbox_inches="tight"     # trims extra whitespace around the figure
)

fig.savefig("square_numbers.pdf")   # the file extension chooses the format
fig.savefig("square_numbers.svg")

plt.show()
```

- **PNG:** raster image, good for slides and websites. `dpi` matters here.
- **PDF:** good for documents, scales cleanly.
- **SVG:** vector format, resizes with no loss of quality.
- `savefig` is a method on the Figure (`fig`), not on the Axes.
- Save before the figure is closed. Calling `savefig` after `plt.show()` can give a blank file.

### Dates (slide 17)

Matplotlib plots Python `datetime` values directly on an axis.

```python
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

dates = [
    datetime.date(2026, 1, 10),
    datetime.date(2026, 2, 10),
    datetime.date(2026, 3, 10),
    datetime.date(2026, 4, 10)
]

values = [12, 18, 15, 21]

fig, ax = plt.subplots()

ax.plot(dates, values, marker="o")

ax.set_title("Values Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Value")

# Format dates as abbreviated month + year, e.g. "Jan 2026"
ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%b %Y")
)

# Rotate/align date labels automatically
fig.autofmt_xdate()

plt.show()
```

Two separate jobs:

- **`DateFormatter("%b %Y")`:** changes the text of the date labels. It does not move, sort or rotate anything.
- **`fig.autofmt_xdate()`:** rotates and aligns the labels so they don't overlap.

### Date format codes (slide 18)

| Code | Meaning | Example |
|---|---|---|
| `%d` | day | 10 |
| `%b` | abbreviated month | Jan |
| `%B` | full month | January |
| `%m` | month number | 01 |
| `%Y` | four-digit year | 2026 |

So `"%d %B %Y"` gives "10 January 2026" and `"%d/%m/%Y"` gives "10/01/2026".

---

## 7. Line charts (slides 19–20)

A line chart is a sequence of (x, y) points joined by a line. Use it for change over time, trends, ordered numerical data, and comparing related series.

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]

y = [12, 18, 15, 22, 25]
y1 = [10, 14, 17, 19, 23]
y2 = [8, 12, 16, 18, 21]

fig, ax = plt.subplots()

# Customised line
ax.plot(
    x,
    y,
    color="red",
    linestyle="--",
    linewidth=3,
    marker="o",
    label="Main Series"
)

# Additional series, drawn with default styling
ax.plot(x, y1, label="Series 1")
ax.plot(x, y2, label="Series 2")

ax.set_title("Values Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()

plt.show()
```

Single-letter colour codes:

| Code | Colour | Code | Colour |
|---|---|---|---|
| `b` | blue | `m` | magenta |
| `g` | green | `y` | yellow |
| `r` | red | `k` | black |
| `c` | cyan | `w` | white |

Black is `k` because `b` is already blue. `color="r"` and `color="red"` do the same thing.

### Line chart from a pandas DataFrame (slide 20)

```python
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Series 1": [1, 3, 4, 3, 5],
    "Series 2": [2, 4, 5, 2, 4],
    "Series 3": [3, 2, 3, 1, 3]
}

df = pd.DataFrame(data)

ax = df.plot()          # line chart by default; returns the Axes

ax.set_title("Multiple Series from a DataFrame")
ax.set_xlabel("Index")
ax.set_ylabel("Value")

plt.show()
```

- `df.plot()` draws a line chart unless you pass `kind=`.
- Each numeric column becomes one line.
- The row index (0–4 here) goes on the x-axis.
- The legend is filled in automatically from the column names.
- `df.plot()` returns an Axes, so you customise it with the same `ax.set_...` methods.

---

## 8. Histograms (slides 21–22)

A histogram shows the distribution of numerical data by grouping values into intervals called bins.

- The x-axis shows ranges of values.
- The y-axis shows how many observations fall in each range.
- The bars touch, because the bins are adjacent intervals on a number line.

```python
import numpy as np
import matplotlib.pyplot as plt

data = np.random.randint(0, 100, 100)   # 100 random integers from 0 to 99

fig, ax = plt.subplots()

ax.hist(data, bins=20)                  # split the range into 20 bins

ax.set_title("Distribution of Random Values")
ax.set_xlabel("Value")
ax.set_ylabel("Frequency")

plt.show()
```

- `np.random.randint(low, high, size)` excludes `high`, so the values run from 0 to 99.
- If you leave out `bins`, the default is 10.
- More bins give more detail but a noisier shape. Fewer bins give a smoother shape but hide detail.
- The data is random, so the chart looks different every time you run it.

---

## 9. Bar charts (slides 23–31)

A bar chart compares values across discrete categories. Categories go on the x-axis and bar height is the value. The bars are separated because the categories are distinct, which is the visual difference from a histogram.

### Basic bar chart (slide 23)

```python
import matplotlib.pyplot as plt

categories = ["A", "B", "C", "D", "E"]
values = [5, 7, 3, 4, 6]

fig, ax = plt.subplots()

ax.bar(categories, values)

ax.set_title("Values by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Value")

plt.show()
```

### Customising (slide 24)

```python
ax.bar(
    categories,
    values,
    width=0.7,          # bar width (default 0.8)
    alpha=0.8,          # transparency: 0 = invisible, 1 = solid
    label="Series 1"
)
ax.legend()
```

| Argument | Purpose |
|---|---|
| `width` | width of the bars |
| `alpha` | transparency, from 0 (fully transparent) to 1 (fully opaque) |
| `label` | name of the series for the legend |
| `yerr` | adds vertical error bars |
| `capsize` | size of the caps on the error bars |

### Error bars (slide 25)

```python
categories = ["A", "B", "C", "D", "E"]

means = [5, 7, 3, 4, 6]
sd = [0.8, 1.0, 0.4, 0.9, 1.3]

fig, ax = plt.subplots()

ax.bar(
    categories,
    means,
    yerr=sd,        # one error value per bar, drawn above and below the top
    capsize=5
)

ax.set_title("Mean Values with Standard Deviation")
ax.set_xlabel("Category")
ax.set_ylabel("Mean Value")

plt.show()
```

The error-bar styling can also be passed as a dictionary:

```python
ax.bar(categories, means, yerr=sd,
       error_kw={"ecolor": "black", "capsize": 5})   # ecolor = error bar colour
```

The values in `yerr` could mean different things:

- **Standard deviation (SD):** variability in the observed data.
- **Standard error (SE):** uncertainty in the estimated mean.
- **Confidence interval (CI):** a range of uncertainty around an estimate.

Matplotlib only draws the numbers. The chart must say which one they are, which is why this example puts "Standard Deviation" in the title.

### Horizontal bars (slide 26)

```python
fig, ax = plt.subplots()

errors = [0.8, 1.0, 0.4, 0.9, 1.3]

ax.barh(
    categories,     # categories now go on the y-axis
    values,         # values now go along the x-axis
    xerr=errors,    # xerr, not yerr, because the bars run horizontally
    capsize=5
)

ax.set_title("Values by Category")
ax.set_xlabel("Value")
ax.set_ylabel("Category")

plt.show()
```

`barh` swaps the roles of the two axes, so the axis labels swap and `yerr` becomes `xerr`. Horizontal bars suit long category names or many categories.

### Multiseries (grouped) bar chart (slide 27)

Each category gets several bars side by side, one per series.

```python
import numpy as np
import matplotlib.pyplot as plt

categories = ["A", "B", "C", "D", "E"]

series1 = [5, 7, 3, 4, 6]
series2 = [6, 6, 4, 5, 7]
series3 = [5, 6, 5, 4, 6]

x = np.arange(len(categories))   # [0, 1, 2, 3, 4]: one number per category
width = 0.25                     # width of each bar

fig, ax = plt.subplots()

ax.bar(x - width, series1, width, label="Series 1")   # shifted left
ax.bar(x,         series2, width, label="Series 2")   # centred
ax.bar(x + width, series3, width, label="Series 3")   # shifted right

ax.set_title("Multiseries Bar Chart")
ax.set_xlabel("Category")
ax.set_ylabel("Value")

ax.set_xticks(x)                  # put a tick at the centre of each group
ax.set_xticklabels(categories)    # and label it with the category name

ax.legend()

plt.show()
```

How it works:

1. Bars can't be offset from text labels, so the categories are first turned into numbers with `np.arange`.
2. Each series is drawn at a slightly different x position: `x - width`, `x`, `x + width`.
3. The third argument is the bar width. Three bars of 0.25 fill 0.75 of each slot, leaving a gap between groups.
4. `set_xticks` and `set_xticklabels` put the category names back on the axis.

### Multiseries horizontal bar chart (slide 28)

The same idea with every x swapped for y and `width` for `height`.

```python
y = np.arange(len(categories))
height = 0.25

fig, ax = plt.subplots()

ax.barh(y - height, series1, height, label="Series 1")
ax.barh(y,          series2, height, label="Series 2")
ax.barh(y + height, series3, height, label="Series 3")

ax.set_yticks(y)
ax.set_yticklabels(categories)

ax.set_title("Multiseries Horizontal Bar Chart")
ax.set_xlabel("Value")
ax.set_ylabel("Category")

ax.legend()
plt.show()
```

### Grouped bars with pandas (slide 29)

pandas does all the offset work for you.

```python
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Series 1": [1, 4, 4, 3, 5],
    "Series 2": [2, 4, 5, 2, 4],
    "Series 3": [3, 2, 3, 1, 3]
}

df = pd.DataFrame(data)

ax = df.plot(kind="bar")      # kind="barh" gives the horizontal version

ax.set_title("Multiseries Bar Chart")
ax.set_xlabel("Category")
ax.set_ylabel("Value")

plt.show()
```

Each row is one group of bars and each numeric column is one series.

### Stacked bar chart with pandas (slide 30)

A stacked bar shows how several series add up to a total for each category.

```python
df = pd.DataFrame(
    data,
    index=["A", "B", "C", "D", "E"]   # row labels become the category names
)

ax = df.plot(
    kind="bar",        # kind="barh" for horizontal stacked bars
    stacked=True       # put the series on top of each other
)

ax.set_title("Stacked Bar Chart")
ax.set_xlabel("Category")
ax.set_ylabel("Value")

plt.show()
```

- Each bar is one category and each coloured section is one series.
- The full height of the bar is the combined total.
- Stacked is good for totals and composition. Grouped is better when individual values need to be compared accurately, because only the bottom section of a stacked bar starts at zero.

### Diverging bar chart (slide 31)

Bars go in opposite directions from a common baseline, usually zero. Use it for positive vs negative values, increases vs decreases, or opposing groups.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(8)

positive = [1, 3, 4, 6, 4, 3, 2, 1]
negative = [-1, -2, -5, -4, -3, -3, -2, -1]

fig, ax = plt.subplots()

bars1 = ax.bar(x, positive, label="Positive")   # bars going up
bars2 = ax.bar(x, negative, label="Negative")   # negative heights go down

ax.axhline(0, linewidth=1)                      # horizontal line at y = 0: the baseline

ax.bar_label(bars1, padding=3)                  # write each value at the end of its bar
ax.bar_label(bars2, padding=3)

ax.set_title("Diverging Bar Chart")
ax.set_ylabel("Value")
ax.legend()

plt.show()
```

- `ax.bar()` returns the group of bars it drew. Saving it in a variable lets `bar_label` find them.
- `ax.bar_label(bars, padding=3)` adds the value labels, 3 points away from the bar end.
- `ax.axhline(0)` draws a horizontal line across the whole plot at y = 0.

---

## 10. Pie charts (slides 32–33)

A pie chart shows how categories make up a single whole. Use one only when:

- the categories are parts of the same total;
- the values are non-negative;
- there are only a few categories;
- approximate proportions matter more than precise values.

```python
import matplotlib.pyplot as plt

labels = ["A", "B", "C", "D"]
values = [25, 35, 20, 20]

fig, ax = plt.subplots()

ax.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",       # displays percentages, to one decimal place
    startangle=90,           # rotates the starting position
    explode=(0, 0.1, 0, 0)   # emphasises one slice (B)
)

ax.set_title("Share by Category")

plt.show()
```

- `ax.pie()` converts the values into proportions of their total, so they don't need to sum to 100.
- `autopct="%1.1f%%"`: `%1.1f` is a number with one decimal place and `%%` is a literal percent sign, giving "35.0%".
- `explode`: one number per slice, the distance it is pushed out from the centre. Only non-zero slices move.
- `startangle`: degrees of rotation, 0 to 360, default 0. With 0 the first slice starts at 3 o'clock; with 90 it starts at 12 o'clock. Slices then go anticlockwise.
- `shadow=True` adds a shadow under the pie.

### Pie chart from a pandas Series (slide 33)

A pie chart can show only one data series, so you select one column.

```python
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Category": ["A", "B", "C", "D"],
    "Sales": [25, 35, 20, 20]
}

df = pd.DataFrame(data)

ax = df.set_index("Category")["Sales"].plot(
    kind="pie",
    autopct="%1.1f%%",
    ylabel=""
)

ax.set_title("Share of Sales by Category")

plt.show()
```

Reading the chained line left to right:

1. `df.set_index("Category")` makes the category names the row labels, which become the slice labels.
2. `["Sales"]` selects one column, giving a pandas Series.
3. `.plot(kind="pie", ...)` draws it as a pie.
4. `ylabel=""` removes the word "Sales" that pandas would otherwise print at the side.

---

## 11. Scatter plots (slide 34)

A scatter plot shows the relationship between two numerical variables. Each point is one observation with an (x, y) pair. It helps you spot positive or negative relationships, clusters, gaps and outliers.

### Basic

```python
import matplotlib.pyplot as plt

study_hours = [2, 3, 4, 5, 6, 7]
marks = [48, 55, 61, 69, 75, 82]

fig, ax = plt.subplots()

ax.scatter(study_hours, marks)

ax.set_title("Study Hours and Marks")
ax.set_xlabel("Study Hours")
ax.set_ylabel("Mark")

plt.show()
```

The points rise from left to right, which is a positive relationship: more hours go with higher marks.

### Extra variables through size and colour

```python
sizes = [40, 60, 80, 100, 120, 140]
engagement = [3, 4, 5, 6, 7, 8]

fig, ax = plt.subplots()

scatter = ax.scatter(
    study_hours,
    marks,
    s=sizes,            # marker size, one value per point
    c=engagement,       # numbers that decide each point's colour
    cmap="viridis",     # the colour map used to turn those numbers into colours
    alpha=0.7           # transparency, useful when points overlap
)

ax.set_title("Study Hours, Marks and Engagement")
ax.set_xlabel("Study Hours")
ax.set_ylabel("Mark")

fig.colorbar(
    scatter,            # the scatter whose colours the bar explains
    ax=ax,
    label="Engagement"
)

plt.show()
```

One scatter plot can carry four variables: x position, y position, marker size (`s`) and marker colour (`c`). The colour bar is the legend for the colours, so it is needed whenever `c` holds numbers.

### Two groups with different markers

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)     # random generator with a fixed seed: same numbers every run

# Generate two groups
x1 = rng.integers(30, 40, 50)       # 50 integers from 30 to 39
y1 = rng.integers(20, 30, 50)

x2 = rng.integers(50, 70, 50)       # 50 integers from 50 to 69: a higher x range
y2 = rng.integers(20, 30, 50)

fig, ax = plt.subplots()

ax.scatter(x1, y1, marker="o", label="Group 1")   # circles
ax.scatter(x2, y2, marker="^", label="Group 2")   # triangles

ax.set_title("Comparison of Two Randomly Generated Groups")
ax.set_xlabel("X value")
ax.set_ylabel("Y value")

ax.legend()

plt.show()
```

- `rng.integers(low, high, size)` excludes `high`, like `randint`.
- The seed (42) makes the "random" data reproducible.
- Two `scatter()` calls with different markers and labels show two clusters on the same Axes.

---

## 12. Box plots (slides 35–36)

A box plot summarises the distribution of numerical data in five numbers, and makes groups easy to compare.

How to read one:

- **Line inside the box:** the median (the middle value).
- **Box:** the interquartile range (IQR), from Q1 (25th percentile) to Q3 (75th percentile). It holds the middle 50% of the values.
- **Whiskers:** extend to the furthest values that are still within 1.5 × IQR of the box.
- **Points beyond the whiskers:** possible outliers.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

group1 = rng.normal(50, 10, 100)   # 100 values, mean 50, standard deviation 10
group2 = rng.normal(65, 12, 100)
group3 = rng.normal(55, 15, 100)

fig, ax = plt.subplots()

ax.boxplot(
    [group1, group2, group3],                       # a list of datasets: one box each
    tick_labels=["Group 1", "Group 2", "Group 3"]   # names under each box
)

ax.set_title("Distribution of Values by Group")
ax.set_ylabel("Value")

plt.show()
```

- `rng.normal(mean, sd, n)` draws n values from a normal distribution.
- A higher median line means a higher typical value (Group 2 here). A taller box and longer whiskers mean more spread (Group 3 here).
- `tick_labels=` is the name in Matplotlib 3.9 and later. Older versions call it `labels=`.

### Box plot from a pandas DataFrame (slide 36)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

data = {
    "Group": (
        ["Group 1"] * 100 +      # list repetition: 100 copies of "Group 1"
        ["Group 2"] * 100 +
        ["Group 3"] * 100
    ),
    "Value": np.concatenate([    # join the three arrays into one of 300 values
        rng.normal(50, 10, 100),
        rng.normal(65, 12, 100),
        rng.normal(55, 15, 100)
    ])
}

df = pd.DataFrame(data)

ax = df.boxplot(
    column="Value",    # the numerical column to summarise
    by="Group",        # the column that splits the rows into groups
    grid=False
)

ax.set_title("Distribution of Values by Group")
ax.set_xlabel("Group")
ax.set_ylabel("Value")

plt.suptitle("")       # removes the extra title pandas adds automatically
plt.show()
```

- The data is in long format: one row per observation, with one column saying which group it belongs to.
- `df.boxplot(column=..., by=...)` draws one box per group.
- `by=` makes pandas add an overall title ("Boxplot grouped by Group"). `plt.suptitle("")` clears it.

---

## 13. Inset Axes (slide 37)

An inset Axes is a small plotting area placed inside a main Axes. It is useful for a zoomed-in region, a related secondary view, or highlighting a subset of the data.

```python
import numpy as np
import matplotlib.pyplot as plt

# Create x-values from 0 to 9
x = np.arange(10)

# Define the corresponding y-values
y = [1, 2, 7, 1, 5, 2, 4, 2, 3, 1]

# Create the Figure and the main Axes
fig, ax = plt.subplots()

# Plot the data on the main Axes
ax.plot(x, y)
ax.set_title("Main Plot")

# Create a smaller Axes inside the main Axes
# [left, bottom, width, height]
# Values are given relative to the size of the main Axes
inset_ax = ax.inset_axes([0.62, 0.58, 0.3, 0.3])

# Plot the same data inside the inset Axes
inset_ax.plot(x, y)
inset_ax.set_title("Inset", fontsize=9)

plt.show()
```

- The four numbers are fractions of the main Axes, not data values: the inset starts 62% across and 58% up, and is 30% wide and 30% tall.
- `inset_ax` is a normal Axes, so it has its own `plot`, `set_title` and so on.
- It lives inside the same Figure. It is not a second Figure.

---

## 14. Quiz traps

- **Figure vs Axes:** the Figure is the canvas and the Axes is the plot. `savefig`, `autofmt_xdate` and `colorbar` are called on `fig`; plotting and labelling are called on `ax`.
- **Histogram vs bar chart:** histogram for the distribution of numerical values in bins (bars touch); bar chart for comparing categories (bars separated).
- **`plt.subplots(rows, columns)`:** `(2, 1)` is stacked vertically and `(1, 2)` is side by side.
- **`label=` needs `ax.legend()`:** without the legend call the names never appear.
- **Legend codes:** 1 upper right, 2 upper left, 3 lower left, 4 lower right, 10 center, 0 best.
- **Default bins:** 10.
- **`barh` uses `xerr`:** `bar` uses `yerr`.
- **Error bars:** they could be SD, SE or a CI, so the chart must say which.
- **Grouped vs stacked:** grouped for comparing individual values, stacked for totals and composition.
- **Pie charts:** parts of one whole, few categories, non-negative values. One data series only.
- **`autopct="%1.1f%%"`:** percentage with one decimal place.
- **`explode`:** only the slices with a non-zero value move.
- **`startangle`:** default 0.
- **Date labels:** `DateFormatter` changes the text; `autofmt_xdate` rotates it.
- **`%b` vs `%B`:** Jan vs January. `%m` is the month number and `%Y` is the four-digit year.
- **Colour code `k`:** black.
- **`df.plot()`:** line chart by default; `kind="bar"`, `"barh"` or `"pie"` changes it, and `stacked=True` stacks the bars.
- **`plt.suptitle("")`:** removes the automatic title from `df.boxplot(by=...)`.
- **Box plot:** median line, box from Q1 to Q3, whiskers, outlier points.
- **`inset_axes([left, bottom, width, height])`:** fractions of the main Axes.
- **Upper bounds are excluded:** in `np.arange`, `np.random.randint` and `rng.integers`.
- **Save before closing:** call `savefig` before `plt.show()`.
