from helpers import mcq, tf, out, fill

SUBJECT = "plotting"

TOPICS = [
    ("fig-axes", "The Figure / Axes model"),
    ("plot-types", "Line, bar, scatter, hist and box plots"),
    ("labels-legends", "Titles, labels, legends and styling"),
    ("subplots", "Subplot grids"),
    ("pandas-plot", "Plotting from pandas"),
    ("training-curves", "Training curves and reading them"),
    ("heatmaps", "imshow and confusion-matrix heatmaps"),
    ("choosing", "Choosing a chart and log scales"),
    ("pitfalls", "pyplot vs OO API, show/close/savefig"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ fig-axes
    mcq("In matplotlib, what is the difference between a Figure and an Axes?",
        ["The Figure is the whole canvas/window; an Axes is one plot area inside it, with its own x and y axis",
         "They are two names for the same thing",
         "An Axes holds several Figures",
         "The Figure is the x axis and the Axes is the y axis"], 0,
        "One is the page, the other is a chart drawn on the page.",
        "A Figure is the top-level container (the image you save). Each Axes is a single plot with its own data, ticks, labels and title. One Figure can hold many Axes.",
        analogy="Figure = the browser page; Axes = one chart component on that page.",
        diagram="""
+---------------- Figure ----------------+
|  +---- Axes ----+   +---- Axes ----+   |
|  |  title       |   |  title       |   |
|  |  y  /\\_/     |   |  y   . .     |   |
|  |     x        |   |      x       |   |
|  +--------------+   +--------------+   |
+----------------------------------------+""",
        topic="fig-axes", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
print(type(fig).__name__, type(ax).__name__, len(fig.axes))""",
        ["Figure Axes 1", "Figure ndarray 1", "Axes Figure 1", "Figure Axes 0"], 0,
        "With no arguments, subplots makes one plot area.",
        "plt.subplots() returns a (Figure, Axes) pair; the figure holds exactly one Axes.",
        topic="fig-axes", level=1),
    fill("The recommended way to start a plot is `fig, ax = plt.____()`.",
        "subplots",
        "It creates the figure and the axes in one call.",
        "plt.subplots() returns the Figure and Axes objects so you can call methods on ax directly (the object-oriented style).",
        topic="fig-axes", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.plot([1, 2, 3], [6, 5, 4])
print(len(ax.lines))""",
        ["2", "1", "6", "0"], 0,
        "Each plot() call adds a line to the same Axes.",
        "Calling ax.plot twice draws two lines on the same axes; ax.lines holds both Line2D objects.",
        topic="fig-axes", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
result = ax.plot([1, 2, 3])
print(type(result).__name__, len(result), type(result[0]).__name__)""",
        ["list 1 Line2D", "Line2D 1 Line2D", "Axes 1 Line2D", "list 3 float"], 0,
        "plot can draw several lines in one call, so it returns a container.",
        "ax.plot returns a list of Line2D objects (one per line drawn). Hence the idiom `line, = ax.plot(...)` to unpack a single line.",
        topic="fig-axes", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
x, y = ax.lines[0].get_data()
print([int(v) for v in x], [int(v) for v in y])""",
        ["[1, 2, 3] [1, 4, 9]", "[0, 1, 2] [1, 4, 9]", "[1, 4, 9] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]"], 0,
        "plot(x, y): first argument is x.",
        "With two arguments the first is x and the second is y. The Line2D object stores both.",
        topic="fig-axes", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([10, 20, 30])
x, y = ax.lines[0].get_data()
print(list(map(int, x)))""",
        ["[0, 1, 2]", "[1, 2, 3]", "[10, 20, 30]", "[]"], 0,
        "With one list, what does matplotlib use for x?",
        "If you pass only y, matplotlib uses x = 0, 1, 2, ... (the positions). Training-loss plots made this way start at epoch 0.",
        topic="fig-axes", level=2),
    out("""import matplotlib.pyplot as plt
print(plt.rcParams["figure.figsize"], plt.rcParams["figure.dpi"])
fig = plt.figure(figsize=(8, 3))
print(fig.get_size_inches().tolist())""",
        ["[6.4, 4.8] 100.0\n[8.0, 3.0]", "[8.0, 6.0] 72.0\n[8.0, 3.0]", "[6.4, 4.8] 100.0\n[3.0, 8.0]", "(6.4, 4.8) 100\n(8, 3)"], 0,
        "figsize is (width, height) in inches.",
        "The default size is 6.4 x 4.8 inches at 100 dpi (640 x 480 pixels). figsize=(8, 3) means 8 inches wide, 3 tall.",
        topic="fig-axes", level=2),
    out("""import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
ax3 = ax1.twinx()
print(len(fig.axes))""",
        ["3", "2", "1", "4"], 0,
        "twinx creates a brand-new Axes sharing the x axis.",
        "Two subplots plus a twin axes (a second y axis on the right of ax1) = 3 Axes objects in the figure.",
        topic="fig-axes", level=3),
    mcq("What is an 'Artist' in matplotlib?",
        ["Any object that can be drawn on a figure: Figure, Axes, Line2D, Text, Patch, etc.",
         "The backend that renders PNG files",
         "A colour theme",
         "A function that saves a figure"], 0,
        "Everything you see is one.",
        "Everything visible is an Artist. Containers (Figure, Axes) hold primitives (Line2D, Rectangle, Text). Calling ax.plot creates Line2D artists and adds them to the Axes.",
        topic="fig-axes", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2])
ax.bar(["a", "b"], [1, 2])
ax.scatter([1, 2], [3, 4])
ax.text(0, 0, "hi")
print(len(ax.lines), len(ax.patches), len(ax.collections), len(ax.texts))""",
        ["1 2 1 1", "1 1 1 1", "4 0 0 0", "1 2 2 1"], 0,
        "Each chart type creates a different kind of Artist and stores it in a different list.",
        "A line is a Line2D in ax.lines; each bar is a Rectangle patch (2 patches); scatter is one PathCollection in ax.collections; text goes to ax.texts.",
        topic="fig-axes", level=4),
    mcq("Why does calling `ax.plot` twice put two lines on the same chart instead of replacing the first one?",
        ["An Axes is a container: every plotting call adds artists to it until you clear it",
         "matplotlib merges the two datasets into one line",
         "The second call creates a hidden second figure",
         "The first line is replaced but stays in memory"], 0,
        "Think about what ax.plot does to ax.",
        "An Axes accumulates artists. That is why overlaying train and val curves is just two plot calls, and why you must use ax.cla() or a new Axes to start fresh.",
        topic="fig-axes", level=2),

    # ------------------------------------------------------------------ plot-types
    mcq("Which chart is best for showing how training loss changes over 50 epochs?",
        ["Line plot", "Pie chart", "Bar chart of each epoch's loss", "Box plot"], 0,
        "Ordered x values, a trend over time.",
        "A line plot connects values in order, which makes the trend (going down, levelling off, going up) easy to see.",
        topic="plot-types", level=1),
    mcq("Which chart shows the relationship between two numeric variables, such as height and weight for 500 people?",
        ["Scatter plot", "Line plot", "Pie chart", "Histogram"], 0,
        "One dot per person.",
        "A scatter plot puts one point per row at (height, weight), so you can see correlation, clusters and outliers. A line plot would connect points in row order, which means nothing here.",
        topic="plot-types", level=1),
    mcq("What does a histogram show?",
        ["How the values of ONE numeric variable are distributed, by counting how many fall into each bin",
         "How two variables relate to each other",
         "Values over time",
         "Category totals in decreasing order"], 0,
        "Bins and counts.",
        "A histogram splits the value range into bins and draws a bar for the count in each, showing the shape (skew, peaks, outliers) of the distribution.",
        topic="plot-types", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
n, bins, patches = ax.hist([1, 2, 2, 3, 3, 3], bins=3)
print([int(c) for c in n], len(bins), len(patches))""",
        ["[1, 2, 3] 4 3", "[1, 2, 3] 3 3", "[3, 2, 1] 4 3", "[6] 2 1"], 0,
        "3 bins need how many edges?",
        "hist returns the counts per bin, the bin EDGES and the bar patches. 3 bins have 4 edges; the counts are 1, 2, 3.",
        topic="plot-types", level=2),
    out("""import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
ax.hist(np.arange(100))
print(len(ax.patches))""",
        ["10", "100", "20", "1"], 0,
        "What is the default number of bins?",
        "hist uses bins=10 by default, so 10 rectangle patches. The default often hides detail; try bins=30 or bins='auto'.",
        topic="plot-types", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
bars = ax.bar(["cat", "dog", "fish"], [5, 3, 1])
print(type(bars).__name__, len(bars), bars[0].get_height())""",
        ["BarContainer 3 5", "list 3 5", "BarContainer 1 5", "Rectangle 3 5"], 0,
        "Each bar is a Rectangle; bar returns a container of them.",
        "ax.bar returns a BarContainer holding one Rectangle per category; you can index it like a list and read each bar's height.",
        topic="plot-types", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
bp = ax.boxplot([1, 2, 3, 4, 100])
print(len(bp["fliers"][0].get_ydata()), len(bp["medians"]))""",
        ["1 1", "0 1", "5 1", "1 5"], 0,
        "Fliers are points beyond the whiskers (1.5 x IQR).",
        "The box covers the middle 50% (2 to 4); whiskers extend at most 1.5 x IQR. 100 is far outside, so it is drawn as 1 flier (outlier). One box means one median line.",
        diagram="""
   o        <- flier (100)

  ---       <- whisker end
   |
 +---+      <- Q3
 |---|      <- median
 +---+      <- Q1
   |
  ---""",
        topic="plot-types", level=3),
    mcq("When should you use a box plot instead of a histogram?",
        ["To compare the distribution of a value across several groups side by side (e.g. salary per department)",
         "To show a trend over time",
         "To show parts of a whole",
         "To show one exact value"], 0,
        "Box plots are compact.",
        "Each box summarises a distribution in five numbers plus outliers, so many groups fit side by side. Overlaid histograms get messy beyond two or three groups.",
        topic="plot-types", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.barh(["x", "y", "z"], [3, 1, 2])
print(len(ax.patches), [float(p.get_width()) for p in ax.patches])""",
        ["3 [3.0, 1.0, 2.0]", "3 [0.8, 0.8, 0.8]", "1 [3.0]", "3 [1.0, 2.0, 3.0]"], 0,
        "In a horizontal bar chart, the value is the bar's width.",
        "barh draws one horizontal Rectangle per category; the value sets the width. Horizontal bars are great when category names are long.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
sc = ax.scatter([1, 2, 3], [3, 1, 2], c=[0.1, 0.5, 0.9], s=[10, 20, 30])
print(type(sc).__name__, len(sc.get_offsets()), len(ax.collections))""",
        ["PathCollection 3 1", "Line2D 3 3", "PathCollection 1 3", "list 3 1"], 0,
        "A scatter is ONE collection of many markers.",
        "scatter returns a single PathCollection holding all 3 points; c and s set per-point colour and size, letting you show 4 variables in one chart.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 2, 3], "o")
print(ax.lines[0].get_linestyle(), ax.lines[0].get_marker(), len(ax.collections))""",
        ["None o 0", "- o 0", "None o 1", "- None 0"], 0,
        "A format string with only a marker means 'no connecting line'.",
        "plot(x, y, 'o') draws markers only (linestyle 'None'). It is still a Line2D, not a scatter collection, and is faster than scatter when all points share size and colour.",
        topic="plot-types", level=4),
    mcq("You plot 1 million points with `ax.scatter` and the chart is a solid blob. What is the best fix?",
        ["Use small markers with transparency (alpha), or a 2-D density plot like hexbin / hist2d",
         "Use a pie chart",
         "Use a thicker line",
         "Plot only the first 10 points"], 0,
        "Overplotting hides density.",
        "When points overlap, you can't tell 10 from 10,000. Lower alpha and marker size, sample the data, or switch to hexbin / hist2d, which show counts per region.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.errorbar([1, 2], [1, 2], yerr=0.1)
ax.fill_between([0, 1], [0, 1], [1, 2])
ax.axhline(0.5)
print(len(ax.lines), len(ax.collections), len(ax.containers))""",
        ["2 2 1", "3 1 1", "2 1 0", "1 2 1"], 0,
        "axhline is a line; fill_between is a collection; errorbar draws a line plus a collection of bars.",
        "errorbar adds 1 data line plus a LineCollection for the error bars and an ErrorbarContainer; fill_between adds a PolyCollection; axhline adds a Line2D. So 2 lines, 2 collections, 1 container.",
        topic="plot-types", level=4),

    # ------------------------------------------------------------------ labels-legends
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_title("Loss")
ax.set_xlabel("epoch")
print(ax.get_title(), ax.get_xlabel(), repr(ax.get_ylabel()))""",
        ["Loss epoch ''", "Loss epoch None", "Loss epoch 'y'", "'Loss' 'epoch' ''"], 0,
        "A label that was never set is an empty string.",
        "set_title/set_xlabel store the text; get_ylabel returns '' because no y label was set. Always label both axes (with units).",
        topic="labels-legends", level=1),
    mcq("What does `ax.legend()` need to show an entry for a line?",
        ["The line must have a label, e.g. ax.plot(x, y, label='train')",
         "Nothing: it lists every line automatically as 'line 1', 'line 2'",
         "The line must be red",
         "You must call plt.show() first"], 0,
        "Where does the legend text come from?",
        "legend() collects artists that have a label. Lines without one are skipped (matplotlib warns 'No artists with labels found').",
        topic="labels-legends", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2], label="train")
ax.plot([2, 1], label="val")
ax.plot([1, 1])
leg = ax.legend()
print([t.get_text() for t in leg.get_texts()])""",
        ["['train', 'val']", "['train', 'val', '']", "['train', 'val', 'line2']", "[]"], 0,
        "Unlabelled lines don't appear.",
        "Only artists with a label are added to the legend; the third line has none.",
        topic="labels-legends", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2], label="train")
ax.plot([2, 1], label="_baseline")
print(len(ax.legend().get_texts()))""",
        ["1", "2", "0", "ValueError"], 0,
        "Labels starting with an underscore are special.",
        "A label beginning with '_' tells legend() to ignore the artist. That's how matplotlib hides helper artists.",
        topic="labels-legends", level=3),
    fill("To set the title of an Axes object in the OO style, call `ax.____('Accuracy')`.",
        "set_title",
        "The OO setters start with set_.",
        "ax.set_title sets the Axes title. The pyplot equivalent is plt.title.",
        topic="labels-legends", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1], "r--")
