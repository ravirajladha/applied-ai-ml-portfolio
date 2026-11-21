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
    ("scales-ticks", "Twin axes, log/symlog scales, ticks and formatters"),
    ("color-images", "Colormaps, norms and image arrays"),
    ("ml-plots", "ML evaluation plots: ROC/PR, confusion, calibration, residuals, embeddings"),
    ("reading-charts", "Reading and critiquing charts"),
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
    # ================================================================== round 2
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 1, squeeze=False)
print(axs.shape, type(axs[0, 0]).__name__)""",
        ["(1, 1) Axes", "() Axes", "(1,) Axes", "(1, 1) ndarray"], 0,
        "squeeze=False turns off the shape-shrinking.",
        "With squeeze=False, subplots always returns a 2-D array, even for a 1x1 grid. Use it in helper functions that take nrows/ncols as arguments, so the same axs[r, c] indexing works for every grid size. With the default squeeze=True, a 1x1 grid returns a bare Axes, not an array.",
        topic="subplots", level=2),
    out("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 3)
print(axs.flat[4] is axs[1, 1], axs.T.shape, len(axs))""",
        ["True (3, 2) 2", "False (3, 2) 6", "True (2, 3) 6", "False (2, 3) 2"], 0,
        "axs is an ordinary NumPy object array in row-major order.",
        "flat walks the grid row by row, so index 4 is row 1, column 1. axs.T is the transposed view (3, 2), handy when you want to loop over columns. len() of a 2-D array counts rows (2), not Axes. That is why a `for ax in axs` loop over a 2-D grid gives you rows of Axes, and calling ax.plot on one fails.",
        topic="subplots", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
line, = ax.plot([1, 2])
print(line.axes is ax, line.figure is fig, ax.figure is fig, plt.gca() is ax)""",
        ["True True True True", "True False True True", "False False True True", "True True True False"], 0,
        "Every Artist keeps a reference to its parents.",
        "The Artist tree links both ways: a Figure holds Axes and an Axes holds lines, and each child points back with .axes and .figure. So a helper that only receives a Line2D can still reach its Axes and Figure. plt.subplots also makes the new Axes current, so gca() returns it.",
        analogy="Like DOM nodes: a child element knows its parentNode, so you can walk up from any element to the document.",
        topic="fig-axes", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.plot([0, 10], [0, 1])
print(tuple(float(v) for v in ax.get_xlim()))""",
        ["(0.0, 5.0)", "(-0.5, 10.5)", "(0.0, 10.0)", "(0.0, 5.0, 10.0)"], 0,
        "Setting limits by hand changes the Axes' autoscale setting.",
        "set_xlim turns x autoscaling off, so data you plot afterwards does NOT widen the view. Half of this line is clipped off the chart. Real-world case: a plotting helper sets limits for the first run, and later runs that go further are silently cut off. Call ax.autoscale() (or set the limits last) if you want the view to fit all the data.",
        topic="fig-axes", level=4),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
line, = ax.plot([0, 1, 2], [0, 1, 2])
line.set_ydata([0, 10, 20])
a = tuple(round(float(v), 1) for v in ax.get_ylim())
ax.relim(); ax.autoscale_view()
b = tuple(round(float(v), 1) for v in ax.get_ylim())
print(a, b)""",
        ["(-0.1, 2.1) (-1.0, 21.0)", "(-1.0, 21.0) (-1.0, 21.0)", "(-0.1, 2.1) (-0.1, 2.1)", "(0.0, 20.0) (-1.0, 21.0)"], 0,
        "Changing a line's data does not recompute the data limits.",
        "set_ydata only swaps the numbers inside the Line2D. The Axes keeps its cached data limits until you call relim() and then autoscale_view(). A live training-loss plot that updates a line in place will draw the new points off-screen until you do this. Calling plot() again on every step does rescale, but it piles up a new artist each time.",
        analogy="Like mutating an object in place in React state: the data changed, but nothing re-ran the layout until you tell it to.",
        topic="fig-axes", level=4),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax2 = ax.twinx()
plt.ylabel("lr")
print(repr(ax.get_ylabel()), repr(ax2.get_ylabel()))""",
        ["'' 'lr'", "'lr' ''", "'lr' 'lr'", "'' ''"], 0,
        "Which Axes did twinx leave as the 'current' one?",
        "twinx creates a new Axes and makes it current, so the pyplot call plt.ylabel labels the right-hand (twin) axis, not the original. This is a classic mixed-style bug: the OO code builds the axes, and a later plt.* call goes to whichever Axes was touched last. Call ax.set_ylabel / ax2.set_ylabel explicitly.",
        topic="fig-axes", level=4),
    out("""import matplotlib.pyplot as plt
for i in range(3):
    plt.figure()
plt.close()
print(plt.get_fignums())""",
        ["[1, 2]", "[]", "[2, 3]", "[1, 2, 3]"], 0,
        "With no argument, plt.close closes only one figure.",
        "plt.close() closes the CURRENT figure, which is the most recently created one (number 3). Figures 1 and 2 stay open. In loops, call plt.close(fig) on the exact figure you made, or plt.close('all') at the end.",
        topic="pitfalls", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2])
fig.clf()
print(len(fig.axes), len(plt.get_fignums()))""",
        ["0 1", "0 0", "1 1", "1 0"], 0,
        "Clearing a figure is not the same as closing it.",
        "fig.clf() removes all Axes and artists, but the figure is still registered with pyplot. A loop that calls clf() instead of plt.close(fig) still adds one figure per iteration to pyplot's list. Use clf() to reuse one figure on purpose, and close() to free it.",
        topic="pitfalls", level=3),
    mcq("A plotting script works on your laptop but crashes on a Linux CI runner (no screen) with a 'no display' or Tcl error as soon as `plt.subplots()` runs. What's the fix?",
        ["Use the non-GUI Agg backend: set MPLBACKEND=Agg in the environment, or call matplotlib.use('Agg') before importing pyplot, and save with fig.savefig",
         "Install a bigger font cache",
         "Call plt.show(block=False)",
         "Replace PNG output with JPEG"], 0,
        "The script is trying to open a window on a machine that has no screen.",
        "A GUI backend (TkAgg, QtAgg) needs a display server. Agg renders to an in-memory image, which is all you need for savefig. Setting the environment variable is the cleanest option because the code doesn't change. plt.show() does nothing under Agg, so the script must save its figures.",
        analogy="Like running a browser test on a CI box: you switch to headless Chrome because there's no screen.",
        topic="pitfalls", level=3),
    tf("In a loop that makes 1,000 plots with `fig, ax = plt.subplots()`, calling `fig.clf()` at the end of each iteration keeps pyplot's figure count from growing.", False,
        "clf empties the figure. Does pyplot forget the figure?",
        "pyplot keeps a global registry of every figure it created until plt.close is called. clf frees the artists but leaves the Figure, its canvas and its manager registered. After 20 figures you get the 'More than 20 figures have been opened' RuntimeWarning, and memory still grows. Use plt.close(fig), or build matplotlib.figure.Figure objects directly so pyplot never tracks them.",
        topic="pitfalls", level=4),
    # ------------------------------------------------------------------ scales-ticks
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.plot([1, 2], [1, 2], label="loss")
ax2.plot([1, 2], [100, 200], label="lr")
print(ax.get_xlim() == ax2.get_xlim(), ax.get_ylim() == ax2.get_ylim())
print(len(ax.legend().get_texts()))""",
        ["True False\n1", "True True\n2", "False False\n1", "True False\n2"], 0,
        "A twin shares one axis and nothing else, including the legend.",
        "twinx shares the x axis and gives the new Axes its own y scale (here 1-2 on the left, 100-200 on the right). Each Axes has its own legend, so ax.legend() only sees 'loss'. To get one legend, collect handles from both: h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2).",
        diagram="""
 loss                          lr
 2 |              ___/ ...  | 200
   |        ___/  ...       |
 1 |__/ ...                 | 100
   +------------------------+
          shared x (step)""",
        topic="scales-ticks", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([-1000, -1, 0, 1, 1000])
