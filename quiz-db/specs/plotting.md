# Plotting Basics: coverage spec

**Ladder:** Foundations › Python for Data   ·   **Prerequisites:** Python basics, NumPy arrays, pd-dataframes (for pandas plotting)
**Why it matters for AI/ML:** you debug models with your eyes: loss curves show overfitting and bad learning rates, histograms show skewed features, confusion-matrix heatmaps show which classes get mixed up. Being able to make and READ these charts quickly is an everyday skill and a common interview topic.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `fig-axes` | Figure / Axes model | Figure vs Axes, fig, ax = plt.subplots(), lines accumulate, plot(x, y) order | plot returns a list of Line2D, x defaults to 0..n-1, figsize/dpi, Axes as a container | twinx adds an Axes, Artists, artists point back to .axes/.figure | which list (lines/patches/collections/texts) each call fills, set_xlim switches autoscale off, set_ydata needs relim + autoscale_view, twinx becomes the current Axes |
| 2 | `plot-types` | Line, bar, scatter, hist, box | which chart for trend / relationship / distribution | hist return values and edges, default 10 bins, BarContainer, box vs hist | box plot fliers (1.5 x IQR), barh, scatter as one PathCollection with c/s, overplotting, c= vs color=, s is area, hist2d counts, density=True area = 1, integer-data comb | 'o' format = Line2D without line, errorbar / fill_between / axhline artists, c=(1, 0, 0) with 3 points is colour-mapped, last hist bin is closed |
| 3 | `labels-legends` | Titles, labels, legends, styling | set_title/set_xlabel, legend needs labels | unlabelled lines skipped, format strings, set_xlim, legend placement | '_' labels hidden, default margins, text/annotate, plt.title targets the current Axes | — |
| 4 | `subplots` | Subplot grids | subplots(2, 3) shape | squeeze to 1-D, squeeze=False, IndexError with 2-D index, axs.flat, sharex, tight_layout | add_subplot numbering, shared limits, delaxes, axs.flat order / axs.T / len(axs) counts rows | subplot_mosaic with spanning cells |
| 5 | `pandas-plot` | Plotting from pandas | df.plot returns an Axes with one line per column | index -> x label, legend from columns, plot.bar grouping, hist 'Frequency', ax= | subplots=True array, value_counts bar, text columns skipped, groupby then plot | NaN becomes a masked gap |
| 6 | `training-curves` | Training curves and reading them | overfitting picture, underfitting picture | best epoch from val loss, high vs low learning rate shapes | val > train can be legit, log-scale loss, smoothing with rolling mean, comparing runs on a log scale | leakage-shaped curves, early stopping with patience, learning curves vs data size |
| 7 | `heatmaps` | imshow and confusion matrices | reading the diagonal | imshow + colorbar Axes, annotating cells and tick labels, origin='upper' | accuracy and precision from the matrix, clim autoscaling / vmin-vmax, row-normalising for imbalance | diverging colormaps for correlations, pixel-centred extents and inverted y |
| 8 | `choosing` | Choosing a chart, log scales | bar for categories, hist/box for distributions, no lines for unordered categories | set_yscale, when to use log, bars vs pies | log axis hides zeros, truncated bar baselines, PR curves | overlaid class score distributions vs bar of means |
| 9 | `pitfalls` | pyplot vs OO API, show/close/savefig | pyplot vs OO style, plt.show in scripts, savefig | current Axes drift, figures stay open until closed, show-then-savefig blank, plt.plot goes to the newest figure | cla vs clf, clf does not close, plt.close() closes only the current figure, pass ax into helper functions, Agg backend / MPLBACKEND on headless CI | pyplot is not thread-safe, Figure() outside pyplot, clf in a loop still leaks figures |
| 10 | `scales-ticks` | Twin axes, log/symlog scales, ticks and formatters | — | set_ylim(bottom=0), locator vs formatter | twinx shares x only and has its own legend, symlog + linthresh, equal pixels per decade, fractional epoch ticks, MaxNLocator(integer=True) | log axes show ratios (0.02 vs 0.01 = 2 vs 1), formatter rounding (round-half-even) |
| 11 | `color-images` | Colormaps, norms and image arrays | — | '_r' reversed maps, aspect='auto' for wide arrays | cmap LUT and RGBA, LogNorm, CenteredNorm, viridis vs jet, HxWxC uint8 vs float, CHW TypeError, cmap ignored for RGB | int vs float cmap lookup, NaN = transparent 'bad' colour and 'over' clipping, TwoSlopeNorm, denormalising images before imshow |
| 12 | `ml-plots` | ML evaluation plots | — | — | roc_curve arrays and the inf threshold, confusion_matrix label order, residual plot shapes | PR baseline = prevalence, normalize='true' vs 'pred', EMA lag picks a late checkpoint, calibration curve reading, t-SNE size/distance caveats, per-step vs per-epoch x axes |
| 13 | `reading-charts` | Reading and critiquing charts | — | LR-too-high divergence shape | — | flat loss at ln(C), twin-axis crossings are artefacts, single-seed comparisons and over-smoothing |