ln = ax.lines[0]
print(ln.get_color(), ln.get_linestyle())""",
        ["r --", "red dashed", "#ff0000 --", "r -"], 0,
        "The format string packs colour and line style.",
        "'r--' means red, dashed. get_color returns the value as given ('r'); get_linestyle returns '--'.",
        topic="labels-legends", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
ax.set_xlim(0, 10)
lo, hi = ax.get_xlim()
print(float(lo), float(hi))""",
        ["0.0 10.0", "1.0 3.0", "0 10", "-0.1 2.1"], 0,
        "set_xlim overrides the automatic range.",
        "Without set_xlim the range would be auto-scaled with margins (-0.1 to 2.1). After set_xlim it is exactly 0 to 10.",
        topic="labels-legends", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
lo, hi = ax.get_xlim()
print(round(float(lo), 2), round(float(hi), 2))""",
        ["-0.1 2.1", "0.0 2.0", "1.0 3.0", "0.0 3.0"], 0,
        "matplotlib adds a small margin around the data.",
        "x is 0..2; default axes margins add 5% of the range (0.1) on each side.",
        topic="labels-legends", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.text(0.5, 0.5, "center")
ax.annotate("best", xy=(1, 2), xytext=(2, 3), arrowprops={"arrowstyle": "->"})
print(len(ax.texts))""",
        ["2", "1", "0", "3"], 0,
        "annotate creates a text artist too.",
        "Both ax.text and ax.annotate add Text artists to ax.texts. annotate is ideal for marking e.g. the epoch with the best validation loss.",
        topic="labels-legends", level=3),
    tf("`plt.title('x')` and `ax.set_title('x')` can set titles on different plots if `ax` is not the current Axes.", True,
        "pyplot functions act on the 'current' Axes.",
        "plt.title targets plt.gca(), the most recently active Axes. In a multi-plot figure that may not be the ax you think. Using ax.set_title is explicit.",
        topic="labels-legends", level=3),
    mcq("Your legend covers the most important part of the plot. What's the cleanest fix?",
        ["ax.legend(loc='best') or place it outside with bbox_to_anchor",
         "Delete the legend and explain colours in the title",
         "Make the lines thinner",
         "Call plt.show() twice"], 0,
        "legend has placement options.",
        "loc='best' (the default for Axes legends) tries to avoid data; loc='upper right' etc. choose a corner; bbox_to_anchor=(1.02, 1), loc='upper left' puts it outside the plot.",
        topic="labels-legends", level=2),

    # ------------------------------------------------------------------ subplots
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 3)
print(axs.shape, len(fig.axes))""",
        ["(2, 3) 6", "(3, 2) 6", "(6,) 6", "(2, 3) 1"], 0,
        "subplots(nrows, ncols).",
        "subplots(2, 3) makes 2 rows x 3 columns = 6 Axes, returned as a 2-D NumPy array of shape (2, 3).",
        analogy='Like a CSS grid with 2 rows and 3 columns: each cell is its own chart component.',
        diagram="""