ax.set_yscale("symlog", linthresh=1)
fig.canvas.draw()
print(ax.get_yscale(), ax.get_ylim()[0] < 0)""",
        ["symlog True", "log False", "symlog False", "ValueError"], 0,
        "symlog = symmetric log: linear near zero, logarithmic further out.",
        "A plain log axis cannot show zero or negative values. symlog is linear inside (-linthresh, linthresh) and logarithmic outside, on both sides. That suits signed data that spans orders of magnitude, like gradient values, profit/loss or reward. The cost is a kink at the threshold, so say so in the caption.",
        topic="scales-ticks", level=3),
    fill("`ax.set_yscale('symlog', ____=1e-3)` sets the size of the linear region around zero.",
        "linthresh",
        "linear + threshold.",
        "linthresh is the half-width of the linear band around 0. Pick it close to the smallest magnitude you care about. If it is too large, everything sits in the linear band and you lose the log view. If it is too small, the band around zero gets squeezed into a sliver.",
        topic="scales-ticks", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 1000])
ax.set_yscale("log")
y = ax.transData.transform([(0, 1), (0, 10), (0, 100)])[:, 1]
print(round(float(y[1] - y[0]), 3) == round(float(y[2] - y[1]), 3))""",
        ["True", "False", "ValueError", "None"], 0,
        "transData maps data coordinates to pixels. Compare the 1->10 and 10->100 gaps.",
        "On a log axis every factor of 10 (a decade) gets the same number of pixels, so going from 1 to 10 looks as big as going from 10 to 100. That is why a loss falling from 1.0 to 0.1 and from 0.01 to 0.001 look like equally large improvements on a log plot.",
        topic="scales-ticks", level=3),
    tf("On a log y axis, the vertical gap between loss 0.02 and 0.01 is the same as the gap between 2.0 and 1.0.", True,
        "Log axes show ratios.",
        "Both pairs differ by a factor of 2, so both gaps are log10(2) decades. That is great for seeing late-training progress, but it can mislead: an absolute change of 0.01 looks as big as a change of 1.0. When you report 'run B is much better' from a log plot, check the absolute numbers too.",
        topic="scales-ticks", level=4),
    out("""from matplotlib.ticker import FuncFormatter
f = FuncFormatter(lambda x, pos: f"{x / 1000:.0f}k")
print(f(2500), f(3500), f(1000))""",
        ["2k 4k 1k", "3k 4k 1k", "2k 3k 1k", "2.5k 3.5k 1k"], 0,
        "Python's format rounds halves to the nearest even digit.",
        "':.0f' uses round-half-to-even: 2.5 -> '2' and 3.5 -> '4'. A tick formatter that drops decimals can label two different ticks with the same text, or label 2,500 as '2k'. Formatters run on every tick value, so use '.1f' or a smarter rule when the ticks are not whole thousands.",
        topic="scales-ticks", level=4),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0.9, 0.5, 0.3])
fig.canvas.draw()
print(ax.get_xticks().tolist())""",
        ["[-0.25, 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25]", "[0, 1, 2]", "[0.0, 1.0, 2.0]", "[-0.1, 0.0, 1.0, 2.0, 2.1]"], 0,
        "The default locator picks 'nice' numbers, not your data points.",
        "The automatic tick locator divides the view (-0.1 to 2.1) into round steps of 0.25, so a 3-epoch plot shows 'epoch 0.75'. The list also includes ticks just outside the view (-0.25, 2.25), which are not drawn. Fix it with ax.xaxis.set_major_locator(MaxNLocator(integer=True)) or ax.set_xticks(range(n)).",
        topic="scales-ticks", level=3),
    fill("To force whole-number ticks for epochs: `ax.xaxis.set_major_locator(____(integer=True))`.",
        "MaxNLocator",
        "It's a locator from matplotlib.ticker that caps the number of ticks.",
        "MaxNLocator(integer=True) picks at most a handful of nice ticks and only integer ones, so short training runs don't get fractional epoch labels. Locators decide WHERE ticks go; formatters decide what TEXT they show.",
        topic="scales-ticks", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([5, 9])
ax.set_ylim(bottom=0)
print(tuple(round(float(v), 1) for v in ax.get_ylim()))""",
        ["(0.0, 9.2)", "(0.0, 9.0)", "(4.8, 9.2)", "(0.0, 1.0)"], 0,
        "Only one end is fixed; the other keeps its automatic value.",
        "set_ylim(bottom=0) pins the bottom and leaves the top at its autoscaled value (9 plus the 5% margin). This is the quick way to make an accuracy or throughput chart start at zero without guessing the maximum.",
        topic="scales-ticks", level=2),
    mcq("Your dashboard shows a 'locator' and a 'formatter' on the y axis of a latency chart. Which statement is right?",
        ["The locator decides where the ticks go; the formatter turns each tick value into its label text",
         "The locator sets the axis limits; the formatter sets the colour",
         "They are two names for the same object",
         "The formatter decides where the ticks go; the locator picks the font"], 0,
        "One answers 'where', the other answers 'what text'.",
        "Each axis has a major and a minor locator (e.g. MaxNLocator, LogLocator, FixedLocator) and a formatter (ScalarFormatter, PercentFormatter, FuncFormatter). Swapping the formatter to show '12 ms' or '25%' never moves the ticks. Calling set_xticks replaces the locator with a FixedLocator.",
        analogy="Like a chart library's tickValues vs tickFormat options: one picks the positions, the other renders the strings.",
        topic="scales-ticks", level=2),
    # ------------------------------------------------------------------ color-images
    out("""import matplotlib.pyplot as plt
import numpy as np
cmap = plt.get_cmap("viridis")
print(cmap.N, np.round(cmap(0.0), 3).tolist())""",
        ["256 [0.267, 0.005, 0.329, 1.0]", "256 [0.0, 0.0, 0.0, 1.0]", "100 [0.267, 0.005, 0.329]", "256 [0.993, 0.906, 0.144, 1.0]"], 0,
        "A colormap is a lookup table; calling it with a number in [0, 1] returns RGBA.",
        "viridis has 256 entries. cmap(0.0) is its dark purple end as an (R, G, B, A) tuple of floats in [0, 1], and cmap(1.0) is the yellow end. The plotting pipeline is always data -> norm (scales values to 0..1) -> cmap (0..1 -> RGBA).",
        diagram="""
data value --norm--> 0..1 --cmap--> RGBA
   -3.2      vmin/vmax   0.42     (0.13, 0.57, 0.55, 1.0)""",
        topic="color-images", level=3),
    out("""import matplotlib.pyplot as plt
cmap = plt.get_cmap("viridis")
print(cmap(1) == cmap(1.0), cmap(255) == cmap(1.0))""",
        ["False True", "True False", "True True", "False False"], 0,
        "Integers and floats mean different things to a colormap.",
        "A float is a position in [0, 1]. An int is an INDEX into the 256-entry lookup table. So cmap(1) is the second-darkest colour, not the top one, and cmap(255) is the top. A bug in hand-rolled class colours: cmap(label) with integer labels 0, 1, 2 gives three nearly identical dark purples. Use cmap(label / (n - 1)), or a qualitative map like 'tab10'.",
        topic="color-images", level=4),
    out("""import matplotlib.pyplot as plt
import numpy as np
cmap = plt.get_cmap("viridis")
print(tuple(float(v) for v in cmap(np.nan)), cmap(2.0) == cmap(1.0))""",
        ["(0.0, 0.0, 0.0, 0.0) True", "(0.267, 0.005, 0.329, 1.0) True", "(0.0, 0.0, 0.0, 1.0) False", "ValueError"], 0,
        "Colormaps have special 'bad' and 'over' colours.",
        "NaN maps to the 'bad' colour, fully transparent by default, so missing cells in a heatmap show the background, not a colour. Values above 1 use the 'over' colour, which defaults to the top colour, so out-of-range data blends in silently. cmap.with_extremes(bad='grey', over='red') makes both visible, and colorbar(extend='max') shows that values were clipped.",
        topic="color-images", level=4),
    out("""from matplotlib.colors import Normalize, TwoSlopeNorm
n = Normalize(vmin=0, vmax=10)
t = TwoSlopeNorm(vcenter=0, vmin=-1, vmax=4)
print(float(n(5)), float(t(-1)), float(t(0)), float(t(2)))""",
        ["0.5 0.0 0.5 0.75", "0.5 0.0 0.2 0.6", "0.5 0.0 0.5 1.0", "5.0 -1.0 0.0 2.0"], 0,
        "TwoSlopeNorm maps vcenter to 0.5 and scales each side separately.",
        "Normalize is linear: 5 is halfway between 0 and 10. TwoSlopeNorm puts 0 at the colormap middle (the neutral white of 'RdBu' or 'coolwarm'), maps [-1, 0] to [0, 0.5] and [0, 4] to [0.5, 1]. So 2 -> 0.75. With plain Normalize(-1, 4), zero would land at 0.2 and look clearly blue, which suggests a negative value that isn't there.",
        topic="color-images", level=4),
    out("""from matplotlib.colors import LogNorm
n = LogNorm(vmin=1, vmax=1000)
print(round(float(n(10)), 3), round(float(n(100)), 3))""",
        ["0.333 0.667", "0.01 0.1", "0.009 0.099", "0.5 0.75"], 0,
        "Each decade gets an equal share of the colour range.",
        "LogNorm maps log10(value) linearly: 1, 10, 100, 1000 land at 0, 1/3, 2/3, 1. Use it when a heatmap's counts span orders of magnitude (hist2d of a million points, attention scores, word-pair counts). Otherwise one hot cell turns everything else the darkest colour.",
        topic="color-images", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import CenteredNorm
fig, ax = plt.subplots()
im = ax.imshow(np.array([[-0.2, 0.9], [0.1, 0.4]]), cmap="coolwarm", norm=CenteredNorm())
fig.canvas.draw()
print(tuple(round(float(v), 2) for v in im.get_clim()))""",
        ["(-0.9, 0.9)", "(-0.2, 0.9)", "(-1.0, 1.0)", "(0.0, 0.9)"], 0,
        "CenteredNorm keeps the centre (0 by default) in the middle of the colour range.",
        "CenteredNorm makes the range symmetric around 0 using the largest absolute value (0.9), so it becomes [-0.9, 0.9]. Positive and negative values of the same size get colours of the same strength. Without it, autoscaling to [-0.2, 0.9] puts 0 off-centre in a diverging map. That is the usual bug in correlation and weight-difference heatmaps.",
        topic="color-images", level=3),
    mcq("Why do plotting libraries now default to 'viridis' instead of the old rainbow 'jet' colormap?",
        ["viridis is perceptually uniform (equal steps in value look like equal steps in colour) and still readable in greyscale and for colour-blind viewers; jet creates false bands and hides detail in its bright cyan/yellow regions",
         "jet is slower to render",
         "viridis has more colours (jet has only 64)",
         "jet cannot be saved to PNG"], 0,
        "Think about what the eye sees as a 'big change' in each map.",
        "In jet, lightness goes up and down, so the eye sees sharp edges where the data is smooth and misses real changes in the green band. Perceptually uniform maps (viridis, magma, cividis) increase steadily in lightness. For heatmaps of loss landscapes, attention or activations this decides whether the 'structure' you see is real.",
        topic="color-images", level=3),
    fill("Append ____ to a colormap name to reverse it, e.g. `cmap='viridis____'` (same text both times).",
        "_r",
        "Underscore plus one letter.",
        "Every built-in colormap has a reversed twin named with '_r' ('Blues_r', 'RdBu_r'). Use it when the natural reading is flipped. For example, with an error heatmap you may want low = dark and high = light. cmap.reversed() does the same in code.",
        topic="color-images", level=2),
    out("""import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((4, 6, 3), dtype=np.uint8))