## Must-know facts
- A Figure is the canvas; an Axes is one plot inside it. fig, ax = plt.subplots() is the standard start.
- ax.plot returns a LIST of Line2D; with one argument x defaults to 0..n-1.
- Calling plotting methods on the same Axes adds to it; nothing is replaced.
- Lines live in ax.lines, bars/hist bars in ax.patches, scatter in ax.collections, text in ax.texts, images in ax.images.
- hist(bins=k) returns k counts and k+1 edges; the default is 10 bins.
- legend() shows only artists with labels; labels starting with '_' are hidden.
- subplots(r, c) returns a 2-D array of Axes, but a single row/column is squeezed to 1-D.
- df.plot() returns an Axes, uses the index for x and column names for the legend; pass ax= to target a subplot.
- Overfitting: train loss keeps falling while val loss rises. Underfitting: both high and close.
- Spiky / exploding loss -> learning rate too high; very slow steady decline -> too low.
- Confusion matrix: rows = true, columns = predicted (sklearn convention); diagonal = correct.
- Precision divides by a column sum, recall by a row sum.
- imshow draws row 0 at the top (origin='upper'); fig.colorbar adds an extra Axes.
- Log scales suit data spanning orders of magnitude; they cannot show 0 or negatives.
- Bars must start at zero; lines may zoom.
- pyplot keeps figures open until plt.close; save before show.
- Agg is the headless backend used on servers and in tests.
- set_xlim/set_ylim switch autoscaling off; after line.set_data you need ax.relim() + ax.autoscale_view().
- twinx shares x only, becomes the current Axes, and has its own legend (merge handles from both).
- symlog = linear within +-linthresh, log outside: use it for signed data spanning decades.
- Locators place ticks; formatters turn values into text.
- Colour pipeline: value -> norm (to 0..1) -> cmap -> RGBA. cmap(float) is a position, cmap(int) is a LUT index; NaN is transparent.
- Signed data: diverging cmap centred with TwoSlopeNorm / CenteredNorm; counts over decades: LogNorm. Prefer perceptually uniform maps (viridis) over jet.
- imshow wants (H, W) or (H, W, 3/4); RGB floats must be in [0, 1] (uint8 in 0..255) and ignore cmap. PyTorch (C, H, W) needs a transpose.
- scatter: c= is colour-mapped data, color= is a fixed colour; s is area in points^2.
- hist density=True makes the area 1 (heights can exceed 1); the last bin is closed on the right.
- sklearn: roc_curve's first threshold is inf; PR random baseline is the positive rate; confusion_matrix normalize='true' gives recall on the diagonal, 'pred' gives precision.
- Calibration curve below the diagonal = over-confident. t-SNE cluster sizes and gaps mean little.
- EMA smoothing lags: never pick a checkpoint from the smoothed curve. A flat loss at ln(C) = uniform predictions.