axs[0,0]  axs[0,1]  axs[0,2]
axs[1,0]  axs[1,1]  axs[1,2]""",
        topic="subplots", level=1),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3)
print(axs.shape)""",
        ["(3,)", "(1, 3)", "(3, 1)", "3"], 0,
        "A single row gets squeezed.",
        "By default (squeeze=True) a 1-row or 1-column grid returns a 1-D array, so you index axs[0], not axs[0, 0]. squeeze=False always gives 2-D.",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3)
axs[0, 1].plot([1, 2])""",
        ["IndexError", "TypeError", "KeyError", "(nothing is printed)"], 0,
        "What is the shape of axs here?",
        "axs is 1-D with shape (3,), so a 2-D index raises IndexError ('too many indices for array'). Use axs[1].",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 2)
for ax in axs.flat:
    ax.plot([1, 2])
print(sum(len(ax.lines) for ax in fig.axes))""",
        ["4", "1", "2", "8"], 0,
        "axs.flat walks every Axes in the grid.",
        "axs.flat (or axs.ravel()) iterates all 4 Axes regardless of grid shape; each gets one line.",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(2, 2, 3)
print(ax.get_subplotspec().rowspan.start, ax.get_subplotspec().colspan.start)""",
        ["1 0", "0 2", "1 1", "2 0"], 0,
        "Numbering goes left to right, top to bottom, starting at 1.",
        "In a 2x2 grid, position 3 is the first plot of the second row: row 1, column 0 (0-based).",
        diagram="""