print(im.get_array().shape, tuple(float(v) for v in ax.get_xlim()), ax.get_aspect())""",
        ["(4, 6, 3) (-0.5, 5.5) 1.0", "(6, 4, 3) (-0.5, 3.5) 1.0", "(4, 6, 3) (0.0, 6.0) auto", "(3, 4, 6) (-0.5, 5.5) 1.0"], 0,
        "Images are (height, width, channels); width is the x axis.",
        "An RGB image is an H x W x 3 array (rows first). It has 6 columns, so x runs from -0.5 to 5.5 with each pixel centred on an integer. imshow uses aspect='equal' by default (reported as 1.0), so pixels stay square. A uint8 image is read as 0-255, and a float image as 0-1.",
        topic="color-images", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
img = np.zeros((3, 32, 32), dtype=np.float32)
fig, ax = plt.subplots()
ax.imshow(img)""",
        ["TypeError", "ValueError", "IndexError", "(nothing is printed)"], 0,
        "PyTorch stores images as C x H x W. What does imshow expect?",
        "imshow accepts (H, W), (H, W, 3) or (H, W, 4). A channels-first (3, 32, 32) tensor raises TypeError 'Invalid shape (3, 32, 32) for image data'. Convert with img.transpose(1, 2, 0) in NumPy or tensor.permute(1, 2, 0).cpu().numpy() before plotting a batch of training images.",
        diagram="""
PyTorch:     (C, H, W) = (3, 32, 32)
imshow:      (H, W, C) = (32, 32, 3)
fix:         img.transpose(1, 2, 0)""",
        topic="color-images", level=3),
    mcq("You plot a training image straight from the DataLoader after `Normalize(mean, std)`. It shows up as strange, high-contrast colours, and the log says 'Clipping input data to the valid range for imshow with RGB data'. What is going on?",
        ["The normalised floats range roughly from -2 to +2; imshow clips RGB floats to [0, 1], so you must undo the normalisation (x * std + mean) before plotting",
         "imshow needs uint8 images and cannot show floats",
         "The model has corrupted the image",
         "The colormap is wrong; pass cmap='gray'"], 0,
        "What value range does imshow expect for a float RGB image?",
        "For RGB(A) arrays there is no colormap or norm. Floats must lie in [0, 1] (ints in [0, 255]). Anything outside is clipped, so negatives become black and values above 1 become full colour. Denormalise, then clip to [0, 1]. Passing cmap or vmin does nothing for 3-channel data. This is the usual 'my augmentations look broken' false alarm.",
        topic="color-images", level=4),
    tf("For an H x W x 3 RGB array, `imshow` ignores the `cmap` argument.", True,
        "A colormap turns ONE number per pixel into a colour.",
        "A colormap only applies to 2-D (single-channel) data, where each value is mapped through norm and cmap. An RGB array already holds colours, so cmap is ignored. To see one channel (or a grayscale MNIST digit) as grey, pass the 2-D array with cmap='gray'. Otherwise you get viridis purple-yellow digits.",
        topic="color-images", level=3),
    mcq("You `imshow` a spectrogram of shape (64, 2000) and get a thin, unreadable strip. What's the fix?",
        ["Pass aspect='auto' so the pixels stretch to fill the Axes instead of staying square",
         "Transpose it to (2000, 64)",
         "Increase dpi to 600",
         "Use origin='lower'"], 0,
        "By default imshow keeps every pixel square.",
        "imshow defaults to aspect='equal', so 2000 columns by 64 rows becomes a 31:1 strip. aspect='auto' fills the Axes. Add extent=(t0, t1, f0, f1) to label the axes in seconds and Hz instead of pixel indices, and origin='lower' so low frequencies sit at the bottom.",
        topic="color-images", level=2),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