## Common traps (each one must have at least one question)
- Indexing axs[0, 1] on a 1-row grid -> IndexError.
- Calling legend() with unlabelled lines -> empty legend / warning.
- plt.title / plt.plot hitting the wrong (current) Axes in a multi-plot figure.
- Creating figures in a loop without closing -> memory leak.
- plt.show() then plt.savefig() -> blank image.
- Line chart for unordered categories.
- Truncated y axis on a bar chart exaggerates differences.
- Zeros silently vanish on a log axis.
- Default 10 histogram bins hide structure.
- Overplotting a million scatter points -> unreadable blob.
- Reading precision from a row (that's recall).
- Sequential colormap for signed data like correlations.
- Too-good-to-be-true validation curves -> leakage, not a great model.
- Expecting df.plot() to plot text columns.
- Plotting more data after set_xlim -> the new data is clipped. Updating a line with set_ydata -> points off-screen until relim.
- plt.ylabel after ax.twinx() -> labels the twin axis.
- fig.clf() or plt.close() (no argument) in a loop -> figures still pile up.
- cmap(label) with integer labels -> nearly identical colours (LUT index, not fraction).
- Plain Normalize on signed data -> zero is off-centre in a diverging map.
- imshow of a (C, H, W) tensor -> TypeError; of a normalised float image -> clipped, broken-looking colours.
- scatter(c=(1, 0, 0)) with exactly 3 points -> colour-mapped, not red.
- density=True heights read as probabilities -> they are densities and can exceed 1.
- Integer data with bins=10 -> a comb of empty bins.
- Diagonal baseline on a PR curve -> wrong; it is the positive rate.
- Heatmap tick labels in a different order than confusion_matrix's labels -> every cell mislabelled.
- Choosing the checkpoint from an EMA-smoothed curve -> a late, overfitted checkpoint.
- Reading t-SNE cluster size or distance as real -> wrong conclusions.
- Per-step train loss and per-epoch val loss plotted against their own indices -> val squeezed into the left edge.
- Crossings on twin y axes, single-seed comparisons, heavy smoothing -> misleading charts.
- FuncFormatter with ':.0f' -> 2500 shows as '2k' (round-half-even).

## Interview angle
- **"What does an overfitting loss curve look like and what do you do?"** Training loss keeps dropping while validation loss bottoms out and rises; the gap widens. Use early stopping at the validation minimum, regularisation (dropout, weight decay), augmentation, or more data. SDE analogy: code that passes the tests it was tuned on but fails on new inputs.
- **"How do you read a confusion matrix?"** Rows are the true class, columns the prediction; the diagonal is correct. Off-diagonal cells show which classes are confused. Precision per class = diagonal / column sum, recall = diagonal / row sum. Normalise rows for imbalanced data.
- **"Figure vs Axes, and why prefer the OO API?"** The Figure is the canvas, an Axes is one plot. pyplot's plt.* functions act on hidden global 'current' state; the OO API (ax.plot, ax.set_title) is explicit, which matters with subplots, in reusable functions and in servers. Analogy: global variables vs passing objects as parameters.
- **"Which chart would you use for X?"** Trend over time -> line; compare categories -> bar; relationship between two numbers -> scatter; distribution of one variable -> histogram; compare distributions across groups -> box plot; matrix of values -> heatmap.
- **"When would you use a log scale?"** When values span orders of magnitude (loss from 5 to 0.001, latency percentiles) or relative change matters. Not for data with zeros or negatives, and never on bar charts where length encodes value.

- **"How would you plot a correlation matrix or a weight-difference heatmap?"** imshow with a diverging colormap ('RdBu_r', 'coolwarm') and a norm centred at 0 (vmin=-1, vmax=1, TwoSlopeNorm or CenteredNorm), plus a colorbar. A sequential map or autoscaled limits make zero look like a real value.
- **"ROC or PR curve for a 1%-positive problem?"** PR: its baseline is the prevalence, and it shows the false-alarm cost of each catch. ROC can look excellent because the huge negative class keeps the FPR tiny. Plot from sklearn's arrays (roc_curve, precision_recall_curve) and draw the right baseline.
- **"What can you read from a t-SNE plot of embeddings?"** Local neighbourhoods and label noise, not cluster sizes or distances between clusters. Check claims with distances in the original space or with PCA.
- **"Your server-side report generator leaks memory. Why?"** pyplot keeps every figure until plt.close(fig). clf() and close() with no argument don't free the right one. Use the Agg backend and matplotlib.figure.Figure directly in services.

## Source material
To be added