add_subplot(2, 2, k)
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
+---+---+""",
        topic="subplots", level=3),
    mcq("What does `plt.subplots(2, 1, sharex=True)` do?",
        ["Both rows use the same x-axis range, so zooming/limits stay in sync and the top plot's x tick labels can be hidden",
         "It draws the same data twice",
         "It puts both plots on the same Axes",
         "It shares the colour of the lines"], 0,
        "Shared axis = shared limits.",
        "sharex links the x limits of the Axes, ideal for stacking, say, loss and learning rate over the same epochs.",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot([0, 10], [0, 1])
axs[1].plot([0, 5], [0, 1])
print(axs[0].get_xlim() == axs[1].get_xlim())""",
        ["True", "False", "ValueError", "None"], 0,
        "Shared axes autoscale together.",
        "With sharex=True both Axes use one x range that covers all data (0..10 plus margins), so the limits are equal.",
        topic="subplots", level=3),
    mcq("Labels of neighbouring subplots overlap each other. What's the usual fix?",
        ["fig.tight_layout() (or plt.subplots(..., layout='constrained'))",
         "Use fewer data points",
         "Call plt.show() before adding labels",
         "Set dpi=300"], 0,
        "Ask matplotlib to recompute spacing.",
        "tight_layout / constrained layout adjust the spacing so titles, tick labels and axis labels don't collide.",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 2)
fig.delaxes(axs[1, 1])
print(len(fig.axes))""",
        ["3", "4", "2", "ValueError"], 0,
        "delaxes removes an Axes from the figure.",
        "With 3 plots in a 2x2 grid, removing the unused 4th Axes avoids an empty box. axs still references it, but the figure no longer holds it.",
        topic="subplots", level=3),
    out("""import matplotlib.pyplot as plt
fig, axd = plt.subplot_mosaic([["loss", "loss"], ["acc", "lr"]])
print(sorted(axd), len(fig.axes))""",
        ["['acc', 'loss', 'lr'] 3", "['loss', 'loss', 'acc', 'lr'] 4", "['acc', 'loss', 'lr'] 4", "TypeError"], 0,
        "Repeated names in the mosaic make one Axes that spans those cells.",
        "subplot_mosaic returns a dict name -> Axes. 'loss' spans the whole top row, so there are 3 Axes, not 4.",
        diagram="""
+---------------+
|     loss      |
+-------+-------+
|  acc  |  lr   |
+-------+-------+""",
        topic="subplots", level=4),

    # ------------------------------------------------------------------ pandas-plot
    out("""import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame({"train": [1.0, 0.6, 0.4], "val": [1.1, 0.8, 0.7]})
ax = df.plot()
print(type(ax).__name__, len(ax.lines))""",
        ["Axes 2", "Figure 2", "Axes 1", "DataFrame 2"], 0,
        "df.plot() draws one line per numeric column and returns the Axes.",
        "DataFrame.plot is a wrapper around matplotlib: it returns the Axes so you can keep customising (ax.set_xlabel...).",
        analogy='Like a UI component library wrapping raw DOM calls: quick defaults, and you can still reach the underlying element.',
        topic="pandas-plot", level=1),
    out("""import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame({"loss": [3, 2, 1]}, index=pd.Index([1, 2, 3], name="epoch"))
ax = df.plot()
print(ax.get_xlabel(), [t.get_text() for t in ax.get_legend().get_texts()])""",
        ["epoch ['loss']", "'' ['loss']", "index []", "epoch []"], 0,
        "pandas uses the index for x and the column names for the legend.",
        "The index becomes the x axis and its name becomes the x label; each column becomes a labelled line with an automatic legend.",
        topic="pandas-plot", level=2),
    out("""import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
axs = df.plot(subplots=True)
print(type(axs).__name__, axs.shape)""",
        ["ndarray (2,)", "Axes ()", "list (2,)", "ndarray (1, 2)"], 0,
        "subplots=True gives one Axes per column.",
        "With subplots=True pandas creates one Axes per column, stacked vertically, and returns them as a NumPy array.",
        topic="pandas-plot", level=3),
    out("""import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})
ax = df.plot.bar()
print(len(ax.patches))""",
        ["6", "3", "2", "1"], 0,
        "Grouped bars: one bar per (row, column).",
        "plot.bar draws one group per row (3) with one bar per column (2): 6 rectangles.",
        topic="pandas-plot", level=2),
    out("""import matplotlib.pyplot as plt
import pandas as pd
s = pd.Series([1, 2, 2, 3, 3, 3])
ax = s.plot(kind="hist")
print(ax.get_ylabel())""",
        ["Frequency", "count", "", "y"], 0,
        "pandas fills in a default y label for histograms.",
        "Series.plot(kind='hist') (same as s.plot.hist()) labels the y axis 'Frequency'.",
        topic="pandas-plot", level=2),
    out("""import matplotlib.pyplot as plt
import pandas as pd
fig, axs = plt.subplots(1, 2)
s = pd.Series([3, 1, 2])
s.plot(ax=axs[1])
print(len(axs[0].lines), len(axs[1].lines))""",
        ["0 1", "1 0", "1 1", "0 0"], 0,
        "ax= tells pandas where to draw.",
        "Passing ax= makes pandas draw on that existing Axes instead of the current one, which is how you put pandas plots into a subplot grid.",
        topic="pandas-plot", level=2),
    out("""import matplotlib.pyplot as plt
import pandas as pd
s = pd.Series(["cat", "dog", "cat", "cat"])
ax = s.value_counts().plot.bar()
print([t.get_text() for t in ax.get_xticklabels()], [float(p.get_height()) for p in ax.patches])""",
        ["['cat', 'dog'] [3.0, 1.0]", "['dog', 'cat'] [1.0, 3.0]", "['0', '1'] [3.0, 1.0]", "['cat', 'dog', 'cat', 'cat'] [1.0, 1.0, 1.0, 1.0]"], 0,
        "value_counts sorts by count, then the bar chart keeps that order.",
        "value_counts gives cat 3, dog 1 (descending); plot.bar uses the index as tick labels. This is the quickest class-balance chart.",
        topic="pandas-plot", level=3),
    mcq("You call `df.plot()` on a DataFrame with columns name (text), age and salary. What happens to `name`?",
        ["It is skipped: only numeric columns are plotted",
         "It is plotted as zeros",
         "It raises TypeError",
         "It is used as the x axis automatically"], 0,
        "What is the y value of 'Ann'?",
        "pandas plots numeric columns only. To put names on the x axis use df.plot(x='name', y='salary', kind='bar') or set_index('name') first.",
        topic="pandas-plot", level=3),
    out("""import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame({"g": ["a", "b", "a"], "v": [1, 5, 3]})