a = ax.scatter([1, 2, 3], [1, 2, 3], c=[0, 5, 10])
b = ax.scatter([1, 2, 3], [1, 2, 3], color="red")
print(a.get_array().tolist(), b.get_array())""",
        ["[0.0, 5.0, 10.0] None", "[0, 5, 10] [1, 0, 0]", "None None", "[0.0, 0.5, 1.0] None"], 0,
        "c= is DATA to colour-map; color= is a fixed colour.",
        "With c= the values are stored on the collection and sent through norm + cmap at draw time, so you can add a colorbar. color='red' sets the face colour directly, so there is no array to map. Use c for 'colour by predicted probability' and color for 'all class-0 points are blue'.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
sc = ax.scatter([1, 2, 3], [4, 5, 6], c=(1, 0, 0))
fig.canvas.draw()
print(sc.get_array().tolist(), len({tuple(r) for r in sc.get_facecolors().round(3).tolist()}))""",
        ["[1.0, 0.0, 0.0] 2", "None 1", "[1.0, 0.0, 0.0] 1", "ValueError"], 0,
        "There are exactly 3 points, and the tuple also has 3 numbers.",
        "When len(c) equals the number of points, matplotlib reads c as three data values, not one RGB colour. The points come out yellow, purple, purple (2 distinct colours), not red. With 4 points the same tuple would mean 'red'. This shape-dependent behaviour is why the docs say: for a single colour, always use color=.",
        topic="plot-types", level=4),
    tf("In `ax.scatter(x, y, s=...)`, `s` is the marker AREA in points squared, so doubling `s` makes each dot about 1.41x wider, not 2x.", True,
        "Is s a radius or an area?",
        "s is in points^2, so the diameter grows with sqrt(s). If you map a quantity (e.g. sample count) to s, the dot AREA is proportional to it, which is the honest choice for bubble charts. Mapping it to radius would make large values look much bigger than they are.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(0)
x, y = rng.normal(size=(2, 1000))
fig, ax = plt.subplots()
counts, xe, ye, im = ax.hist2d(x, y, bins=(4, 5))
print(counts.shape, len(xe), int(counts.sum()))""",
        ["(4, 5) 5 1000", "(5, 4) 5 1000", "(4, 5) 4 1000", "(4, 5) 5 20"], 0,
        "Same rule as a 1-D histogram: k bins have k+1 edges, along each axis.",
        "hist2d returns counts indexed [x_bin, y_bin] (4 x 5), 5 x-edges, 6 y-edges and the image. Every point lands in exactly one cell, so the counts add up to 1000. Note the order: counts[i, j] is x-bin i, which is TRANSPOSED compared with how imshow draws a matrix (rows = y). Pass counts.T if you re-plot it yourself.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(0)
data = rng.normal(0, 0.1, size=500)
fig, ax = plt.subplots()
n, edges, _ = ax.hist(data, bins=20, density=True)
print(round(float((n * np.diff(edges)).sum()), 3), bool(n.max() > 1))""",
        ["1.0 True", "1.0 False", "500.0 True", "20.0 False"], 0,
        "density=True makes the AREA equal 1, not the heights.",
        "With density=True each bar's height is count / (N * bin width), so height x width sums to 1. The bins here are only about 0.03 wide, so heights go well above 1. That is fine for a probability density but surprising if you expected fractions. For 'percent of samples per bin', use weights=np.ones(N) / N instead.",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
n, edges, _ = ax.hist([0, 1, 2, 3] * 5, bins=10)
print([int(c) for c in n])""",
        ["[5, 0, 0, 5, 0, 0, 5, 0, 0, 5]", "[5, 5, 5, 5, 0, 0, 0, 0, 0, 0]", "[2, 2, 2, 2, 2, 2, 2, 2, 2, 2]", "[5, 5, 5, 5]"], 0,
        "10 equal-width bins between 0 and 3 are each 0.3 wide. Where do the integers fall?",
        "Integer data (star ratings, counts, class ids) with more bins than distinct values gives a 'comb' with empty bins in between. It can look like a strange multi-modal distribution. Use one bin per integer (bins=np.arange(-0.5, 4)) or a bar chart of value_counts().",
        diagram="""
count
 5 |#        #        #        #
   |#        #        #        #
 0 +#--+--+--#--+--+--#--+--+--#
   0                           3""",
        topic="plot-types", level=3),
    out("""import matplotlib.pyplot as plt
fig, ax = plt.subplots()
n, edges, _ = ax.hist([0, 1, 2, 3], bins=3)
print([int(c) for c in n], edges.tolist())""",
        ["[1, 1, 2] [0.0, 1.0, 2.0, 3.0]", "[1, 1, 1] [0.0, 1.0, 2.0, 3.0]", "[2, 1, 1] [0.0, 1.0, 2.0, 3.0]", "[1, 1, 1, 1] [0.0, 1.0, 2.0, 3.0]"], 0,
        "Bins are half-open [a, b) except one.",
        "Every bin is [left, right) EXCEPT the last, which is closed [2, 3], so the maximum value is counted. The bins hold {0}, {1} and {2, 3}. On integer data with edges that land on integers, the last bar is often taller than it should be. This trips up hand-rolled bucketing code that assumes half-open bins everywhere.",
        topic="plot-types", level=4),
    # ------------------------------------------------------------------ ml-plots
    out("""from sklearn.metrics import roc_curve
y = [0, 0, 1, 1]
s = [0.1, 0.4, 0.35, 0.8]
fpr, tpr, thr = roc_curve(y, s)
print(fpr.tolist(), tpr.tolist())
print(thr[0])""",
        ["[0.0, 0.0, 0.5, 0.5, 1.0] [0.0, 0.5, 0.5, 1.0, 1.0]\ninf", "[0.0, 0.5, 1.0] [0.5, 1.0, 1.0]\n0.8", "[0.0, 0.0, 0.5, 0.5, 1.0] [0.0, 0.5, 0.5, 1.0, 1.0]\n1.0", "[0.0, 0.5, 0.5, 1.0] [0.5, 0.5, 1.0, 1.0]\ninf"], 0,
        "roc_curve adds a starting point where nothing is predicted positive.",
        "roc_curve returns arrays ready for ax.plot(fpr, tpr). x = false positive rate and y = true positive rate, one point per threshold, starting at (0, 0). In sklearn 1.6 the first threshold is inf, meaning 'predict nothing positive'. So if you colour points by threshold or put thresholds in a table, drop or special-case thr[0]. Add ax.plot([0, 1], [0, 1], '--') as the random-guess line.",
        topic="ml-plots", level=3),
    mcq("You plot a precision-recall curve for a fraud model where 2% of transactions are fraud. Where is the 'random classifier' reference line?",
        ["A horizontal line at precision = 0.02 (the positive rate), not the diagonal used for ROC",
         "The diagonal from (0, 1) to (1, 0)",
         "A horizontal line at precision = 0.5",
         "There is no baseline for PR curves"], 0,
        "A random scorer flags a random subset. What fraction of any random subset is fraud?",
        "A classifier that ignores the input has precision equal to the base rate at every recall, so the PR baseline is y = prevalence. Drawing a diagonal or 0.5 line makes a weak model look far worse or better than chance. It also explains why ROC-AUC can be 0.95 while average precision is 0.3 on imbalanced data: the PR view shows how many false alarms each catch costs.",
        diagram="""
precision
 1 |\\___
   |    \\___  model
   |        \\____
.02|------------------- random = prevalence
   +-------------------> recall""",
        topic="ml-plots", level=4),
    out("""from sklearn.metrics import confusion_matrix
y_true = [0, 0, 0, 0, 1, 1]
y_pred = [0, 0, 0, 1, 1, 0]
print(confusion_matrix(y_true, y_pred, normalize="true").round(2).tolist())
print(confusion_matrix(y_true, y_pred, normalize="pred").round(2).tolist())""",
        ["[[0.75, 0.25], [0.5, 0.5]]\n[[0.75, 0.5], [0.25, 0.5]]", "[[0.75, 0.25], [0.5, 0.5]]\n[[0.75, 0.25], [0.5, 0.5]]", "[[0.75, 0.5], [0.25, 0.5]]\n[[0.75, 0.25], [0.5, 0.5]]", "[[3, 1], [1, 1]]\n[[3, 1], [1, 1]]"], 0,
        "normalize='true' divides by rows (actual); 'pred' divides by columns (predicted).",
        "Raw counts are [[3, 1], [1, 1]]. 'true' makes each ROW sum to 1, so the diagonal is per-class RECALL (0.75, 0.5). 'pred' makes each COLUMN sum to 1, so the diagonal is per-class PRECISION (0.75, 0.5 here). The two heatmaps look alike but answer different questions. Always say in the title which one you plotted.",
        topic="ml-plots", level=4),
    out("""from sklearn.metrics import confusion_matrix
y_true = ["cat", "dog", "dog", "dog"]
y_pred = ["cat", "cat", "dog", "dog"]
print(confusion_matrix(y_true, y_pred).tolist(), confusion_matrix(y_true, y_pred, labels=["dog", "cat"]).tolist())""",
        ["[[1, 0], [1, 2]] [[2, 1], [0, 1]]", "[[1, 1], [0, 2]] [[2, 0], [1, 1]]", "[[1, 0], [1, 2]] [[1, 0], [1, 2]]", "[[2, 1], [0, 1]] [[1, 0], [1, 2]]"], 0,
        "Without labels=, classes come out in sorted order. Rows are the actual class.",
        "Sorted order is cat, dog. Row 'dog' (actual) has 1 predicted cat and 2 predicted dog. labels=['dog', 'cat'] reorders both rows and columns. Your heatmap tick labels must use the SAME list. A common bug is a matrix built in sorted order with tick labels in the model's class order, so every cell is mislabelled while the plot looks fine.",
        topic="ml-plots", level=3),
    mcq("Your plotting script smooths a noisy validation-loss curve with an EMA (exponential moving average, smoothing 0.9, like a training-dashboard slider) and picks the checkpoint at the smoothed curve's minimum. What's the catch?",
        ["An EMA only looks backwards, so it lags: the smoothed minimum appears several epochs AFTER the real one, and you pick an already-overfitting checkpoint",
         "An EMA always makes the minimum lower than it really was",
         "An EMA moves the minimum earlier in time",
         "There is no catch; smoothing never changes where the minimum is"], 0,
        "Each smoothed value is mostly made of older values.",
        "s_t = 0.9 * s_(t-1) + 0.1 * x_t keeps about 10 steps of memory, so turning points show up late. The early start is also biased toward the first value. Smooth to SEE the trend, but choose the checkpoint from the raw (or centred-window) metric. With pandas: val.ewm(alpha=0.3, adjust=False).mean() on [1.0, 0.6, 0.4, 0.35, 0.5, ...] puts the minimum at index 4 instead of 3.",
        diagram="""
loss  raw .   smoothed ---
  |  .
  |   .--__
  |      . --___ . .--
  |        .  ^raw min  ^smoothed min (late)
  +------------------------> epoch""",
        topic="ml-plots", level=4),
    mcq("A reliability (calibration) plot is built with `calibration_curve(y, p, n_bins=2)`, and it returns fraction of positives [0.0, 0.75] at mean predicted probability [0.08, 0.93]. How should you read it?",
        ["The model is over-confident at the top: when it says about 93%, only 75% are actually positive (the point is below the diagonal)",
         "The model is perfectly calibrated because both lists increase",
         "The model is under-confident: it should predict higher probabilities",
         "Calibration plots only make sense for regression"], 0,
        "Compare each x value (predicted) with its y value (actual rate). The diagonal y = x is perfect.",
        "Points below the diagonal mean the predicted probability is higher than the observed frequency, i.e. over-confident. That is typical of boosted trees and of deep nets after long training. Fix it with CalibratedClassifierCV (isotonic or sigmoid) or temperature scaling. A plot with few bins is noisy, so also plot a histogram of p underneath.",
        code="""import numpy as np
from sklearn.calibration import calibration_curve
y = np.array([0, 1, 0, 1, 0, 1, 1, 0, 1, 1])
p = np.array([0.95, 0.95, 0.9, 0.9, 0.05, 0.95, 0.9, 0.1, 0.92, 0.97])
frac_pos, mean_pred = calibration_curve(y, p, n_bins=2)
print(frac_pos.round(2).tolist(), mean_pred.round(2).tolist())""",
        topic="ml-plots", level=4),
    mcq("A t-SNE plot of your sentence embeddings shows cluster A as a big, spread-out blob far from a tight cluster B. What can you safely conclude?",
        ["Very little about size or distance: t-SNE keeps local neighbourhoods but distorts cluster sizes and between-cluster gaps; check with distances in the original space",
         "A has much higher variance than B in the original space",
         "A and B are the most dissimilar classes in the data",
         "The embedding model is broken because the clusters differ in size"], 0,
        "What does t-SNE try to preserve: neighbours or distances?",
        "t-SNE only tries to keep each point's nearest neighbours close. Density gets evened out (dense clusters expand, sparse ones shrink) and global gaps depend on perplexity and the random seed. UMAP has similar caveats. Use the plot to spot neighbourhoods and label noise. For size or similarity claims, compute cosine distances in the embedding space or use PCA, whose axes are linear and show the variance they explain.",
        topic="ml-plots", level=4),
    mcq("You plot residuals (y - prediction) against predicted values for a linear regression model. Which pattern says 'the model is missing a non-linear term'?",
        ["A U-shaped (curved) band: positive at both ends and negative in the middle",
         "A random horizontal cloud around 0",
         "A cloud whose spread widens to the right (a funnel)",
         "Exactly zero residuals everywhere"], 0,
        "A good residual plot looks like noise.",
        "Curvature means the errors depend on x in a way a straight line can't capture: add polynomial or interaction features, or use a non-linear model. A funnel means heteroscedasticity (error grows with the value), so think log-transforming y or using prediction intervals. A random cloud is what you want.",
        diagram="""
resid
 +  .                     .
 0 --- .  .  .  .  .  . ----
 -        .  .  .  .
   +-----------------------> predicted
     U-shape = missing curve""",
        topic="ml-plots", level=3),
    tf("If you log training loss every step (300 points) and validation loss every epoch (3 points) and call `ax.plot(train)` and `ax.plot(val)` on the same Axes, the validation curve ends at x = 2 while training ends at x = 299.", True,
        "With one argument, x is just 0..n-1.",
        "Each plot() call without x uses its own index, so the 3 val points are crammed into the first 1% of the chart and look like a vertical drop. Plot both against a shared unit: ax.plot(steps, train) and ax.plot(epoch_end_steps, val), or convert steps to fractional epochs. It's the same bug as joining two time series on row number instead of timestamp.",
        topic="ml-plots", level=4),
    # ------------------------------------------------------------------ reading-charts
    mcq("What does this training-loss chart most likely show?",
        ["The learning rate is too high: loss drops briefly, then bounces and blows up (often to NaN)",
         "Classic overfitting",
         "The model is underfitting because it is too small",
         "Normal training; loss always rises at the end"], 0,
        "Look at what happens after the first few hundred steps.",
        "A short dip, growing oscillation and then an explosion is what overshooting updates look like. Lower the LR (often by 3-10x), add warmup, or clip gradients. Overfitting looks different: TRAIN loss keeps falling and only validation rises. Here the training loss itself diverges.",
        diagram="""
loss                       NaN ^
 3 |                          |
 2 |\\        /\\   /\\    /\\   /
 1 | \\__/\\__/  \\_/  \\__/  \\_/
   +-----------------------------> step""",
        topic="reading-charts", level=2),
    mcq("A 10-class classifier's training loss sits flat at about 2.30 from the first step to the last. What does the chart tell you?",
        ["The model outputs a near-uniform distribution: 2.30 = ln(10) is the cross-entropy of guessing 1/10 for every class, so it is learning nothing (dead inputs, LR of 0, labels shuffled, or frozen weights)",
         "The model has converged to a good solution",
         "It is overfitting",
         "The loss is in log scale so 2.30 means 10% error"], 0,
        "Compute -ln(1/10).",
        "A flat line at ln(C) is a fingerprint: uniform predictions. The usual causes are no gradient flow (a requires_grad / freeze bug, LR = 0, optimizer built on the wrong parameters), inputs all zero, or labels that don't match the inputs. Knowing the starting loss (ln C for C classes) is a quick sanity check in any training dashboard.",
        diagram="""
loss
2.30 |---------------------------------
     |
     +---------------------------------> step""",
        topic="reading-charts", level=4),
    mcq("A slide shows revenue (left axis) and model accuracy (right axis) on twin y axes, and the two lines cross in March. The presenter says 'accuracy overtook revenue in March'. What's wrong?",
        ["Nothing about the crossing is real: each axis has its own arbitrary scale, so moving either axis's limits moves (or removes) the crossing point",
         "Twin axes always need a log scale",
         "The lines should be bars",
         "Accuracy must be plotted on the left axis"], 0,
        "Change ax2.set_ylim and watch what happens to the crossing.",
        "With twinx the vertical positions of the two series have no common unit, so crossings, 'gaps' and 'parallel trends' are created by whoever picked the limits. Show the series in two stacked panels with sharex=True, or plot both indexed to 100 at a common start date. Twin axes are fine for reading values off, not for comparing the lines.",
        analogy="Like two dashboard widgets with independent auto-scaled y axes placed on top of each other: the overlap pattern is an artefact of the layout.",
        topic="reading-charts", level=4),
    mcq("A blog post compares two optimizers with one training run each and shows a smoothed validation-accuracy chart where B ends 0.3% above A. Which critique is most important?",
        ["One seed per method gives no idea of run-to-run noise, which is often larger than 0.3%; show the mean and a band (min/max or std) over several seeds, and the raw curve alongside the smoothed one",
         "The chart should use a pie chart",
         "Validation accuracy should be plotted on a log scale",
         "The y axis must start at 0% for line charts"], 0,
        "Would a rerun of A with a different seed land in the same place?",
        "Seed noise (data order, init, dropout) easily moves final accuracy by a few tenths of a percent, so a single-run gap of 0.3% proves nothing. Heavy smoothing can also hide instability, like a spike or divergence that one optimizer has. Plot mean +- std with fill_between over 3-5 seeds and keep the raw curve visible. A line chart may zoom its y axis (unlike bars), so that is not the issue.",
        diagram="""
acc
 |        ____----- B (seed 0)
 |   ___--  ~~~~~~ A seeds 0..4 band
 |  /  ~~~~~~
 +---------------------------> epoch""",
        topic="reading-charts", level=4),
    # ---- round 3 pass 5: conceptual mcq/tf/fill
    # ---------------------------------------------------------------- level 1
    mcq("Which of these is a DISTRIBUTION question (best answered with a histogram or box plot)?",
        ["'What range do most users' session lengths fall in, and are there extreme ones?'",
         "'Did daily sign-ups go up or down over the last 6 months?'",
         "'Do users who spend longer per session also buy more?'",
         "'Which of our 5 regions had the most revenue?'"], 0,
        "One variable, and you want to know its spread and shape.",
        "Most chart choices start by naming the question type. A distribution question is about how ONE variable's values spread out: histogram or box plot. "
        "Change over time is a trend (line). Does X move with Y is a relationship (scatter). Which group is biggest is a comparison (bar). "
        "In an interview, saying the question type out loud before picking a chart shows you know why the chart fits.",
        diagram="""
 question            chart
 trend over time  -> line
 compare groups   -> bar
 distribution     -> histogram / box
 relationship     -> scatter""",
        topic="choosing", level=1),
    mcq("On a standard ROC curve, what goes on each axis?",
        ["x: false positive rate (share of negatives wrongly flagged); y: true positive rate (share of positives caught)",
         "x: threshold; y: accuracy",
         "x: recall; y: precision",
         "x: epoch; y: loss"], 0,
        "ROC compares 'caught' against 'false alarms'.",
        "Each point on a ROC (receiver operating characteristic) curve is one threshold: how many real positives you catch (TPR, also called recall) versus how many negatives you wrongly flag (FPR). "
        "Recall on x and precision on y is a different plot, the PR curve. Threshold vs accuracy is a third one. Mixing up ROC and PR axes is a common slip in interviews.",
        topic="ml-plots", level=1),
    mcq("What does `alpha=0.3` do in `ax.scatter(x, y, alpha=0.3)`?",
        ["Makes each marker 30% opaque, so places where many points overlap look darker",
         "Draws only 30% of the points",
         "Shrinks the markers to 30% of their size",
         "Sets the significance level of a statistical test"], 0,
        "alpha is the opacity of the colour.",
        "alpha goes from 0 (invisible) to 1 (solid). With see-through markers, a pile of overlapping points looks darker than a single point, so you can see where the data is dense. "
        "It's the first fix for overplotting, where thousands of solid dots merge into one blob. alpha doesn't drop any data.",
        topic="plot-types", level=1),
    mcq("A heatmap has a colorbar beside it. What does the colorbar tell you?",
        ["Which data value each colour stands for",
         "How many cells the heatmap has",
         "The order in which the cells were drawn",
         "Which colours are safe for printing"], 0,
        "It's the legend for colour.",
        "A colorbar is the key that maps colours back to numbers, like a map's legend. Without one, a reader can't tell whether dark blue means 0.1 or 100. "
        "Check its range too: two heatmaps with different colorbar ranges can't be compared by eye.",
        topic="color-images", level=1),
    mcq("What does the `dpi` setting control when you save a figure as PNG?",
        ["Dots (pixels) per inch: how many pixels each inch of the figure becomes, so higher dpi gives a sharper, larger image",
         "The font size",
         "The number of data points drawn",
         "The colour depth of the image"], 0,
        "dpi = dots per inch.",
        "A figure is sized in inches (figsize). dpi decides how many pixels each inch becomes, so a 6.4 x 4.8 inch figure at dpi=100 is 640 x 480 pixels, and at 300 it is 1920 x 1440. "
        "Use around 150-300 for slides and reports. A low-dpi PNG looks blurry when it gets stretched.",
        topic="pitfalls", level=1),
    tf("On a ROC plot, the diagonal line from (0, 0) to (1, 1) shows what a model guessing at random would score.", True,
        "A random guesser flags positives and negatives at the same rate.",
        "If a model ignores the input and flags, say, 30% of rows at random, it catches 30% of positives AND 30% of negatives, so TPR = FPR: a point on the diagonal. "
        "A useful model's curve bows up towards the top-left corner. A curve below the diagonal means the scores are flipped.",
        diagram="""
 TPR
 1 |   ___-----'
   |  /     .'
   | /    .'   <- random (diagonal)
   |/   .'
 0 +-------------> FPR
   0            1""",
        topic="ml-plots", level=1),
    tf("Like the bars of a category bar chart, the bars of a histogram can be sorted from tallest to shortest.", False,
        "What does the x axis of a histogram stand for?",
        "A histogram's x axis is a number line: each bar is a bin such as 10-20 ms, and the bins must stay in numeric order or the shape of the distribution is lost. "
        "A bar chart of categories (cities, classes) has no natural order, so sorting by height there makes it easier to read.",
        topic="plot-types", level=1),
    tf("If you call `plt.plot([1, 2, 3])` without creating a figure first, pyplot creates a figure and an Axes for you.", True,
        "pyplot keeps track of a 'current' figure.",
        "pyplot works like a state machine: when there's no current figure, plt.plot makes one, adds an Axes and draws on it. "
        "Handy in a quick notebook, but this hidden state is also why plt.* calls sometimes land on the wrong chart in bigger code. "
        "fig, ax = plt.subplots() makes the objects explicit.",
        topic="fig-axes", level=1,
        analogy="Like a global 'current tab' in an editor: commands act on whatever tab happens to be active."),
    fill("To make the y axis logarithmic in the OO style, call `ax.____('log')`.",
        "set_yscale",
        "OO setters start with set_; this one sets the y scale.",
        "ax.set_yscale('log') (and set_xscale for x) changes how the axis maps values to positions: each factor of 10 gets the same space. "
        "It's the standard view for losses that fall over several orders of magnitude.",
        topic="scales-ticks", level=1),
    fill("`fig.savefig('loss.png', ____=300)` saves a high-resolution image (one word, the pixels-per-inch setting).",
        "dpi",
        "Three letters: dots per inch.",
        "dpi sets the pixel density of raster formats like PNG. dpi=300 is print quality. Vector formats (PDF, SVG) mostly ignore it, because lines and text are stored as shapes, not pixels.",
        topic="pitfalls", level=1),
    # ---------------------------------------------------------------- level 2
    mcq("A figure made with the default figsize (6.4 x 4.8 inches) is saved with `fig.savefig('f.png', dpi=200)`. How big is the PNG?",
        ["1280 x 960 pixels", "640 x 480 pixels", "200 x 200 pixels", "6.4 x 4.8 pixels, scaled up by the viewer"], 0,
        "Pixels = inches x dots per inch.",
        "6.4 x 200 = 1280 and 4.8 x 200 = 960. figsize sets the size in inches and dpi turns inches into pixels, so you can make a sharper image without changing the layout. "
        "640 x 480 is what you'd get at the default dpi of 100.",
        topic="pitfalls", level=2),
    mcq("Your loss chart looks sharp in the notebook but blurry when stretched across a slide. What's the best fix?",
        ["Save at a higher dpi (e.g. 200-300), or save as SVG/PDF so lines and text stay sharp at any size",
         "Use a thicker figure border",
         "Call plt.show() before saving",
         "Switch to a log scale"], 0,
        "Blurry means too few pixels for the size it's shown at.",
        "A PNG has a fixed number of pixels; stretching it past that size blurs it. More dpi means more pixels. A vector format stores shapes instead, so it scales cleanly. "
        "Vector files get huge with millions of points, though; for those, use a PNG or rasterise just the dense layer.",
        topic="pitfalls", level=2),
    tf("If a confusion-matrix heatmap of raw counts shows one very dark diagonal cell, the model must be doing well.", False,
        "What if one class has 95% of the rows?",
        "With 950 negatives and 50 positives, a model that predicts 'negative' every time gets a near-black top-left cell, while the positive row is pale and almost all wrong. "
        "Raw counts let the big class dominate the colour scale. Look at the per-row (recall) view, or annotate each cell with its number.",
        diagram="""
            pred 0   pred 1
 true 0  [  950 ##     0   ]   dark, looks great
 true 1  [   50 .      0   ]   every positive missed""",
        topic="heatmaps", level=2),
    mcq("You log loss after every batch instead of once per epoch, and the curve now looks very jagged. What's the most likely reason?",
        ["Each batch is a different small sample, so its loss naturally jumps around; the epoch average hides that noise",
         "The learning rate doubled when you changed the logging",
         "The model is overfitting",
         "matplotlib adds random jitter to long lines"], 0,
        "An epoch average is an average over many batches.",
        "Per-batch loss depends on which examples landed in that batch, so it's noisy even when training is healthy. Averaging over an epoch smooths it. "
        "To read the trend, overlay a rolling mean on the raw curve. Worry when the noise grows over time or the trend goes up, not when the line is merely jagged.",
        topic="training-curves", level=2),
    mcq("You colour points by model name (5 models, no order between them). Which kind of colormap fits?",
        ["A qualitative (categorical) map like 'tab10': distinct hues with no implied order",
         "A sequential map like 'Blues'",
         "A diverging map like 'RdBu'",
         "A rainbow map like 'jet'"], 0,
        "Is 'model C' more than 'model A'?",
        "Sequential maps (light to dark) say 'more vs less'. Diverging maps say 'above vs below a centre'. Categories with no order need hues that are easy to tell apart and imply no ranking. "
        "That's 'tab10', matplotlib's default colour cycle. Using 'Blues' would suggest that the darkest model is the 'biggest' one.",
        diagram="""
 sequential   light ......... dark       amounts
 diverging    blue ... white ... red     +/- around 0
 qualitative  blue orange green red ...  categories""",
        topic="color-images", level=2),
    tf("A line chart's y axis must always start at zero, just like a bar chart's.", False,
        "What does a line encode: length or position?",
        "Bars encode values as lengths, so a cut-off baseline distorts them. A line encodes values as positions, and zooming in to show a change from 0.91 to 0.94 accuracy is normal and honest, as long as the axis is labelled. "
        "The trap is the other way round: a line zoomed so far in that noise looks like a big trend.",
        topic="choosing", level=2),
    mcq("You tried learning rates 1e-5, 1e-4, 1e-3, 1e-2 and 1e-1 and want to plot final loss against learning rate. How should the x axis be set up?",
        ["Log scale (ax.set_xscale('log')), so each factor of 10 gets equal space",
         "Linear scale, so that the true distances are shown",
         "As categories in a pie chart",
         "Sorted by final loss instead of learning rate"], 0,
        "On a linear axis, where would 1e-5, 1e-4 and 1e-3 end up?",
        "On a linear axis running to 0.1, the points for 1e-5, 1e-4 and 1e-3 sit almost on top of each other at the left edge. Hyperparameters searched in powers of 10 are plotted on a log axis. "
        "The loss usually forms a U shape there, with its best region visible. The same goes for weight decay or regularisation strength.",
        topic="scales-ticks", level=2),
    fill("In pyplot, `plt.____()` returns the current Axes (the one plt.plot would draw on).",
        "gca",
        "'get current axes'.",
        "plt.gca() gets the current Axes and plt.gcf() the current Figure. They connect the pyplot state machine to the OO API: "
        "when a library has drawn something with plt.*, ax = plt.gca() gives you the object so you can keep customising it.",
        topic="fig-axes", level=2),
    fill("For 1 million (x, y) points, `ax.____(x, y, gridsize=50)` groups them into hexagonal bins coloured by count.",
        "hexbin",
        "hex + bin.",
        "hexbin draws a 2-D histogram with hexagonal cells, so dense regions show as counts with a colorbar instead of a solid blob. "
        "Hexagons tile the plane with less directional bias than squares. Pass bins='log' when counts vary over orders of magnitude.",
        topic="plot-types", level=2),
    mcq("Your training loss is flat-ish, then suddenly drops at epoch 30 and again at epoch 60, like a staircase. What usually explains this?",
        ["A step learning-rate schedule that cuts the LR (e.g. by 10x) at those epochs",
         "Data leakage that starts at epoch 30",
         "The validation set was reshuffled",
         "matplotlib re-scaled the y axis at those points"], 0,
        "Something changes at exactly fixed epochs.",
        "With a step schedule (e.g. MultiStepLR at milestones 30 and 60), each LR cut lets the optimiser settle deeper into the minimum, so the loss drops suddenly. "
        "Plotting the LR on a panel below, with sharex=True, makes the cause obvious. Cosine schedules give a smooth curve instead.",
        diagram="""
 loss
  |\\____
  |     \\________
  |              \\________
  +-----30-------60--------> epoch
       LR/10    LR/10""",
        topic="training-curves", level=2),
    # ---------------------------------------------------------------- level 3
    mcq("You scatter 2 million points with `alpha=0.05` to fix overplotting. The core of the cloud is still one flat, solid colour. Why?",
        ["Opacity stacks as 1 - (1 - alpha)^n, so after about 100 overlapping points a spot is over 99% opaque and 100 looks the same as 10,000",
         "alpha only works on line plots, not on scatter",
         "matplotlib caps alpha at 0.5",
         "Transparency is lost when the figure is saved"], 0,
        "Work out how opaque a spot is after 100 layers of 5%.",
        "Each marker lets through 95% of what's behind it, so 100 stacked markers let through 0.95^100, about 0.6%: the spot looks solid. Alpha helps in medium-density regions but saturates in the densest ones. "
        "To see real counts, use hexbin / hist2d with a log colour scale, or a KDE plot.",
        diagram="""
 points stacked:   1     10     50    100   1000
 opacity (a=.05): .05   .40    .92   .99   1.00
                                 ^ the eye can't tell these apart""",
        topic="plot-types", level=3),
    tf("Squaring every score (scores in [0, 1]) leaves the ROC curve and ROC AUC exactly the same.", True,
        "ROC only cares about the ORDER of the scores.",
        "Squaring keeps the order of scores in [0, 1], so every threshold splits the rows the same way and each (FPR, TPR) point is unchanged. Any order-preserving transform works the same: log, sigmoid, multiplying by 10. "
        "The flip side: ROC tells you nothing about whether the probabilities are calibrated. For that you need a reliability plot.",
        code="from sklearn.metrics import roc_auc_score\ny = [0, 0, 1, 1, 0, 1]\ns = [0.1, 0.4, 0.35, 0.8, 0.6, 0.9]\nprint(roc_auc_score(y, s), roc_auc_score(y, [v ** 2 for v in s]))",
        topic="ml-plots", level=3),
    tf("A classifier with ROC AUC 0.99 can still be badly calibrated, e.g. saying 0.99 for cases that are positive only 70% of the time.", True,
        "AUC measures ranking. Does ranking say anything about the actual probability values?",
        "AUC only checks that positives get higher scores than negatives. Squash every score towards 0.5, or push them all towards 1, and AUC is unchanged while the probabilities become meaningless. "
        "If the scores drive decisions such as 'flag if risk > 0.8' or expected-cost maths, check a reliability plot, and calibrate if needed (CalibratedClassifierCV, temperature scaling).",
        topic="ml-plots", level=3),
    tf("Saving the same figure with dpi=300 instead of dpi=100 makes the text look smaller relative to the plot.", False,
        "Font sizes are in points, and a point is 1/72 of an inch.",
        "Fonts, line widths and the figure itself are all sized in physical units (points and inches). Raising dpi scales EVERYTHING by the same factor: 3x the pixels, 3x the text height in pixels, same proportions. "
        "To change how big text looks relative to the plot, change figsize or the font size. A large figsize with small fonts is why some saved plots look tiny in papers.",
        topic="pitfalls", level=3),
    mcq("A team's model-error heatmap uses red for 'bad' and green for 'good'. Why is that a problem, and what's a better choice?",
        ["About 1 in 12 men has red-green colour-vision deficiency and can't tell the two apart; use a map that varies in lightness (viridis, cividis) or blue/orange, and print the values in the cells",
         "Red and green can't be printed",
         "matplotlib renders red more slowly than other colours",
         "Heatmaps must always be greyscale"], 0,
        "Think about who might be reading the chart.",
        "The most common colour-vision deficiency mixes up red and green, so 'good' and 'bad' look the same muddy colour to some readers. Maps that change steadily in lightness still read correctly in greyscale and for colour-blind viewers. "
        "Adding the numbers (or a second cue such as hatching) means colour isn't the only thing carrying the information.",
        topic="color-images", level=3),
    tf("Printed in greyscale, the 'jet' rainbow colormap still shows low values as dark and high values as light, in order.", False,
        "Where is jet brightest: at its ends or in the middle?",
        "jet goes dark blue -> cyan -> yellow -> red -> dark red. Its lightness rises to a peak around cyan/yellow and then falls again, so in greyscale the top values come out dark like the bottom ones. "
        "viridis and cividis get steadily lighter from end to end, so their order survives greyscale printing and colour-blind viewers.",
        diagram="""
 lightness along the map (0 = low value, 1 = high)
 jet:      __/~~~~\\__     up, then down again
 viridis:  ______/////     steadily up""",
        topic="color-images", level=3),
    mcq("Request sizes range from 100 bytes to 10 MB, with most under 10 KB. A histogram with 50 linear bins shows one tall bar and nothing else. Best fix?",
        ["Use log-spaced bins (np.logspace) together with ax.set_xscale('log'), so each decade gets its own bins",
         "Use 5000 linear bins",
         "Drop every value above 10 KB",
         "Use a pie chart of the size groups"], 0,
        "Linear bins 200 KB wide put almost everything in bin one.",
        "Heavy-tailed data (sizes, latencies, word counts, income) needs bins that grow with the value. np.logspace(2, 7, 50) puts equal-width bins on a log axis and reveals the shape. "
        "Linear bins on a log axis look odd (the bars get thinner to the right), and many linear bins still squash the small values. Deleting the tail hides the very outliers you want to know about.",
        topic="choosing", level=3),
    fill("To compare three confusion-matrix heatmaps by colour, give every imshow the same colour range: pass the same ____ and vmax.",
        "vmin",
        "The lower end of the colour scale.",
        "By default each imshow stretches its colours from its own min to its own max, so 'dark blue' means a different number in each panel. "
        "Fixing vmin and vmax (or sharing one Normalize object) and drawing a single colorbar makes the panels comparable.",
        topic="heatmaps", level=3),
    mcq("You scatter class 0 (10,000 points, blue) and then class 1 (10,000 points, orange) on one Axes. The overlap region looks all orange. What's going on?",
        ["Artists drawn later sit on top, so orange covers the blue points beneath; shuffle the drawing order, use small markers with alpha, or plot each class in its own panel",
         "matplotlib mixes the two colours into orange",
         "Class 1 really outnumbers class 0 in that region",
         "The legend is hiding the blue points"], 0,
        "Which points are painted last?",
        "In one Axes, artists added later are drawn on top (unless you set zorder). With dense overlap the last class drawn wins, and the chart says 'class 1 dominates here' when it may not. "
        "Plot both classes in one scatter call with rows in random order and a colour array, or use side-by-side panels or density contours. Worth checking in any t-SNE/UMAP plot of labelled points.",
        topic="reading-charts", level=3),
    mcq("Scaling-law charts plot test loss against training compute on log-log axes. Why log-log?",
        ["A power law L = a * C^(-b) becomes a straight line, log L = log a - b log C, so the slope gives the exponent and you can extrapolate along it",
         "Because loss can be negative",
         "Log-log axes make every curve look flat",
         "Compute is always a power of 10"], 0,
        "Take the log of both sides of L = a * C^(-b).",
        "On log-log axes, power laws are straight lines, and the slope is -b. That's why scaling plots are read as 'a straight line on log-log', and bends at the end are spotted as departures from the trend. "
        "On linear axes the same data looks like a curve that has 'flattened out', which hides the steady improvement per 10x of compute. "
        "Only log-log does this: log-linear axes straighten exponentials, not power laws.",
        diagram="""
 log L
  |\\
  |  \\         straight line on log-log
  |    \\       slope = -b
  |      \\
  +--------------> log C""",
        topic="scales-ticks", level=3),
    # ---------------------------------------------------------------- level 4
    mcq("From epoch 8 on, validation ACCURACY keeps rising slowly while validation LOSS (cross-entropy) also rises. What is the most likely story?",
        ["The model is getting over-confident: it gets a few more examples right but is very confident on the ones it gets wrong, and cross-entropy punishes confident mistakes heavily",
         "It can't happen; the plotting code must have mixed up the curves",
         "The learning rate is too low",
         "The model is underfitting"], 0,
        "Accuracy only checks which side of 0.5 a prediction is on. Loss checks how confident it was.",
        "Example: going from p(correct) = 0.7 on 8 of 10 rows to 0.99 on 9 rows plus 0.001 on one row raises accuracy from 0.8 to 0.9 but mean loss from 0.47 to 0.70, because -ln(0.001) is about 6.9. "
        "It's an early form of overfitting and a calibration problem. Which checkpoint to keep depends on the metric you ship. If you use the probabilities, consider early stopping on loss, label smoothing or temperature scaling.",
        diagram="""
      val acc  ___----      (slowly up)
      val loss     __/--    (up)
 +-------8---------------> epoch""",
        topic="training-curves", level=4),
    mcq("A long training run's loss curve shows rare sharp spikes that mostly recover within a few hundred steps, but one doesn't recover. What is the most sensible response?",
        ["Plot the gradient norm and LR alongside the loss to find the cause; use gradient clipping or a lower peak LR, and for the unrecovered spike, go back to an earlier checkpoint and skip or reshuffle the data that came next",
         "Ignore it; the spikes are a matplotlib rendering artefact",
         "Smooth the curve harder until the spikes disappear",
         "Double the learning rate to get past the spike faster"], 0,
        "A spike is a symptom. What would you plot next to find out why it happened?",
        "Spikes usually come with a gradient-norm spike: a bad or unusual batch, too high a peak LR, or optimiser state blowing up (e.g. Adam's second-moment estimate getting tiny). "
        "Clipping limits the damage, and restoring a checkpoint and skipping the batch is the standard fix for a spike the run doesn't recover from. "
        "Heavy smoothing only hides the evidence: always keep the raw curve available.",
        diagram="""
 loss          |          |
  |\\           |\\         |\\________  <- no recovery
  | \\__________| \\________|
  +------------------------------> step
 gnorm  ______|____________|________""",
        topic="reading-charts", level=4),
    mcq("Why does scikit-learn draw a precision-recall curve as a STEP plot instead of joining the points with straight lines, as ROC plots do?",
        ["Precision doesn't change linearly between two thresholds, so a straight line shows precision values no threshold actually gives; steps (and average_precision_score's step sum) show only what can be achieved",
         "Step plots render faster",
         "PR curves have only two points",
         "Straight lines are not allowed on a 0-1 axis"], 0,
        "Between two PR points, recall and precision change together in a non-linear way.",
        "Moving between two ROC points can be done with a mix of the two thresholds, so a straight line is fair. For PR, precision = TP / (TP + FP) is a ratio, and the true path between two points is curved, not straight. "
        "That's why PrecisionRecallDisplay uses drawstyle='steps-post', and why average precision (AP) is a sum of steps rather than auc(recall, precision) with the trapezoid rule. "
        "When you compare papers, check which one they report: the two numbers differ.",
        topic="ml-plots", level=4),
    mcq("Your fraud model's scores are mostly below 0.05. A reliability plot with `calibration_curve(y, p, n_bins=10)` shows a jagged line built from a few points at high probabilities. What's the better setup?",
        ["Use strategy='quantile' so every bin has the same number of samples, and show a histogram of p below the curve",
         "Increase n_bins to 100 with the default uniform bins",
         "Drop all predictions below 0.05",
         "Switch to a ROC curve, which measures calibration better"], 0,
        "With equal-WIDTH bins, how many rows land in the 0.9-1.0 bin?",
        "The default strategy='uniform' makes bins of equal width, so nearly every row falls in the first bin and the upper bins have a handful of rows each: the points there are mostly noise. "
        "strategy='quantile' gives each bin an equal share of the rows, so every point is equally reliable, and the bins crowd in where the predictions are. "
        "ROC is unaffected by calibration, so it can't measure it.",
        topic="ml-plots", level=4),
    mcq("A scatter of hours studied vs exam score for all students slopes DOWN. Coloured by course, every course's own cloud slopes UP. How do you read this?",
        ["Simpson's paradox: course is a confounder (harder courses need more hours but give lower scores), so the pooled trend is reversed; report the within-group trend and show the groups",
         "The colouring is wrong; one of the two trends must be a plotting bug",
         "More study hours lower exam scores",
         "Scatter plots can't show trends, so neither reading is valid"], 0,
        "Where does each course's cloud sit compared with the others?",
        "When groups differ in both x and y, the overall line can join the group centres rather than follow any group's own trend. The groups explain the pooled pattern. "
        "In ML this appears in metrics too, e.g. a model better on every segment but worse overall because of the segment mix. Colour or facet by the suspected confounder before drawing conclusions from a single trend line.",
        diagram="""
 score
  |  /A/
  |      /B/        each course slopes up
  |          /C/    pooled cloud slopes down
  +----------------> hours""",
        topic="reading-charts", level=4),
    mcq("Why are bar charts on a log y axis usually misleading?",
        ["A log axis has no zero, so each bar starts at an arbitrary lower limit; bar lengths and length ratios then depend on that limit rather than on the values",
         "matplotlib can't draw bars on a log axis",
         "Bars on a log axis are always the same height",
         "Log axes reverse the order of the bars"], 0,
        "Where does a bar start when log(0) doesn't exist?",
        "Bars ask the reader to compare lengths from a common zero. On a log axis the baseline is wherever the axis happens to start (say 1 or 0.1), so changing ylim changes how long the bars look relative to each other. "
        "For values that span orders of magnitude, use a dot plot or point markers on the log axis, or label the bars with the actual numbers.",
        topic="choosing", level=4),
    mcq("A learning-rate range test (LR increased each step, loss plotted against LR on a log x axis) shows loss flat, then falling steeply, reaching a minimum at 1e-2 and then exploding. Which LR is the usual pick?",
        ["Somewhere on the steep downward part, roughly 1e-3 (often about 10x below the minimum), not the minimum itself",
         "Exactly 1e-2, where the loss is lowest",
         "The largest LR before the curve explodes",
         "The smallest LR tested, to be safe"], 0,
        "At the minimum, the loss is just about to blow up.",
        "During the test the LR keeps climbing, so the lowest point sits right at the edge of instability, and the plotted loss also lags behind the LR. "
        "The steepest-descent region is where learning is fastest while still stable, so the rule of thumb is about a tenth of the minimum's LR. "
        "In an interview, explain that the x axis is the LR, not time, even though each point is one training step.",
        diagram="""
 loss
  |------\\                 /
  |       \\               /   explodes
  |        \\___       __/
  |            \\___/
  +--1e-5---1e-3---1e-2--1e-1--> LR (log)
            pick ^    ^ min""",
        topic="training-curves", level=4),
    mcq("A chart looks perfect in a Jupyter notebook, but the PNG saved with `fig.savefig('f.png')` has its y-label cut off. What explains the difference?",
        ["The notebook's inline backend renders with bbox_inches='tight' by default, which grows the image to fit everything; plain savefig keeps the exact figure size, so pass bbox_inches='tight' or use layout='constrained'",
         "Notebooks use a different font that is narrower",
         "savefig always crops 10% of each side",
         "The PNG viewer is cropping the image"], 0,
        "Notebook display and savefig are two different calls with different defaults.",
        "matplotlib-inline displays figures through print_figure with {'bbox_inches': 'tight'}, so labels that hang outside the figure edge are pulled back into the image. "
        "fig.savefig uses rcParams['savefig.bbox'], which defaults to None (the exact figsize), so anything outside the canvas is cut. "
        "Fixing the layout itself with constrained layout makes both outputs match, which matters in reports generated in CI.",
        topic="pitfalls", level=4),
    tf("ROC AUC equals the probability that a randomly chosen positive gets a higher score than a randomly chosen negative, with ties counted as half; for this snippet that gives 0.875.", True,
        "Count all positive-negative pairs: 2 positives x 2 negatives = 4 pairs.",
        "Pairs (pos, neg): 0.6 vs 0.2 win, 0.6 vs 0.6 tie (0.5), 0.9 vs 0.2 win, 0.9 vs 0.6 win, so 3.5 / 4 = 0.875. This is the Mann-Whitney U view of AUC. "
        "It explains why AUC ignores calibration and class balance (it only ranks pairs), and why heavily tied scores, such as a model that outputs only a few distinct values, give a staircase ROC with diagonal segments.",
        code="from sklearn.metrics import roc_auc_score\nprint(roc_auc_score([0, 0, 1, 1], [0.2, 0.6, 0.6, 0.9]))",
        topic="ml-plots", level=4),
    fill("A PDF with a 1-million-point scatter is 200 MB and slow to open. Pass ____=True to that scatter call so only that layer is stored as pixels, while text and axes stay as vectors.",
        "rasterized",
        "The opposite of 'vector', as an adjective.",
        "In vector formats every marker is a separate shape, so file size grows with the number of points. rasterized=True draws that one artist as an embedded bitmap at the savefig dpi. "
        "A 200k-point test went from about 3 MB to 24 KB, while labels and ticks stay sharp. It's the usual trick for embedding plots in papers.",
        topic="pitfalls", level=4),
]