ax = df.groupby("g")["v"].mean().plot.bar()
print([float(p.get_height()) for p in ax.patches])""",
        ["[2.0, 5.0]", "[1.0, 5.0, 3.0]", "[4.0, 5.0]", "[5.0, 2.0]"], 0,
        "Aggregate first, then plot the small result.",
        "groupby().mean() gives a: 2.0, b: 5.0, and bar plots one bar per group in index order.",
        topic="pandas-plot", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
idx = pd.date_range("2024-01-01", periods=4, freq="D")
s = pd.Series([1, 3, 2, 4], index=idx)
ax = s.rolling(2).mean().plot()
y = ax.lines[0].get_ydata()
print(type(y).__name__, len(y), int(np.ma.count_masked(y)))""",
        ["MaskedArray 4 1", "ndarray 3 0", "ndarray 4 0", "MaskedArray 3 0"], 0,
        "The NaN point is neither dropped nor set to zero.",
        "rolling(2).mean() has NaN in the first slot. pandas hands matplotlib a masked array: all 4 points are kept, the NaN one is masked, and the line simply has a gap there.",
        topic="pandas-plot", level=4),

    # ------------------------------------------------------------------ training-curves
    mcq("You plot training loss and validation loss per epoch. Training loss keeps falling, but validation loss starts RISING after epoch 10. What does that mean?",
        ["Overfitting: the model is memorising the training data and getting worse on unseen data",
         "Underfitting: the model is too simple",
         "The learning rate is zero",
         "Everything is fine: lower training loss is all that matters"], 0,
        "Which curve reflects performance on data the model hasn't seen?",
        "A widening gap with validation going up is the textbook overfitting picture. Stop around the validation minimum (early stopping), add regularisation, or get more data.",
        diagram="""
loss
 |\\
 | \\      val  __/
 |  \\____/
 |   \\
 |    \\____ train
 +--------------------> epoch
          ^ best epoch""",
        analogy="Like code that passes the hard-coded tests it was tuned on but fails on new inputs.",
        topic="training-curves", level=1),
    mcq("Both training and validation loss are high and flat, close to each other. What's the most likely diagnosis?",
        ["Underfitting: the model is too simple or not trained enough",
         "Overfitting",
         "Data leakage",
         "Perfect model"], 0,
        "Bad everywhere, with no gap.",
        "High loss on both sets with little gap means the model can't capture the pattern. Try a bigger model, better features, more epochs or a higher learning rate.",
        diagram="""
loss
 |---___________ val
 |---___________ train   (both high, tiny gap)
 +---------------------> epoch""",
        topic="training-curves", level=1),
    out("""import matplotlib.pyplot as plt
train = [1.0, 0.7, 0.5, 0.4, 0.3]
val = [1.1, 0.8, 0.7, 0.75, 0.9]
fig, ax = plt.subplots()
ax.plot(range(1, 6), train, label="train")
ax.plot(range(1, 6), val, label="val")
best = val.index(min(val)) + 1
print(best, len(ax.lines))""",
        ["3 2", "5 2", "2 2", "3 1"], 0,
        "Find the epoch with the lowest VALIDATION loss.",
        "val is lowest (0.7) at index 2, i.e. epoch 3 with epochs numbered from 1. After that it rises: early stopping would keep the epoch-3 weights.",
        topic="training-curves", level=2),
    mcq("Your training-loss curve jumps up and down wildly from batch to batch and never settles. What is the most likely cause?",
        ["The learning rate is too high", "The learning rate is too low", "Too many epochs", "The validation set is too large"], 0,
        "Steps that are too big overshoot the minimum.",
        "With too large a learning rate, each update overshoots, so loss oscillates or explodes. Lower it, or use a schedule/warm-up. Some batch-to-batch noise is normal; smoothing (a rolling mean) helps you see the trend.",
        topic="training-curves", level=2),
    mcq("The training loss is going down extremely slowly, almost a straight gentle slope after 100 epochs. Most likely?",
        ["The learning rate is too low", "The learning rate is too high", "The model is overfitting", "The data has leaked"], 0,
        "Tiny steps = slow progress.",
        "A very low learning rate makes each update tiny, so loss decreases slowly but steadily. Try a larger rate or a learning-rate finder.",
        topic="training-curves", level=2),
    tf("If validation accuracy is HIGHER than training accuracy early in training, something must be broken.", False,
        "Think about dropout and when the training metric is measured.",
        "It can happen legitimately: dropout/augmentation make training harder, and training metrics are averaged over the epoch while the model is still improving. Check for leakage only if it persists or is extreme.",
        topic="training-curves", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
loss = np.array([5.0, 1.0, 0.1, 0.01, 0.001])
fig, ax = plt.subplots()
ax.plot(loss)
ax.set_yscale("log")
print(ax.get_yscale(), int(np.log10(loss[0] / loss[-1]).round()))""",
        ["log 4", "linear 4", "log 3", "log 5000"], 0,
        "Each step down on a log axis is a factor of 10.",
        "On a log y axis, loss falling from 5 to 0.001 spans about 4 orders of magnitude (5000x), so late progress stays visible instead of hugging zero.",
        topic="training-curves", level=3),
    out("""import pandas as pd
loss = pd.Series([1.0, 0.2, 0.9, 0.1, 0.8, 0.0])
print(loss.rolling(2).mean().round(2).tolist()[1:])""",
        ["[0.6, 0.55, 0.5, 0.45, 0.4]", "[0.2, 0.9, 0.1, 0.8, 0.0]", "[1.2, 1.1, 1.0, 0.9, 0.8]", "[0.6, 0.6, 0.5, 0.5, 0.4]"], 0,
        "Average each value with the previous one.",
        "A rolling mean smooths noisy batch losses: (1+0.2)/2 = 0.6, (0.2+0.9)/2 = 0.55, ... revealing the steady downward trend hidden by the zig-zag.",
        topic="training-curves", level=3),
    mcq("You plot validation loss for 3 learning rates on one chart, but one run's loss starts at 50 while the others are around 1, so the small differences are invisible. What's the best fix?",
        ["Use a log scale on the y axis (or set_ylim to the interesting range)",
         "Remove the legend",
         "Plot as a pie chart",
         "Use a bar chart of the final values only"], 0,
        "One curve is squashing the others.",
        "A log y axis turns multiplicative differences into equal distances, so curves at very different scales are readable together.",
        analogy='Like plotting latency percentiles p50/p99/p99.9: a log axis keeps the 2 ms and the 2 s values readable together.',
        topic="training-curves", level=3),
    mcq("A loss curve shows training loss dropping to near 0 and validation loss also dropping to near 0, both suspiciously fast in the first epoch on a hard task. What should you suspect first?",
        ["Data leakage: test/validation rows (or the label) are present in the features or the training set",
         "The model is underfitting",
         "The learning rate is too low",
         "The plot uses a log scale"], 0,
        "Too good to be true on a hard problem.",
        "Near-perfect validation scores immediately usually mean the model can see the answer: duplicated rows across splits, a target-derived feature, or preprocessing fitted on all data.",
        topic="training-curves", level=4),
    out("""import numpy as np
train = np.array([0.9, 0.6, 0.4, 0.3, 0.25, 0.2])
val = np.array([1.0, 0.7, 0.55, 0.5, 0.52, 0.6])
patience, best, wait = 1, np.inf, 0
for epoch, v in enumerate(val, start=1):
    if v < best:
        best, wait = v, 0
    else:
        wait += 1
        if wait > patience:
            break
print(epoch, best)""",
        ["6 0.5", "4 0.5", "5 0.5", "6 0.6"], 0,
        "With patience 1, training stops after the second epoch in a row without improvement.",
        "val improves until epoch 4 (0.5). Epoch 5 (0.52) is the first miss (wait=1), epoch 6 (0.6) the second (wait=2 > 1), so the loop stops at epoch 6 and the best value is 0.5.",
        topic="training-curves", level=4),
    mcq("A learning curve plots score vs TRAINING SET SIZE (not epochs). Train score stays high, validation score rises and is still climbing at the largest size. What does it suggest?",
        ["High variance: more data would likely still help",
         "High bias: more data won't help",
         "The model has converged; stop collecting data",
         "The validation set is leaking"], 0,
        "The gap is closing but not closed.",
        "A large but shrinking gap with validation still rising means the model benefits from more data (variance-limited). If both curves had plateaued low and close, more data wouldn't help (bias-limited).",
        diagram="""
score
 |  train --------------
 |                 __/  val (still rising)
 |           ___/
 |      __/
 +----------------------> training set size""",
        topic="training-curves", level=4),

    # ------------------------------------------------------------------ heatmaps
    out("""import matplotlib.pyplot as plt
import numpy as np
cm = np.array([[50, 2], [5, 43]])
fig, ax = plt.subplots()
im = ax.imshow(cm, cmap="Blues")
fig.colorbar(im)
print(len(ax.images), len(fig.axes))""",
        ["1 2", "1 1", "4 2", "0 2"], 0,
        "imshow adds an image; colorbar adds a new small Axes.",
        "imshow draws the matrix as one AxesImage. fig.colorbar creates a separate Axes for the colour scale, so the figure now has 2 Axes.",
        topic="heatmaps", level=2),
    mcq("In a confusion-matrix heatmap with true labels on rows and predicted labels on columns, what do the diagonal cells show?",
        ["Correct predictions (predicted class = true class)",
         "All the errors",
         "The total number of samples",
         "The probabilities of each class"], 0,
        "Row i, column i.",
        "Cell (i, j) counts samples of true class i predicted as j. The diagonal (i = j) is correct; off-diagonal cells are the mistakes, and which cell tells you which classes are confused.",
        analogy='Like a bug-triage table: rows are the real bug type, columns are what the reporter filed it as.',
        diagram="""
              predicted
              cat   dog
true  cat  [  50     2 ]   <- 2 cats called dogs
      dog  [   5    43 ]   <- 5 dogs called cats
diagonal (50, 43) = correct""",
        topic="heatmaps", level=1),
    out("""import numpy as np
cm = np.array([[50, 2], [5, 43]])
print(np.trace(cm) / cm.sum(), cm[1, 1] / cm[:, 1].sum())""",
        ["0.93 0.9555555555555556", "0.93 0.8958333333333334", "0.5 0.9555555555555556", "93 43"], 0,
        "Accuracy = diagonal / total. Precision for class 1 = correct 1s / everything predicted as 1 (a column).",
        "Accuracy is (50 + 43) / 100 = 0.93. Precision for class 1 divides the diagonal cell by its COLUMN sum (2 + 43 = 45): 43/45. Dividing by the row (48) would give recall instead.",
        topic="heatmaps", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
im = ax.imshow(np.array([[5, 1], [2, 8]]))
print(im.get_clim(), im.get_array().shape)""",
        ["(1, 8) (2, 2)", "(0, 8) (2, 2)", "(1, 8) (4,)", "(0.0, 1.0) (2, 2)"], 0,
        "By default the colour scale spans the data's min to max.",
        "imshow autoscales the colour limits (clim) to the min and max of the data (1 and 8). For comparing several heatmaps, fix vmin/vmax so the same colour means the same value.",
        topic="heatmaps", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
cm = np.array([[50, 2], [5, 43]])
fig, ax = plt.subplots()
ax.imshow(cm, cmap="Blues")
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha="center", va="center")
ax.set_xticks([0, 1], labels=["cat", "dog"])
print(len(ax.texts), [t.get_text() for t in ax.get_xticklabels()])""",
        ["4 ['cat', 'dog']", "2 ['0', '1']", "4 ['0', '1']", "1 ['cat', 'dog']"], 0,
        "One text per cell; tick labels replace the numbers.",
        "The loop writes the count into each of the 4 cells (note text(x=j, y=i): column first). set_xticks with labels names the predicted classes.",
        topic="heatmaps", level=2),
    tf("In `ax.imshow(matrix)`, row 0 of the matrix is drawn at the TOP of the image by default.", True,
        "Images are drawn like pictures, not like graphs.",
        "imshow uses origin='upper': row 0 is at the top, like a picture or a printed matrix. That's why confusion matrices read naturally. Pass origin='lower' for graph-style orientation.",
        topic="heatmaps", level=2),
    mcq("Your classes are imbalanced (900 'ok', 100 'fraud'). Why is a row-normalised confusion matrix (each row sums to 1) often more useful than raw counts?",
        ["It shows the recall per class, so the small fraud class isn't visually drowned by the big class",
         "It makes the matrix symmetric",
         "It removes false positives",
         "Raw counts are not allowed in heatmaps"], 0,
        "With raw counts, the 'ok' row dominates the colour scale.",
        "Normalising each row by its total turns cells into rates: the diagonal becomes per-class recall. With raw counts, a 50/100 fraud recall looks pale next to 890/900.",
        topic="heatmaps", level=3),
    mcq("You show a correlation matrix (values from -1 to 1) with the default 'viridis' colormap. What's the better choice and why?",
        ["A diverging colormap like 'coolwarm' with vmin=-1, vmax=1, so 0 is neutral and signs are distinct colours",
         "'Blues', because correlations are always positive",
         "A rainbow 'jet' colormap for more contrast",
         "Grayscale, because colour is misleading"], 0,
        "The data has a meaningful centre.",
        "Diverging data (negative vs positive around 0) needs a diverging colormap centred at 0. Sequential maps hide the sign, and 'jet' creates false boundaries and isn't perceptually uniform.",
        topic="heatmaps", level=4),
    out("""import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
ax.imshow(np.zeros((3, 5)))
lo, hi = ax.get_xlim()
b, t = ax.get_ylim()
print(float(lo), float(hi), float(b), float(t))""",
        ["-0.5 4.5 2.5 -0.5", "0.0 5.0 0.0 3.0", "-0.5 2.5 4.5 -0.5", "0.0 4.0 2.0 0.0"], 0,
        "Each cell is centred on an integer coordinate; the y axis is inverted for images.",
        "A 3x5 array has columns 0..4 and rows 0..2, each cell spanning +-0.5. With origin='upper' the y limits run from 2.5 (bottom) to -0.5 (top), i.e. inverted.",
        topic="heatmaps", level=4),

    # ------------------------------------------------------------------ choosing
    mcq("You want to compare total sales across 6 product categories. Which chart?",
        ["Bar chart", "Line chart", "Scatter plot", "Histogram"], 0,
        "Categories, one number each.",
        "A bar chart compares one value per category. A line would imply an order/continuity between categories that doesn't exist.",
        topic="choosing", level=1),
    mcq("You want to see if a feature is skewed and has outliers before scaling it. Which chart?",
        ["Histogram (or box plot) of that feature", "Pie chart", "Line plot of the feature in row order", "Bar chart of the first 10 rows"], 0,
        "You're asking about a distribution.",
        "A histogram shows the shape (skew, multiple peaks); a box plot highlights outliers. Both are standard EDA (exploratory data analysis) checks.",
        topic="choosing", level=1),
    tf("A line chart is a good way to compare average salary across departments (HR, Sales, IT).", False,
        "Is there an order between HR and IT?",
        "Lines suggest a continuous, ordered x axis (like time). For unordered categories, use bars.",
        topic="choosing", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 10, 100, 1000])
ax.set_yscale("log")
print(ax.get_yscale(), ax.get_xscale())""",
        ["log linear", "log log", "linear log", "linear linear"], 0,
        "set_yscale only changes the y axis.",
        "Only the y axis becomes logarithmic; x stays linear. On a log y axis, 1, 10, 100, 1000 are evenly spaced, so this exponential growth looks like a straight line.",
        topic="choosing", level=2),
    mcq("When is a logarithmic y axis the right choice?",
        ["When values span several orders of magnitude, or you care about relative (percentage) change",
         "Whenever the data has negative values",
         "For bar charts of a few categories with similar values",
         "Never; it distorts the data"], 0,
        "Think 1, 10, 100, 1000.",
        "Log scales make multiplicative changes look equal (10 -> 100 same distance as 100 -> 1000). They can't show zero or negative values.",
        topic="choosing", level=2),
    out("""import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")
fig, ax = plt.subplots()
ax.plot([0, 1, 10], [0, 1, 10])
ax.set_yscale("log")
fig.canvas.draw()
print(float(ax.get_ylim()[0]) > 0)""",
        ["True", "False", "ValueError", "ZeroDivisionError"], 0,
        "log(0) is undefined. What does matplotlib do with the 0?",
        "Non-positive values can't be shown on a log axis; matplotlib masks/clips them, and the lower limit stays positive. The 0 point silently disappears, which can mislead readers.",
        topic="choosing", level=3),
    mcq("A bar chart's y axis starts at 95 instead of 0, making a 96 vs 98 difference look huge. What's wrong?",
        ["Bar length encodes the value, so a truncated baseline exaggerates differences; bars should start at 0",
         "Nothing; zooming is always fine",
         "Bars must always use a log scale",
         "The colours are wrong"], 0,
        "Do bars represent length or position?",
        "Readers compare bar lengths, so a non-zero baseline misleads. If small differences matter, use a dot plot or a line chart where a zoomed axis is acceptable.",
        analogy='Like a dashboard that shows 99.1% vs 99.3% uptime as a giant jump: technically true, visually dishonest.',
        topic="choosing", level=3),
    mcq("You need to show the share of each of 3 classes in a dataset in an interview slide. Which is clearest and most accurate?",
        ["A sorted bar chart of class counts (or percentages)",
         "A 3-D pie chart",
         "A scatter plot of class vs count",
         "A line chart of class counts"], 0,
        "People compare lengths better than angles.",
        "Bars are read more accurately than pie slices, especially 3-D pies, which distort area. With only 2-3 classes a simple pie is acceptable, but bars always work.",
        topic="choosing", level=2),
    mcq("A model's precision-recall trade-off across thresholds is best shown as?",
        ["A line (curve) of precision vs recall, one point per threshold",
         "A pie chart of precision and recall",
         "A histogram of thresholds",
         "A bar chart with two bars"], 0,
        "Two numeric variables traced as a third (threshold) changes.",
        "A PR curve plots recall on x and precision on y, connecting the points for successive thresholds; the area under it summarises performance on imbalanced data.",
        topic="choosing", level=3),
    mcq("You have model scores for 2 classes and want to see how well they separate. Which chart reveals overlap best?",
        ["Two overlaid histograms (or density curves) of the score, one per class, with transparency",
         "A pie chart of predicted classes",
         "A line chart of score vs row number",
         "A bar chart of mean score per class"], 0,
        "Means hide overlap.",
        "Overlaid distributions show where the classes overlap, which is where errors happen and where a threshold should go. A bar of means hides the spread entirely.",
        topic="choosing", level=4),

    # ------------------------------------------------------------------ pitfalls
    mcq("What is the difference between the 'pyplot' style (`plt.plot`, `plt.title`) and the object-oriented style (`ax.plot`, `ax.set_title`)?",
        ["pyplot acts on an implicit 'current' figure and axes; the OO style calls methods on explicit Figure/Axes objects",
         "pyplot is for line charts, OO for bar charts",
         "OO style can't save images",
         "They produce different-looking charts"], 0,
        "Implicit global state vs explicit objects.",
        "plt.* functions keep hidden global state (the current figure/axes) like a state machine. The OO style passes objects explicitly, which is clearer with subplots and inside functions.",
        analogy="Global variables vs passing objects as parameters.",
        topic="pitfalls", level=1),
    out("""import matplotlib.pyplot as plt
plt.plot([1, 2])
plt.plot([2, 1])
print(len(plt.gca().lines))
plt.figure()
print(len(plt.gca().lines))""",
        ["2\n0", "1\n1", "2\n2", "1\n0"], 0,
        "pyplot calls go to the current Axes; plt.figure() makes a new current figure.",
        "Both plt.plot calls draw on the same current Axes (2 lines). plt.figure() creates a fresh figure, and gca() gives its new, empty Axes.",
        topic="pitfalls", level=2),
    out("""import matplotlib.pyplot as plt
for i in range(5):
    fig, ax = plt.subplots()
    ax.plot([i])
print(len(plt.get_fignums()))
plt.close("all")
print(len(plt.get_fignums()))""",
        ["5\n0", "1\n0", "5\n5", "0\n0"], 0,
        "pyplot keeps every figure alive until you close it.",
        "Each plt.subplots call registers a new figure with pyplot; none are freed automatically. In a loop that makes hundreds of plots this leaks memory (matplotlib warns after 20). Call plt.close(fig) after saving.",
        analogy='Like opening database connections in a loop and never closing them: the pool fills up.',
        topic="pitfalls", level=2),
    tf("In a script (not a notebook), the plot window appears only when you call `plt.show()`.", True,
        "Scripts don't auto-display figures.",
        "Notebooks render figures at the end of a cell automatically; a plain Python script needs plt.show() (which blocks until the window closes) or fig.savefig() to produce any output.",
        topic="pitfalls", level=1),
    mcq("You call `plt.show()` and THEN `plt.savefig('loss.png')`. The saved file is blank. Why?",
        ["After show() returns, the figure has been closed/released, so savefig writes a new empty current figure",
         "savefig only works with JPEG",
         "show() deletes the PNG",
         "The file name must not contain a dot"], 0,
        "Order matters.",
        "In most interactive backends show() hands figures to the GUI and, when the window closes, pyplot forgets them. Save first (fig.savefig(...)), then show.",
        topic="pitfalls", level=2),
    fill("To save a figure to a file, call `fig.____('loss.png', dpi=150, bbox_inches='tight')`.",
        "savefig",
        "save + fig.",
        "fig.savefig writes the figure; the file extension picks the format (png, pdf, svg). bbox_inches='tight' trims extra whitespace.",
        topic="pitfalls", level=1),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2])
ax.cla()
print(len(ax.lines), len(fig.axes))""",
        ["0 1", "1 1", "0 0", "1 0"], 0,
        "cla clears an Axes; it doesn't remove it.",
        "ax.cla() (clear axes) removes the artists but keeps the Axes in the figure. fig.clf() would remove all Axes.",
        topic="pitfalls", level=3),
    mcq("A function `def plot_loss(hist): plt.plot(hist); plt.title('loss')` is called inside a loop that also draws on a subplot grid. Plots end up on the wrong panels. Best fix?",
        ["Pass the target Axes in: def plot_loss(hist, ax): ax.plot(hist); ax.set_title('loss')",
         "Call plt.show() at the start of the function",
         "Use a bigger figure",
         "Call plt.figure() inside the loop before every plot"], 0,
        "Avoid hidden global state.",
        "pyplot functions draw on whatever Axes is 'current', which changes as other code runs. Accepting an ax parameter (like pandas' ax=) makes the function reusable and predictable.",
        topic="pitfalls", level=3),
    out("""import matplotlib
print(matplotlib.get_backend().lower())""",
        ["agg", "tkagg", "qtagg", "inline"], 0,
        "This quiz runs matplotlib headless (no window).",
        "The Agg backend renders to images in memory without any GUI; it's what servers, CI and tests use (set via matplotlib.use('Agg') or MPLBACKEND). plt.show() does nothing useful there.",
        topic="pitfalls", level=3),
    out("""import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
plt.plot([1, 2, 3])
print(len(ax1.lines), len(ax2.lines))""",
        ["0 1", "1 0", "1 1", "0 0"], 0,
        "Which figure did pyplot make 'current' last?",
        "Every new figure becomes the current one, so plt.plot draws on ax2. Mixing plt.* calls with explicit Axes is how lines end up in the wrong chart.",
        topic="pitfalls", level=2),
    mcq("Why can generating 10,000 plots in a web server request handler with pyplot cause trouble, even with the Agg backend?",
        ["pyplot keeps global state that is not thread-safe and retains figures until closed; use the OO Figure API (matplotlib.figure.Figure) and close or discard figures",
         "Agg can only render 100 images",
         "pyplot sends data to the internet",
         "PNG files can't be created in threads"], 0,
        "Global state + threads + memory.",
        "pyplot's figure manager is a global registry: concurrent requests can draw on each other's 'current' figure, and unclosed figures leak memory. Creating Figure() objects directly avoids the registry entirely.",
        topic="pitfalls", level=4),
    out("""import matplotlib.pyplot as plt
from matplotlib.figure import Figure
fig = Figure()
ax = fig.subplots()
ax.plot([1, 2])
print(len(fig.axes), len(plt.get_fignums()))""",
        ["1 0", "1 1", "0 0", "AttributeError"], 0,
        "A Figure created directly is not registered with pyplot.",
        "matplotlib.figure.Figure() builds a figure outside pyplot's global manager, so plt.get_fignums() doesn't see it and there's nothing to close. This is the recommended pattern for web servers.",
        topic="pitfalls", level=4),
]
