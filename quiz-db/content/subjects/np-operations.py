from textwrap import dedent

from helpers import mcq, tf, out, fill


def C(s):
    return dedent(s).strip("\n")


def ask(question, code, options, correct, hint, explanation, **kw):
    """An mcq about a code snippet (the snippet is shown and must run)."""
    return mcq(question, options, correct, hint, explanation, code=code, **kw)


SUBJECT = "np-operations"

TOPICS = [
    ("ufuncs", "Element-wise arithmetic and ufuncs"),
    ("broadcasting", "Broadcasting rules"),
    ("aggregation", "Aggregation and the axis argument"),
    ("compare-where", "Comparisons, np.where and np.clip"),
    ("sorting", "Sorting, argsort and unique"),
    ("linalg", "Linear algebra: dot, @, solve, norm"),
    ("vectorisation", "Vectorisation vs Python loops"),
    ("inplace", "In-place operations and out="),
    ("precision", "Integer overflow and float precision"),
    ("random", "Random numbers with seeds"),
    ("ml-idioms", "ML idioms: scaling, one-hot, softmax, distances"),
    ("stability", "Numerical stability"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ ufuncs
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        print(a + 10)
        """),
        ["[11 12 13]", "[1 2 3 10]", "[11, 12, 13]", "16"], 0,
        "The 10 is used for every element.",
        "Arithmetic between an array and a number applies to every element: 1+10, 2+10, 3+10.",
        topic="ufuncs", level=1),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        print(a * a)
        """),
        ["[1 4 9]", "14", "[1 2 3 1 2 3]", "[[1 2 3]\n [2 4 6]\n [3 6 9]]"], 0,
        "* pairs up elements in the same position.",
        "* is element-wise: 1*1, 2*2, 3*3. It is NOT the dot product (that would be 14, via @).",
        topic="ufuncs", level=1),
    mcq("What is a NumPy 'ufunc' (universal function), such as `np.sqrt` or `np.exp`?",
        ["A function that applies element by element to a whole array, in fast compiled code",
         "A function that only works on single numbers",
         "A function you must call inside a for-loop",
         "A function that returns a Python list"], 0,
        "Universal = works on any shape.",
        "A ufunc takes arrays of any shape and works on each element, running the loop in C. "
        "np.sqrt(np.array([4, 9])) gives [2. 3.] in one call.",
        topic="ufuncs", level=1),
    out(C("""
        import numpy as np
        print(np.sqrt(np.array([4, 9, 16])))
        """),
        ["[2. 3. 4.]", "[2 3 4]", "[16 81 256]", "29.0"], 0,
        "Square roots are usually not whole numbers, so what dtype comes back?",
        "np.sqrt works element-wise and returns float64, so 2.0, 3.0, 4.0 print as '2.', '3.', '4.'.",
        topic="ufuncs", level=1),
    fill("Which ufunc computes e to the power of every element: `np.____(a)`?", "exp",
         "Short for exponential.",
         "np.exp(a) gives e**a for each element. It is the heart of softmax and sigmoid.",
         topic="ufuncs", level=1),
    out(C("""
        import numpy as np
        a = np.array([1, 2])
        print(a / 2)
        print(a // 2)
        """),
        ["[0.5 1. ]\n[0 1]", "[0 1]\n[0 1]", "[0.5 1. ]\n[0.5 1. ]", "[0 1]\n[0.5 1. ]"], 0,
        "/ and // are different operators, like in Python.",
        "/ is true division and always returns float. // is floor division and keeps ints.",
        topic="ufuncs", level=2),
    ask("What do floor division and modulo give for 5 and -5?", C("""
        import numpy as np
        a = np.array([5, -5])
        print(a // 2, a % 2)
        """),
        ["[ 2 -3] [1 1]", "[ 2 -2] [ 1 -1]", "[ 2 -2] [1 1]", "[ 2 -3] [ 1 -1]"], 0,
        "Floor division rounds DOWN, toward minus infinity.",
        "-5 // 2 = floor(-2.5) = -3, and -5 % 2 = 1 so that (-3)*2 + 1 = -5. Same as Python, unlike C/Java/JS, which give -2 and -1.",
        topic="ufuncs", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        print(a ** 2)
        print(a ^ 2)
        """),
        ["[1 4 9]\n[3 0 1]", "[1 4 9]\n[1 4 9]", "[2 4 6]\n[3 0 1]", "[1 4 9]\nTypeError"], 0,
        "^ is not 'power' in Python.",
        "** is power. ^ is bitwise XOR: 1^2=3, 2^2=0, 3^2=1. Same as in JS and Java.",
        topic="ufuncs", level=2),
    out(C("""
        import numpy as np
        print(np.maximum(np.array([1, 5, 2]), np.array([3, 4, 2])))
        print(np.max(np.array([1, 5, 2])))
        """),
        ["[3 5 2]\n5", "5\n5", "[3 5 2]\n[3 5 2]", "[1 4 2]\n5"], 0,
        "One compares two arrays pair by pair; the other reduces one array.",
        "np.maximum is an element-wise ufunc (pairwise max). np.max is a reduction over the array. "
        "np.maximum(x, 0) is ReLU.",
        topic="ufuncs", level=2),
    ask("What table does np.add.outer build?", C("""
        import numpy as np
        print(np.add.outer(np.array([1, 2]), np.array([10, 20, 30])))
        """),
        ["[[11 21 31]\n [12 22 32]]", "[11 22]", "[[11 12]\n [21 22]\n [31 32]]", "ValueError"], 0,
        "outer combines EVERY element of the first with EVERY element of the second.",
        "ufunc.outer builds a table: row i, column j = a[i] + b[j], shape (2, 3). Same as a[:, None] + b.",
        topic="ufuncs", level=3),
    ask("Which pair of calls give identical results for `a = np.array([1, 2, 3, 4])`?",
        C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        print(np.add.reduce(a), np.add.accumulate(a))
        print(a.sum(), a.cumsum())
        """),
        ["np.add.reduce(a) == a.sum() and np.add.accumulate(a) == a.cumsum()",
         "np.add.reduce(a) == a.cumsum()",
         "np.add.accumulate(a) == a.sum()",
         "None of them; reduce and accumulate only exist for multiply"], 0,
        "reduce gives one answer, accumulate gives the running answer.",
        "Every binary ufunc has .reduce (fold to one value) and .accumulate (running fold). sum and cumsum are "
        "add.reduce and add.accumulate; prod and cumprod are the multiply versions.",
        analogy="reduce is JS array.reduce; accumulate is a 'scan' that keeps every intermediate value.",
        topic="ufuncs", level=3),
    ask("What does the guarded division return?", C("""
        import numpy as np
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([0.0, 4.0, 0.0])
        r = np.divide(a, b, out=np.zeros_like(a), where=b != 0)
        print(r)
        """),
        ["[0.  0.5 0. ]", "[inf 0.5 inf]", "[nan 0.5 nan]", "ZeroDivisionError"], 0,
        "where= decides which positions are computed; out= decides what the others hold.",
        "Only the position where b != 0 is divided. The other positions keep the value from out (zeros). "
        "Without out=, those positions would be uninitialised memory.",
        topic="ufuncs", level=4),
    tf("`np.exp` applied to an int64 array returns an int64 array.", False,
       "What is e**1?",
       "Most maths ufuncs (exp, log, sqrt, sin) have no integer loop, so ints are cast to float64 first.",
       topic="ufuncs", level=2),

    # ------------------------------------------------------------------ broadcasting
    tf("`np.array([1, 2, 3]) + 5` adds 5 to every element; this is the simplest case of broadcasting.", True,
       "The 5 is 'stretched' to the array's shape.",
       "Broadcasting lets NumPy treat a smaller operand as if it were repeated to match the bigger one, "
       "without actually copying it.",
       topic="broadcasting", level=1),
    mcq("What is the broadcasting rule for two shapes?",
        ["Line the shapes up from the RIGHT; each pair of sizes must be equal or one of them must be 1",
         "Line the shapes up from the LEFT; sizes must be equal",
         "The arrays must have the same number of dimensions",
         "The smaller array is repeated until it has the same total size"], 0,
        "Start from the last axis.",
        "Compare trailing dimensions first. A missing dimension counts as 1, and a 1 stretches to match the other size.",
        diagram="""
A:      4 x 3
B:          3     -> treated as 1 x 3
result: 4 x 3     (3 == 3, 1 stretches to 4)
""",
        topic="broadcasting", level=2),
    out(C("""
        import numpy as np
        col = np.arange(3).reshape(3, 1)
        row = np.arange(3)
        print(col + row)
        """),
        ["[[0 1 2]\n [1 2 3]\n [2 3 4]]", "[0 2 4]", "ValueError", "[[0 0 0]\n [1 1 1]\n [2 2 2]]"], 0,
        "(3, 1) and (3,) stretch in different directions.",
        "The column stretches across, the row stretches down, giving a 3x3 table of col[i] + row[j].",
        diagram="""
(3,1)  [[0]     (3,)  [0 1 2]
        [1]
        [2]]
     \\              /
       (3,3)  [[0 1 2]
               [1 2 3]
               [2 3 4]]
""",
        topic="broadcasting", level=2),
    out(C("""
        import numpy as np
        X = np.ones((2, 3))
        print((X + np.array([10, 20, 30])).shape)
        print(X + np.array([10, 20]))
        """),
        ["(2, 3)\nValueError", "(2, 3)\n(2, 3)", "ValueError", "(2, 3)\n[[11. 21.]]"], 0,
        "Compare from the right: 3 vs 3, then 3 vs 2.",
        "(2, 3) + (3,) works: the row is added to each row. (2, 3) + (2,) compares 3 with 2, which are "
        "different and neither is 1, so ValueError.",
        topic="broadcasting", level=2),
    ask("What is the broadcast result shape?", C("""
        import numpy as np
        a = np.zeros((8, 1, 6, 1))
        b = np.zeros((7, 1, 5))
        print((a + b).shape)
        """),
        ["(8, 7, 6, 5)", "ValueError", "(8, 7, 5, 6)", "(8, 1, 6, 5)"], 0,
        "Pad the shorter shape with 1s on the LEFT, then take the max of each pair.",
        "b becomes (1, 7, 1, 5). Pairwise: 8/1 -> 8, 1/7 -> 7, 6/1 -> 6, 1/5 -> 5.",
        diagram="""
a:  8  1  6  1
b:     7  1  5   -> 1 7 1 5
    ----------
    8  7  6  5
""",
        topic="broadcasting", level=3),
    out(C("""
        import numpy as np
        X = np.arange(12.0).reshape(4, 3)
        print((X - X.mean(axis=0)).shape)
        print(X - X.mean(axis=1))
        """),
        ["(4, 3)\nValueError", "(4, 3)\n(4, 3)", "ValueError", "(3,)\nValueError"], 0,
        "What shape does each mean have, and how does it line up from the right?",
        "mean(axis=0) has shape (3,), which matches the last axis: fine. mean(axis=1) has shape (4,), which is "
        "compared with 3 -> ValueError. Use X.mean(axis=1, keepdims=True) for per-row centring.",
        diagram="""
X              4 x 3
mean(axis=0)       3   -> 3 == 3  OK
mean(axis=1)       4   -> 4 vs 3  ValueError
keepdims=True  4 x 1   -> 1 stretches to 3  OK
""",
        topic="broadcasting", level=3),
    ask("What does `np.broadcast_shapes` return for these inputs?",
        C("""
        import numpy as np
        print(np.broadcast_shapes((5, 1), (1, 4)), np.broadcast_shapes((3,), (2, 1)))
        """),
        ["(5, 4) (2, 3)", "(5, 4) (3, 2)", "(5, 1) (2, 3)", "ValueError"], 0,
        "Apply the rule pair by pair from the right.",
        "(5,1) and (1,4): 1 vs 4 -> 4, 5 vs 1 -> 5. (3,) becomes (1,3) against (2,1) -> (2,3). "
        "Use broadcast_shapes to check shapes before running big computations.",
        topic="broadcasting", level=3),
    out(C("""
        import numpy as np
        a = np.zeros(3)
        b = np.ones((3, 3))
        a += b
        print(a)
        """),
        ["ValueError", "[1. 1. 1.]", "[3. 3. 3.]", "[[1. 1. 1.]\n [1. 1. 1.]\n [1. 1. 1.]]"], 0,
        "In-place operations cannot change the shape of the left side.",
        "a + b would broadcast to (3, 3), but += must write into a, which is only (3,). NumPy raises ValueError "
        "(non-broadcastable output operand).",
        topic="broadcasting", level=3),
    tf("Broadcasting `np.ones((1000, 1)) + np.ones((1, 1000))` first copies both inputs to shape (1000, 1000) before adding.", False,
       "Think about stride 0.",
       "The inputs are never materialised: NumPy iterates with stride 0 along the stretched axes. Only the "
       "(1000, 1000) result is allocated.",
       topic="broadcasting", level=3),
    mcq("You compute pairwise differences `A[:, None, :] - B[None, :, :]` with A of shape (20000, 512) and B of "
        "shape (20000, 512), both float64. What happens?",
        ["It tries to allocate a (20000, 20000, 512) result, about 1.6 TB, and fails with a memory error",
         "It returns a (20000, 512) array",
         "It raises ValueError because the shapes don't broadcast",
         "It runs fine because broadcasting never allocates memory"], 0,
        "The inputs are free; the RESULT is not.",
        "20000 x 20000 x 512 x 8 bytes is about 1.6e12 bytes. Broadcasting avoids copying inputs but must store the "
        "output. Use the ||a||^2 + ||b||^2 - 2 a.b trick (a matrix multiply) or process in chunks.",
        topic="broadcasting", level=4),
    out(C("""
        import numpy as np
        a = np.arange(3)
        b = np.broadcast_to(a, (2, 3))
        print(b.strides)
        b[0, 0] = 99
        """),
        ["(0, 8)\nValueError", "(24, 8)\n", "(0, 8)", "(8, 0)\nValueError"], 0,
        "Writing one element of a stride-0 view would change every row.",
        "broadcast_to returns a read-only view with stride 0 on the new axis. Assigning raises ValueError "
        "(assignment destination is read-only).",
        topic="broadcasting", level=4),
    ask("What 'accuracy' does this buggy code report?", C("""
        import numpy as np
        y_true = np.array([0, 1, 1])
        y_pred = np.array([[0], [1], [1]])
        print((y_true == y_pred).mean())
        """),
        ["0.5555555555555556", "1.0", "0.3333333333333333", "ValueError"], 0,
        "(3,) == (3, 1) does not compare position by position.",
        "Broadcasting turns this into a (3, 3) table of every pair, and 5 of 9 pairs match. Real accuracy is 1.0. "
        "Classic silent bug: always .ravel() or check shapes before comparing predictions.",
        diagram="""
y_true (3,)   -> (1, 3)  [0 1 1]
y_pred (3, 1)            [[0]
                          [1]
                          [1]]
result (3, 3): every pred vs every label
""",
        topic="broadcasting", level=4),

    # ------------------------------------------------------------------ aggregation
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        print(a.sum(), a.mean(), a.max())
        """),
        ["10 2.5 4", "10 2 4", "10.0 2.5 4.0", "[10] [2.5] [4]"], 0,
        "mean divides, so it gives a float.",
        "sum of ints stays int (10), mean is always float (2.5), max returns an element (4).",
        topic="aggregation", level=1),
    mcq("For a 2D array of shape (rows, cols), what does `a.sum(axis=0)` give?",
        ["One total per COLUMN (the rows are collapsed)", "One total per ROW", "The total of everything",
         "The first row"], 0,
        "axis=0 is the axis that disappears.",
        "The axis you name gets squashed. axis=0 runs down the rows, leaving one value per column.",
        diagram="""
        axis=1 ->
axis=0 [[0 1 2]
  |     [3 4 5]]
  v
sum(axis=0) -> [3 5 7]    sum(axis=1) -> [ 3 12]
""",
        topic="aggregation", level=1),
    out(C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        print(a.sum(axis=0))
        print(a.sum(axis=1))
        """),
        ["[3 5 7]\n[ 3 12]", "[ 3 12]\n[3 5 7]", "15\n15", "[0 1 2]\n[0 3]"], 0,
        "a = [[0 1 2], [3 4 5]].",
        "axis=0 adds down each column: 0+3, 1+4, 2+5. axis=1 adds across each row: 0+1+2, 3+4+5.",
        topic="aggregation", level=2),
    ask("What do the three argmax calls return?", C("""
        import numpy as np
        a = np.array([[1, 9], [8, 2]])
        print(a.argmax(), a.argmax(axis=1), a.argmax(axis=0))
        """),
        ["1 [1 0] [1 0]", "9 [9 8] [8 9]", "(0, 1) [1 0] [1 0]", "1 [0 1] [1 0]"], 0,
        "Without an axis, argmax looks at the FLATTENED array.",
        "Flattened: [1 9 8 2], the max is at index 1. Per row: row 0 max at col 1, row 1 at col 0. "
        "Per column: col 0 max at row 1, col 1 at row 0. Use np.unravel_index to turn a flat index into (row, col).",
        topic="aggregation", level=2),
    ask("What shapes come out of these sums on a (2, 3) array?",
        C("""
        import numpy as np
        a = np.ones((2, 3))
        print(a.sum(axis=1).shape, a.sum(axis=1, keepdims=True).shape)
        """),
        ["(2,) (2, 1)", "(2, 1) (2, 1)", "(3,) (1, 3)", "(2,) (2,)"], 0,
        "keepdims leaves a length-1 axis where the reduced one was.",
        "axis=1 removes the column axis: (2,). keepdims=True keeps it as size 1: (2, 1), which broadcasts back "
        "against (2, 3) correctly.",
        diagram="""
a            (2, 3)
sum(axis=1)  (2,)     axis 1 removed
keepdims     (2, 1)   axis 1 kept as size 1
(2, 3) / (2, 1) -> each row divided by its own total
""",
        topic="aggregation", level=2),
    fill("Which aggregation returns the INDEX of the largest value: `a.____()`?", "argmax",
         "'arg' = the argument (position) that gives the max.",
         "argmax returns the position, max returns the value. In classification, argmax over the class axis gives the predicted label.",
         topic="aggregation", level=2),
    out(C("""
        import numpy as np
        a = np.array([[1, 2], [3, 4]])
        print(a.cumsum(), a.cumsum(axis=0).tolist())
        """),
        ["[ 1  3  6 10] [[1, 2], [4, 6]]", "[[1 3]\n [3 7]] [[1, 2], [4, 6]]", "10 [[1, 2], [4, 6]]",
         "[ 1  3  6 10] [[1, 3], [3, 7]]"], 0,
        "Like sum, cumsum without an axis flattens first.",
        "No axis: running total over 1, 2, 3, 4. axis=0: running total down each column: [1, 2] then [1+3, 2+4].",
        topic="aggregation", level=3),
    ask("What do the two standard deviations come out as?", C("""
        import numpy as np
        x = np.array([1, 2, 3, 4])
        print(np.std(x), np.std(x, ddof=1))
        """),
        ["1.118033988749895 1.2909944487358056", "1.2909944487358056 1.118033988749895",
         "1.25 1.6666666666666667", "1.118033988749895 1.118033988749895"], 0,
        "NumPy's default divides by n, not n - 1.",
        "np.std uses ddof=0 (population std, divide by n). ddof=1 divides by n - 1 (sample std), which is "
        "what pandas' .std() uses by default, so the two libraries disagree unless you set ddof.",
        topic="aggregation", level=3),
    ask("What shape does reducing over two axes give?",
        C("""
        import numpy as np
        a = np.ones((2, 3, 4))
        print(a.sum(axis=(0, 2)).shape, a.mean(axis=-1).shape)
        """),
        ["(3,) (2, 3)", "(2, 4) (3, 4)", "(3,) (3, 4)", "(2, 4) (2, 3)"], 0,
        "Remove the named axes; -1 is the last one.",
        "Summing over axes 0 and 2 leaves axis 1: (3,). mean(axis=-1) removes the last axis: (2, 3). "
        "Example: mean over the sequence axis of a (batch, seq, dim) tensor.",
        topic="aggregation", level=3),
    out(C("""
        import numpy as np
        print(np.array([]).sum())
        print(np.array([]).max())
        """),
        ["0.0\nValueError", "0.0\n0.0", "ValueError", "nan\nnan"], 0,
        "What is the max of nothing?",
        "The empty sum is 0 (the identity of +). max has no identity, so it raises ValueError. Pass initial= "
        "(e.g. np.max(a, initial=-np.inf)) if empty inputs are possible.",
        topic="aggregation", level=3),
    out(C("""
        import numpy as np
        a = np.array([100, 100], dtype=np.int8)
        print(a.sum(), a.sum().dtype)
        print(a + a)
        """),
        ["200 int64\n[-56 -56]", "-56 int8\n[-56 -56]", "200 int64\n[200 200]", "-56 int8\n[200 200]"], 0,
        "Reductions and element-wise ops treat small ints differently.",
        "sum of a small int type is accumulated in the default int (int64), so 200 fits. a + a keeps int8 "
        "and silently wraps: 200 - 256 = -56.",
        topic="aggregation", level=4),
    out(C("""
        import numpy as np
        x = np.arange(24).reshape(2, 3, 4)
        m = x.max(axis=1, keepdims=True)
        print(m.shape, (x - m).shape, (x - x.max(axis=1)).shape)
        """),
        ["ValueError", "(2, 1, 4) (2, 3, 4) ValueError", "(2, 1, 4) (2, 3, 4) (2, 3, 4)", "(2, 4) (2, 3, 4) ValueError"], 0,
        "Without keepdims the result is (2, 4); line it up from the right against (2, 3, 4).",
        "With keepdims, (2, 1, 4) broadcasts back fine. Without it, (2, 4) is compared as (1, 2, 4) vs (2, 3, 4): "
        "2 vs 3 fails. Because the print evaluates all three first, the error happens before anything is printed.",
        question="What does this print? (Careful: when is the print evaluated?)",
        topic="aggregation", level=4),

    # ------------------------------------------------------------------ compare-where
    out(C("""
        import numpy as np
        a = np.array([1, 5, 10])
        print(np.clip(a, 2, 8))
        """),
        ["[2 5 8]", "[5]", "[1 5 10]", "[2 8]"], 0,
        "clip squashes values into a range.",
        "Values below 2 become 2, values above 8 become 8, the rest stay. Common for keeping probabilities away from 0 and 1.",
        topic="compare-where", level=1),
    out(C("""
        import numpy as np
        a = np.array([-2, 3, -1, 4])
        print(np.where(a > 0, a, 0))
        """),
        ["[0 3 0 4]", "[1 3]", "[3 4]", "[-2 0 -1 0]"], 0,
        "np.where(condition, if_true, if_false).",
        "Element by element: keep a where it is positive, otherwise 0. This is the ReLU activation.",
        analogy="It is a vectorised ternary: cond ? a : 0 for every element.",
        topic="compare-where", level=1),
    tf("`np.array([1, 2]) == np.array([1, 3])` returns a single True or False.", False,
       "Comparisons are element-wise too.",
       "It returns [ True False]. Use (a == b).all() or np.array_equal(a, b) for one answer.",
       topic="compare-where", level=1),
    ask("What does np.where return when given only a condition?", C("""
        import numpy as np
        a = np.array([5, 1, 7, 9])
        print(np.where(a > 4))
        """),
        ["(array([0, 2, 3]),)", "[5 7 9]", "[ True False  True  True]", "[0 2 3]"], 0,
        "With ONE argument, np.where tells you WHERE.",
        "np.where(cond) returns a tuple with one index array per axis (same as np.nonzero). For a 1D input "
        "that is a 1-tuple, which is why you often see np.where(...)[0].",
        topic="compare-where", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, -2, 3])
        print(np.any(a < 0), np.all(a > 0), (a > 0).sum())
        """),
        ["True False 2", "False True 2", "True True 2", "True False 3"], 0,
        "any = at least one, all = every one.",
        "One element is negative, so any(a < 0) is True and all(a > 0) is False. Two are positive.",
        topic="compare-where", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        print(np.array_equal(a, [1, 2, 3]), np.array_equal(a, [[1, 2, 3]]))
        print((a == [[1, 2, 3]]).all())
        """),
        ["True False\nTrue", "True True\nTrue", "True False\nFalse", "True True\nFalse"], 0,
        "array_equal also checks the shape; == broadcasts.",
        "array_equal requires identical shapes, so (3,) vs (1, 3) is False. == broadcasts them and every pair matches, so .all() is True.",
        topic="compare-where", level=2),
    out(C("""
        import numpy as np
        x = np.array([-3.0, 0.5, 7.0])
        print(np.clip(x, 0, None))
        """),
        ["[0.  0.5 7. ]", "[0. 0. 0.]", "TypeError", "[-3.   0.5  0. ]"], 0,
        "None means 'no limit on that side'.",
        "Only the lower bound applies, so negatives become 0. Equivalent to np.maximum(x, 0).",
        topic="compare-where", level=2),
    out(C("""
        import numpy as np
        x = np.array([0.0, 2.0])
        with np.errstate(divide="raise"):
            print(np.where(x != 0, 1 / x, 0))
        """),
        ["FloatingPointError", "[0.  0.5]", "[inf 0.5]", "ZeroDivisionError"], 0,
        "Arguments are evaluated before the function runs.",
        "np.where is a normal function: 1 / x is computed for EVERY element first, including 1/0. With divide='raise' "
        "that raises FloatingPointError. Normally it only warns, and where hides the inf. Use np.divide(..., where=...) to avoid it.",
        topic="compare-where", level=3),
    out(C("""
        import numpy as np
        score = np.array([45, 72, 90])
        grade = np.select([score >= 85, score >= 60], ["A", "B"], default="C")
        print(grade)
        """),
        ["['C' 'B' 'A']", "['A' 'B' 'C']", "['C' 'A' 'A']", "['B' 'B' 'A']"], 0,
        "np.select takes the FIRST condition that is true.",
        "90 matches >= 85 first -> A. 72 fails the first but matches >= 60 -> B. 45 matches nothing -> default C. "
        "It is a vectorised if / elif / else.",
        topic="compare-where", level=3),
    ask("What dtype does np.where give when the two branches differ?",
        C("""
        import numpy as np
        r = np.where(np.array([True, False]), 1, 0.5)
        print(r, r.dtype)
        """),
        ["[1.  0.5] float64", "[1 0] int64", "[1 0.5] object", "TypeError"], 0,
        "Both branches must fit in one result dtype.",
        "np.where promotes the two branches to a common dtype, int and float -> float64.",
        topic="compare-where", level=3),
    out(C("""
        import numpy as np
        a = np.array([3, 1, 2])
        lo = np.array([2, 2, 2])
        hi = np.array([2, 5, 2])
        print(np.clip(a, lo, hi))
        """),
        ["[2 2 2]", "[3 1 2]", "[2 1 2]", "ValueError"], 0,
        "The bounds can be arrays and broadcast like everything else.",
        "Per element: 3 clipped to [2, 2] -> 2; 1 clipped to [2, 5] -> 2; 2 clipped to [2, 2] -> 2.",
        topic="compare-where", level=4),
    tf("`np.where(cond, a, b)` short-circuits like `a if cond else b`, so `b` is only computed where `cond` is False.", False,
       "np.where is a function call.",
       "Both a and b are full arrays computed BEFORE np.where runs. Expensive or unsafe branches (log of negatives, "
       "division by zero) still run everywhere.",
       topic="compare-where", level=4),

    # ------------------------------------------------------------------ sorting
    out(C("""
        import numpy as np
        print(np.sort(np.array([3, 1, 2])))
        """),
        ["[1 2 3]", "[3 2 1]", "[1 2 0]", "None"], 0,
        "np.sort returns a new sorted array.",
        "np.sort sorts in ascending order and returns a copy. a.sort() sorts in place.",
        topic="sorting", level=1),
    out(C("""
        import numpy as np
        a = np.array([30, 10, 20])
        print(np.argsort(a))
        """),
        ["[1 2 0]", "[10 20 30]", "[2 0 1]", "[0 1 2]"], 0,
        "argsort gives the positions, in the order that would sort the array.",
        "The smallest (10) is at index 1, then 20 at index 2, then 30 at index 0: [1 2 0]. a[np.argsort(a)] is sorted.",
        topic="sorting", level=2),
    out(C("""
        import numpy as np
        a = np.array([3, 1, 2])
        r = a.sort()
        print(r, a)
        """),
        ["None [1 2 3]", "[1 2 3] [3 1 2]", "[1 2 3] [1 2 3]", "None [3 1 2]"], 0,
        "Methods that change the object in place usually return None.",
        "a.sort() sorts a itself and returns None, like Python's list.sort(). Use np.sort(a) for a sorted copy.",
        topic="sorting", level=2),
    ask("What do unique and its counts come out as?", C("""
        import numpy as np
        vals, counts = np.unique(np.array([3, 1, 3, 2, 1, 3]), return_counts=True)
        print(vals, counts)
        """),
        ["[1 2 3] [2 1 3]", "[3 1 2] [3 2 1]", "[1 2 3] [3 1 2]", "[3 1 3 2 1 3] [1 1 1 1 1 1]"], 0,
        "unique returns the values SORTED.",
        "np.unique sorts the distinct values and return_counts gives how often each appears: a quick class-balance check.",
        topic="sorting", level=2),
    fill("Reverse a sorted array to get descending order: `np.sort(a)[____]`", "::-1",
         "A slice with step -1.",
         "np.sort has no 'descending' flag; reverse the result with [::-1], or sort the negated values.",
         topic="sorting", level=2),
    out(C("""
        import numpy as np
        a = np.array([[3, 1], [2, 5]])
        print(np.sort(a))
        print(np.sort(a, axis=None))
        """),
        ["[[1 3]\n [2 5]]\n[1 2 3 5]", "[[2 1]\n [3 5]]\n[1 2 3 5]", "[1 2 3 5]\n[1 2 3 5]", "[[1 2]\n [3 5]]\n[1 2 3 5]"], 0,
        "The default axis for sort is the LAST one.",
        "np.sort sorts each row independently (axis=-1). axis=None flattens first.",
        topic="sorting", level=3),
    out(C("""
        import numpy as np
        X = np.array([[1, 30], [2, 10], [3, 20]])
        print(X[X[:, 1].argsort()])
        """),
        ["[[ 2 10]\n [ 3 20]\n [ 1 30]]", "[[ 1 10]\n [ 2 20]\n [ 3 30]]", "[[ 1 30]\n [ 2 10]\n [ 3 20]]", "[1 2 0]"], 0,
        "argsort one column, then use it to reorder whole rows.",
        "X[:, 1].argsort() is [1 2 0]; fancy indexing the rows with it keeps each row intact, sorted by column 1. "
        "Like ORDER BY col1 in SQL.",
        topic="sorting", level=3),
    ask("What does argsort applied twice produce?", C("""
        import numpy as np
        a = np.array([40, 10, 30, 20])
        print(a.argsort().argsort())
        """),
        ["[3 0 2 1]", "[1 3 2 0]", "[0 1 2 3]", "[10 20 30 40]"], 0,
        "argsort of an argsort turns positions into ranks.",
        "The rank of each element (0 = smallest): 40 is rank 3, 10 rank 0, 30 rank 2, 20 rank 1.",
        topic="sorting", level=3),
    ask("How does np.unique encode these labels?", C("""
        import numpy as np
        labels = np.array(["cat", "dog", "cat", "bird"])
        classes, ids = np.unique(labels, return_inverse=True)
        print(classes, ids)
        """),
        ["['bird' 'cat' 'dog'] [1 2 1 0]", "['cat' 'dog' 'bird'] [0 1 0 2]", "['bird' 'cat' 'dog'] [0 1 0 2]",
         "['cat' 'dog' 'bird'] [1 2 1 0]"], 0,
        "return_inverse maps each original element to its position in the sorted unique array.",
        "classes are sorted: bird, cat, dog. Each label is replaced by its index in classes: label encoding in one line. "
        "classes[ids] rebuilds the original.",
        topic="sorting", level=3),
    ask("Which two values come out as the top 2?", C("""
        import numpy as np
        a = np.array([5, 9, 1, 7, 3])
        top2 = a[np.argpartition(a, -2)[-2:]]
        print(np.sort(top2))
        """),
        ["[7 9]", "[1 3]", "[9 7]", "[5 9]"], 0,
        "argpartition puts the k largest at the end, in no particular order.",
        "np.argpartition(a, -2) guarantees the last 2 positions hold the 2 largest values (unordered). Sorting just "
        "those gives [7 9]. It runs in O(n), faster than a full sort for top-k.",
        topic="sorting", level=3),
    out(C("""
        import numpy as np
        a = np.array([2, 1, 2, 1])
        print(np.argsort(a, kind="stable"))
        """),
        ["[1 3 0 2]", "[3 1 2 0]", "[1 3 2 0]", "[0 2 1 3]"], 0,
        "A stable sort keeps equal elements in their original order.",
        "The two 1s (positions 1 and 3) keep their order, then the two 2s (positions 0 and 2). The default quicksort "
        "('introsort') does not promise this.",
        topic="sorting", level=4),
    mcq("You need the 10 highest-scoring items out of 50 million scores, in order. What is the best approach?",
        ["argpartition to get the top 10 in O(n), then argsort just those 10",
         "np.argsort(scores)[::-1][:10]: sorting is always fastest in NumPy",
         "A Python loop keeping a running top-10 list",
         "np.unique(scores)[-10:]"], 0,
        "You don't need the other 49,999,990 in order.",
        "A full sort is O(n log n) for information you throw away. argpartition is O(n), then sorting 10 items is "
        "trivial. np.unique also drops tied scores.",
        topic="sorting", level=4),
    out(C("""
        import numpy as np
        print(np.unique(np.array([1.0, np.nan, np.nan, 1.0])))
        print(np.searchsorted(np.array([10, 20, 30]), [5, 20, 35]))
        """),
        ["[ 1. nan]\n[0 1 3]", "[ 1. nan nan]\n[0 1 3]", "[ 1. nan]\n[0 2 3]", "[1.]\n[0 1 2]"], 0,
        "NumPy 2's unique collapses NaNs by default (equal_nan=True).",
        "unique merges all NaNs into one. searchsorted gives the insertion index that keeps the array sorted, "
        "inserting on the LEFT of equal values: 5 -> 0, 20 -> 1, 35 -> 3. It is binary search.",
        topic="sorting", level=4),

    # ------------------------------------------------------------------ linalg
    mcq("For two arrays `A` and `B`, what is the difference between `A * B` and `A @ B`?",
        ["* multiplies element by element; @ is matrix multiplication (rows times columns, summed)",
         "They are the same",
         "* is matrix multiplication; @ is element-wise",
         "@ only works on 1D arrays"], 0,
        "One of them is how linear layers work.",
        "* pairs up matching positions. @ is the matrix product: each output is a dot product of a row of A with a column of B.",
        topic="linalg", level=1),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        print(a @ b, np.dot(a, b))
        """),
        ["32 32", "[ 4 10 18] [ 4 10 18]", "32 [ 4 10 18]", "[ 4 10 18] 32"], 0,
        "Multiply the pairs, then add them up.",
        "For 1D arrays both are the dot product: 1*4 + 2*5 + 3*6 = 32.",
        topic="linalg", level=1),
    ask("What shape is the product of a (2, 3) matrix and a (3, 4) matrix?",
        C("""
        import numpy as np
        A = np.ones((2, 3))
        B = np.ones((3, 4))
        print((A @ B).shape)
        """),
        ["(2, 4)", "(3, 3)", "(2, 3, 4)", "(4, 2)"], 0,
        "The inner sizes must match and then disappear.",
        "(2, 3) @ (3, 4): the 3s match and cancel, leaving (2, 4).",
        diagram="""
 (2, 3) @ (3, 4)
     \\____/
   must match
 result: (2, 4)
""",
        topic="linalg", level=2),
    out(C("""
        import numpy as np
        A = np.ones((2, 3))
        print(A @ A)
        """),
        ["ValueError", "[[1. 1. 1.]\n [1. 1. 1.]]", "[[3. 3.]\n [3. 3.]]", "[[2. 2. 2.]\n [2. 2. 2.]]"], 0,
        "Inner sizes: 3 and 2.",
        "(2, 3) @ (2, 3) has inner sizes 3 vs 2, so ValueError. A @ A.T (shape (2, 2)) would work.",
        topic="linalg", level=2),
    ask("What do A * I and A @ I give?", C("""
        import numpy as np
        A = np.array([[1, 2], [3, 4]])
        I = np.eye(2, dtype=int)
        print(A * I)
        print(A @ I)
        """),
        ["[[1 0]\n [0 4]]\n[[1 2]\n [3 4]]", "[[1 2]\n [3 4]]\n[[1 2]\n [3 4]]",
         "[[1 0]\n [0 4]]\n[[1 0]\n [0 4]]", "[[1 2]\n [3 4]]\n[[1 0]\n [0 4]]"], 0,
        "Multiplying by the identity MATRIX leaves A unchanged, but only with @.",
        "A * I zeroes everything off the diagonal (element-wise). A @ I is the matrix product, which returns A.",
        topic="linalg", level=2),
    out(C("""
        import numpy as np
        print(np.linalg.norm(np.array([3, 4])))
        """),
        ["5.0", "7", "25", "3.5"], 0,
        "The length of a vector, Pythagoras style.",
        "The default norm is the Euclidean (L2) length: sqrt(3**2 + 4**2) = 5.0.",
        topic="linalg", level=2),
    out(C("""
        import numpy as np
        A = np.array([[2.0, 1.0], [1.0, 3.0]])
        b = np.array([3.0, 5.0])
        x = np.linalg.solve(A, b)
        print(x, np.allclose(A @ x, b))
        """),
        ["[0.8 1.4] True", "[1.4 0.8] True", "[1.5 1.6667] True", "[0.8 1.4] False"], 0,
        "Solve 2x + y = 3 and x + 3y = 5.",
        "solve finds x with A @ x = b: x = 0.8, y = 1.4. allclose confirms A @ x reproduces b.",
        topic="linalg", level=3),
    mcq("Why prefer `np.linalg.solve(A, b)` over `np.linalg.inv(A) @ b`?",
        ["solve factorises A once and is faster and more numerically accurate; forming the inverse adds work and error",
         "inv does not exist in NumPy 2",
         "solve works for any shape, inv only for 2x2",
         "They are identical internally"], 0,
        "Computing the inverse is an extra step you didn't need.",
        "solve uses an LU factorisation and back-substitution. inv computes the full inverse (more work) and then "
        "multiplies, compounding rounding error, especially for badly conditioned matrices.",
        topic="linalg", level=3),
    ask("What shapes result from mixing 1D vectors and 2D matrices with @?",
        C("""
        import numpy as np
        v = np.ones(3)
        M = np.ones((3, 2))
        N = np.ones((2, 3))
        print((v @ M).shape, (N @ v).shape)
        """),
        ["(2,) (2,)", "(1, 2) (2, 1)", "(3, 2) (2, 3)", "ValueError"], 0,
        "A 1D operand acts as a row on the left and a column on the right, then that axis is dropped.",
        "v @ M: v is treated as (1, 3) -> (1, 2) -> (2,). N @ v: v is treated as (3, 1) -> (2, 1) -> (2,).",
        topic="linalg", level=3),
    ask("What does .T do to a 1D vector?", C("""
        import numpy as np
        v = np.array([1, 2, 3])
        print(v.T.shape, v.reshape(-1, 1).T.shape)
        """),
        ["(3,) (1, 3)", "(3, 1) (1, 3)", "(1, 3) (3, 1)", "(3,) (3,)"], 0,
        "What does it mean to swap the axes of something with one axis?",
        ".T on a 1D array does nothing: there is only one axis. Make it 2D first (reshape(-1, 1) or v[:, None]) if you need a row/column.",
        topic="linalg", level=3),
    out(C("""
        import numpy as np
        A = np.array([[1.0, 2.0], [2.0, 4.0]])
        print(np.linalg.inv(A))
        """),
        ["LinAlgError", "[[ 4. -2.]\n [-2.  1.]]", "[[inf inf]\n [inf inf]]", "ZeroDivisionError"], 0,
        "Row 2 is exactly twice row 1.",
        "The rows are linearly dependent, so A is singular (determinant 0) and has no inverse: numpy.linalg.LinAlgError.",
        topic="linalg", level=3),
    ask("What shape does @ give for a batch of matrices?",
        C("""
        import numpy as np
        A = np.ones((5, 2, 3))
        B = np.ones((5, 3, 4))
        print((A @ B).shape)
        """),
        ["(5, 2, 4)", "(5, 2, 5, 4)", "(2, 4)", "ValueError"], 0,
        "@ treats leading axes as a batch.",
        "matmul multiplies the last two axes and broadcasts the rest: 5 independent (2,3) @ (3,4) products -> (5, 2, 4).",
        diagram="""
A: (5,  2, 3)
B: (5,  3, 4)
    ^   \\__/  inner 3s match
  batch
A @ B: (5, 2, 4)
""",
        topic="linalg", level=3),
    ask("What shapes do np.dot and np.matmul give on 3D inputs?", C("""
        import numpy as np
        a = np.ones((2, 3, 4))
        b = np.ones((2, 4, 5))
        print(np.dot(a, b).shape, np.matmul(a, b).shape)
        """),
        ["(2, 3, 2, 5) (2, 3, 5)", "(2, 3, 5) (2, 3, 5)", "(2, 3, 5) (2, 3, 2, 5)", "ValueError"], 0,
        "np.dot on N-d arrays is not a batch operation.",
        "np.dot sums over a's last axis and b's SECOND-TO-LAST axis, combining every block of a with every block "
        "of b: (2, 3) + (2, 5). matmul/@ broadcasts the batch axis instead. Use @ for batches.",
        topic="linalg", level=4),
    out(C("""
        import numpy as np
        M = np.array([[3.0, 4.0], [0.0, 0.0]])
        print(np.linalg.norm(M), np.linalg.norm(M, axis=1), np.linalg.norm(M, ord=1))
        """),
        ["5.0 [5. 0.] 4.0", "5.0 [5. 0.] 7.0", "7.0 [5. 0.] 4.0", "5.0 [3. 4.] 7.0"], 0,
        "For a matrix, ord=1 is the max column sum, not the sum of all entries.",
        "Default on a matrix: Frobenius norm sqrt(9 + 16) = 5. axis=1: one L2 norm per row. ord=1 on a matrix: "
        "the largest absolute column sum, max(3, 4) = 4.",
        topic="linalg", level=4),
    out(C("""
        import numpy as np
        A = np.arange(6).reshape(2, 3)
        B = np.ones((2, 3))
        print(np.einsum("ij,ij->i", A, B), np.einsum("ij->j", A))
        """),
        ["[ 3. 12.] [3 5 7]", "[ 3. 12.] [ 3 12]", "15.0 [3 5 7]", "[[0. 1. 2.]\n [3. 4. 5.]] [3 5 7]"], 0,
        "Indexes missing from the output are summed over.",
        "'ij,ij->i' multiplies matching elements and sums over j: a row-wise dot product. 'ij->j' sums over i: "
        "column sums. einsum is a tiny language for these contractions.",
        topic="linalg", level=4),
    mcq("`np.linalg.cond(A)` returns about 1e16 for a float64 matrix. What should you conclude?",
        ["A is numerically singular: solving A x = b may lose all ~16 significant digits",
         "A is perfectly conditioned",
         "A has 1e16 elements",
         "A is guaranteed to be invertible with full accuracy"], 0,
        "float64 carries about 16 significant digits.",
        "The condition number estimates how much input error is amplified. Around 1e16 you can lose all 16 digits, "
        "so the solution is meaningless. Use regularisation (e.g. ridge) or lstsq/pinv.",
        topic="linalg", level=4),

    # ------------------------------------------------------------------ vectorisation
    tf("'Vectorising' code means replacing Python for-loops over elements with whole-array NumPy operations.", True,
       "Who runs the loop?",
       "Vectorised code expresses the maths on whole arrays (a * b, a.sum()) so the loop runs in compiled C.",
       analogy="Like one bulk SQL UPDATE instead of updating rows one by one in an application loop.",
       topic="vectorisation", level=1),
    mcq("Which line replaces this loop?\n`for i in range(n): c[i] = a[i] * b[i] + 1`",
        ["c = a * b + 1", "c = a @ b + 1", "c = np.dot(a, b) + 1", "c = (a + 1) * b"], 0,
        "Each element only uses the elements at the same index.",
        "Element-wise maths on whole arrays matches the loop exactly. @ / np.dot would sum everything into one number.",
        topic="vectorisation", level=2),
    ask("Do the loop and the vectorised version agree?",
        C("""
        import numpy as np
        a = np.array([1.0, 2.0, 3.0])
        total = 0.0
        for x in a:
            total += x ** 2
        print(total, np.sum(a ** 2), a @ a)
        """),
        ["Yes: all three print 14.0", "No: the loop prints 14.0, the others 6.0", "No: a @ a gives [1. 4. 9.]",
         "No: np.sum(a ** 2) gives 36.0"], 0,
        "Sum of squares = dot product of a with itself.",
        "1 + 4 + 9 = 14. np.sum(a ** 2) and a @ a are vectorised forms of the loop; a @ a skips the temporary array.",
        topic="vectorisation", level=2),
    fill("Replace the loop `s = 0; for i in range(n): s += w[i] * x[i]` with one NumPy call: `s = np.____(w, x)`",
         "dot",
         "Multiply pairs and add them up.",
         "np.dot(w, x) (or w @ x) is the weighted sum: exactly what a neuron computes before its activation.",
         topic="vectorisation", level=2),
    mcq("Why is a Python loop over a million floats typically 50-100x slower than the NumPy equivalent?",
        ["Each iteration runs bytecode, boxes/unboxes a Python float and dispatches dynamically; NumPy runs one tight typed C loop (often SIMD)",
         "Python loops are single-threaded and NumPy always uses all cores",
         "NumPy precomputes results at import time",
         "Python floats are less precise than NumPy floats"], 0,
        "Count the work done per element in each case.",
        "Interpreter overhead per element is tens of nanoseconds; a C loop over packed doubles is about a nanosecond "
        "or less. Most NumPy ufuncs are single-threaded; the win is removing per-element overhead.",
        topic="vectorisation", level=3),
    tf("`np.vectorize(f)` compiles `f` to C, so it runs as fast as a built-in ufunc.", False,
       "Read the docs' note on performance.",
       "np.vectorize is a convenience wrapper: it still calls the Python function once per element. Real speed-ups "
       "come from rewriting f with array operations (or numba).",
       topic="vectorisation", level=3),
    mcq("Which loop CANNOT be replaced by a single element-wise expression like `a * b`?",
        ["x[i] = x[i-1] * 0.9 + a[i]  (each step depends on the previous result)",
         "c[i] = a[i] + b[i]",
         "c[i] = max(a[i], 0)",
         "c[i] = a[i] ** 2 if a[i] > 0 else 0"], 0,
        "Look for a dependency between iterations.",
        "A recurrence needs the previous output, so it is sequential. Some have special tools (cumsum, ufunc.accumulate, "
        "scipy.signal.lfilter); the others are plain a + b, np.maximum and np.where.",
        topic="vectorisation", level=3),
    out(C("""
        import numpy as np
        f = np.vectorize(lambda v: v / 2 if v > 1 else 0)
        print(f(np.array([0, 3])))
        g = np.vectorize(lambda v: v / 2 if v > 1 else 0, otypes=[float])
        print(g(np.array([0, 3])))
        """),
        ["[0 1]\n[0.  1.5]", "[0.  1.5]\n[0.  1.5]", "[0 1]\n[0 1]", "[0 1.5]\n[0.  1.5]"], 0,
        "np.vectorize guesses the output dtype from the FIRST call.",
        "The first element returns int 0, so the output array is int and 1.5 is truncated to 1. Pass otypes to fix it.",
        topic="vectorisation", level=4),
    mcq("You vectorise k-NN with a full (n_test, n_train) distance matrix and it runs out of memory. What is the standard fix?",
        ["Process test points in chunks (batches) so each chunk's distance matrix fits in memory",
         "Go back to a pure Python double loop",
         "Use float128 for more precision",
         "Call np.vectorize on the distance function"], 0,
        "Vectorisation trades memory for speed.",
        "Chunking keeps most of the vectorised speed while bounding the size of intermediates. This is exactly what "
        "batch sizes are for in deep learning.",
        topic="vectorisation", level=4),
    mcq("Which version computes the mean of every row of a (n, d) array most efficiently?",
        ["X.mean(axis=1)", "np.array([row.mean() for row in X])", "np.vectorize(np.mean)(X)",
         "np.apply_along_axis(np.mean, 1, X)"], 0,
        "Only one of these avoids a Python-level loop over rows.",
        "X.mean(axis=1) is a single C reduction. The comprehension and apply_along_axis loop in Python over rows; "
        "np.vectorize would even call np.mean per ELEMENT.",
        topic="vectorisation", level=3),

    # ------------------------------------------------------------------ inplace
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = a
        a += 1
        print(b)
        a = a + 1
        print(b)
        """),
        ["[2 3 4]\n[2 3 4]", "[1 2 3]\n[1 2 3]", "[2 3 4]\n[3 4 5]", "[1 2 3]\n[2 3 4]"], 0,
        "+= modifies the object; x = x + 1 creates a new one.",
        "a += 1 writes into the array that b also names, so b sees it. a = a + 1 builds a new array and rebinds a; "
        "b still points at the old one.",
        topic="inplace", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        a += 0.5
        print(a)
        """),
        ["UFuncTypeError", "[1.5 2.5 3.5]", "[1 2 3]", "[2 2 4]"], 0,
        "An in-place op cannot change the array's dtype.",
        "The result (float) cannot be stored safely into int64, so NumPy raises a casting error (UFuncTypeError, "
        "a subclass of TypeError). a = a + 0.5 would work and give a new float array.",
        topic="inplace", level=2),
    ask("Does `out=` reuse the existing array?",
        C("""
        import numpy as np
        a = np.array([1.0, 2.0, 3.0])
        r = np.multiply(a, 2, out=a)
        print(r is a, a)
        """),
        ["Yes: r is a, and a is now [2. 4. 6.]", "No: r is a new array, a is unchanged",
         "Yes, but a is unchanged", "No: out= only works with np.add"], 0,
        "out= says where to write the result.",
        "With out=a the ufunc writes into a and returns that same object. No new memory is allocated.",
        topic="inplace", level=2),
    ask("What is `a` after the overlapping in-place add?", C("""
        import numpy as np
        a = np.array([1, 1, 1, 1])
        a[1:] += a[:-1]
        print(a)
        """),
        ["[1 2 2 2]", "[1 2 3 4]", "[2 2 2 1]", "[1 1 1 1]"], 0,
        "Do the inputs see the values already overwritten?",
        "The source and destination overlap. NumPy detects this and buffers, so the result is as if a[:-1] had been "
        "copied first: every element just adds the original 1. For a running total use cumsum.",
        topic="inplace", level=3),
    mcq("Why do training loops on big arrays use `np.add(a, b, out=a)` or `a += b` instead of `a = a + b`?",
        ["They avoid allocating a new large temporary array on every step, reducing memory use and allocator time",
         "They are more precise",
         "They work for any dtype combination",
         "a = a + b is not allowed on arrays larger than 1 GB"], 0,
        "What does a + b have to create?",
        "a + b allocates a full-size result each time. In-place versions reuse a's buffer, which matters for "
        "multi-GB arrays. (Autograd frameworks may forbid in-place ops on tensors they need for backprop.)",
        topic="inplace", level=3),
    out(C("""
        import numpy as np
        a = np.ones(3, dtype=np.int64)
        np.multiply(a, 2.5, out=a, casting="unsafe")
        print(a)
        """),
        ["[2 2 2]", "[2.5 2.5 2.5]", "[3 3 3]", "UFuncTypeError"], 0,
        "casting='unsafe' allows the float result to be squeezed into int.",
        "The product 2.5 is computed in float and then cast (truncated) into the int64 output: 2. You asked for it explicitly.",
        topic="inplace", level=3),
    mcq("What is wrong with `r = np.divide(a, b, where=b != 0)` (no `out=`)?",
        ["Positions where b == 0 are left uninitialised, so r contains arbitrary leftover values there",
         "It raises ZeroDivisionError",
         "It returns NaN where b == 0",
         "Nothing; it returns 0 where b == 0"], 0,
        "where= skips positions. What is in the skipped slots?",
        "Without out=, NumPy allocates a fresh (np.empty-like) result and never writes the skipped positions. "
        "Always pair where= with out=np.zeros_like(a) (or another default).",
        topic="inplace", level=4),
    out(C("""
        import numpy as np
        x = np.arange(4.0)
        y = x[::2]
        np.exp(y, out=y)
        print(x)
        """),
        ["[1.        1.        7.3890561 3.       ]", "[0. 1. 2. 3.]",
         "[ 1.          2.71828183  7.3890561  20.08553692]", "ValueError"], 0,
        "y is a view on every second element of x.",
        "Writing the result into the view y changes x at positions 0 and 2 only: exp(0) = 1, exp(2) ~ 7.389.",
        topic="inplace", level=4),

    # ------------------------------------------------------------------ precision
    tf("In NumPy, `np.float64(0.1) + np.float64(0.2) == 0.3` is False, just like in plain Python.", True,
       "NumPy uses the same IEEE 754 doubles.",
       "0.1 and 0.2 are not exactly representable in binary, so the sum is 0.30000000000000004. Compare floats with a tolerance.",
       topic="precision", level=1),
    out(C("""
        import numpy as np
        print(0.1 + 0.2 == 0.3, np.isclose(0.1 + 0.2, 0.3))
        """),
        ["False True", "True True", "False False", "True False"], 0,
        "isclose allows a tiny tolerance.",
        "== demands exact bits; np.isclose checks |a - b| <= atol + rtol * |b| (defaults 1e-8 and 1e-5).",
        topic="precision", level=2),
    out(C("""
        import numpy as np
        a = np.array([1.0, 2.0])
        b = a + 1e-9
        print((a == b).all(), np.allclose(a, b))
        """),
        ["False True", "True True", "False False", "True False"], 0,
        "allclose is isclose(...).all().",
        "Tiny differences break ==. allclose returns one True if every pair is within tolerance; use it in tests.",
        analogy="Like assertEquals(expected, actual, delta) for doubles in JUnit.",
        topic="precision", level=2),
    out(C("""
        import numpy as np
        a = np.array([127], dtype=np.int8)
        print(a + 1)
        """),
        ["[-128]", "[128]", "OverflowError", "[127]"], 0,
        "int8 holds -128..127.",
        "Array integer arithmetic wraps around silently: 127 + 1 overflows to -128. No error, no warning.",
        diagram="""
int8 is a ring:   ... 126  127 | -128 -127 ...
                            +1 wraps here
""",
        topic="precision", level=2),
    mcq("Why should you never test floats with `==` in ML code (e.g. `if loss == 0.3`)?",
        ["Rounding errors make mathematically equal results differ in the last bits",
         "== is not defined for floats",
         "== on floats is slow",
         "Floats are random"], 0,
        "Think 0.1 + 0.2.",
        "Different operation orders give slightly different results. Use np.isclose / np.allclose or compare with a tolerance.",
        topic="precision", level=2),
    ask("What is element 3 of the arange grid, and does it equal 0.3?", C("""
        import numpy as np
        print(np.arange(0, 1, 0.1)[3], np.arange(0, 1, 0.1)[3] == 0.3)
        """),
        ["0.30000000000000004 False", "0.3 True", "0.3 False", "0.30000000000000004 True"], 0,
        "arange computes start + i * step.",
        "3 * 0.1 = 0.30000000000000004 in floating point, so == 0.3 fails. Filtering with x == 0.3 on such grids silently matches nothing.",
        topic="precision", level=3),
    out(C("""
        import numpy as np
        print(np.array([2**62]) * 4)
        print(np.float32(16777217))
        """),
        ["[0]\n16777216.0", "[18446744073709551616]\n16777217.0", "OverflowError\n", "[0]\n16777217.0"], 0,
        "int64 wraps modulo 2**64; float32 has a 24-bit mantissa.",
        "2**62 * 4 = 2**64, which wraps to 0 in int64. float32 cannot represent 2**24 + 1, so it rounds to 16777216.",
        topic="precision", level=3),
    ask("What does np.isclose say about 1e-10 vs 2e-10?", C("""
        import numpy as np
        print(np.isclose(1e-10, 2e-10), np.isclose(1e-10, 2e-10, atol=0))
        """),
        ["True False", "False False", "True True", "False True"], 0,
        "The default atol is 1e-8, much bigger than these numbers.",
        "|1e-10 - 2e-10| = 1e-10 <= atol (1e-8), so the default says 'close' even though one is double the other. "
        "For tiny values set atol=0 (or scale your data).",
        topic="precision", level=3),
    tf("`np.int8(127) + np.int8(1)` on scalars gives -128 and emits a RuntimeWarning about overflow.", True,
       "Scalar and array integer overflow are reported differently.",
       "NumPy scalar integer arithmetic warns on overflow (and still wraps to -128); array arithmetic wraps silently.",
       code=C("""
           import numpy as np
           import warnings
           warnings.simplefilter("ignore")
           print(np.int8(127) + np.int8(1))
           """),
       topic="precision", level=3),
    out(C("""
        import numpy as np
        print(np.isclose(100, 101, rtol=0.00995, atol=0), np.isclose(101, 100, rtol=0.00995, atol=0))
        """),
        ["True False", "True True", "False False", "False True"], 0,
        "The tolerance is relative to the SECOND argument only.",
        "isclose(a, b) checks |a - b| <= rtol * |b|. With b = 101 the tolerance is 1.005 (pass); with b = 100 it is 0.995 (fail). "
        "isclose is not symmetric; math.isclose uses max(|a|, |b|) instead.",
        topic="precision", level=4),
    out(C("""
        import numpy as np
        x = np.array([1e16])
        print(x + 1 - 1e16, x - 1e16 + 1)
        """),
        ["[0.] [1.]", "[1.] [1.]", "[0.] [0.]", "[1.] [0.]"], 0,
        "Floating-point addition is not associative.",
        "At 1e16 the gap between doubles is 2, so 1e16 + 1 rounds back to 1e16. Order of operations changes the result, "
        "which is why parallel GPU sums are not bit-for-bit reproducible.",
        topic="precision", level=4),
    out(C("""
        import numpy as np
        eps = np.finfo(np.float32).eps
        print(eps, np.float32(1) + np.float32(1e-8) == 1)
        """),
        ["1.1920929e-07 True", "2.220446049250313e-16 True", "1.1920929e-07 False", "1e-08 False"], 0,
        "eps is the gap between 1.0 and the next representable float.",
        "float32 eps is 2**-23 ~ 1.19e-7. Adding 1e-8 to 1 is below half that gap, so it disappears. float64 eps is 2.2e-16.",
        topic="precision", level=4),

    # ------------------------------------------------------------------ random
    mcq("Why do ML notebooks set a random seed, e.g. `rng = np.random.default_rng(42)`?",
        ["So the 'random' numbers are the same on every run, making results reproducible",
         "To make the numbers more random",
         "To speed up random number generation",
         "Because NumPy refuses to make random numbers without one"], 0,
        "Think: can someone else get your exact results?",
        "A seed fixes the starting point of the pseudo-random sequence, so splits, initial weights and shuffles repeat exactly.",
        topic="random", level=1),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        r = rng.integers(1, 7, size=1000)
        print(r.min(), r.max())
        """),
        ["1 6", "1 7", "0 6", "0 7"], 0,
        "The high value is exclusive, like range().",
        "rng.integers(1, 7) draws from 1..6 (dice rolls). With 1000 draws both ends appear.",
        topic="random", level=1),
    ask("What can you say about `rng.random(3)`?",
        C("""
        import numpy as np
        rng = np.random.default_rng(1)
        x = rng.random(3)
        print(x.shape, ((x >= 0) & (x < 1)).all())
        """),
        ["Shape (3,), every value in [0, 1)", "Shape (3,), values in [0, 3)", "Shape (1, 3), values in [-1, 1]",
         "One float, between 0 and 3"], 0,
        "random() is uniform on the unit interval.",
        "rng.random(size) returns floats uniform on [0, 1): 0 included, 1 excluded.",
        topic="random", level=2),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        x = rng.normal(loc=5, scale=2, size=100_000)
        print(round(x.mean()), round(x.std()))
        """),
        ["5 2", "0 1", "5 4", "2 5"], 0,
        "loc is the mean and scale is the standard deviation.",
        "normal(loc, scale) samples a bell curve centred at loc with spread scale. With 100k samples the estimates are very close.",
        topic="random", level=2),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        print(np.sort(rng.choice(5, size=5, replace=False)))
        """),
        ["[0 1 2 3 4]", "[0 0 1 3 4]", "[1 2 3 4 5]", "ValueError"], 0,
        "Without replacement, nothing can repeat.",
        "Choosing 5 of 0..4 without replacement must pick each exactly once, so the sorted result is all of them (a shuffle).",
        topic="random", level=2),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        a = np.arange(5)
        r = rng.shuffle(a)
        p = rng.permutation(5)
        print(r, np.sort(a), np.sort(p))
        """),
        ["None [0 1 2 3 4] [0 1 2 3 4]", "[0 1 2 3 4] [0 1 2 3 4] [0 1 2 3 4]", "None [0 1 2 3 4] None",
         "[4 2 0 1 3] [0 1 2 3 4] [0 1 2 3 4]"], 0,
        "One shuffles in place, the other returns a new array.",
        "rng.shuffle(a) shuffles a itself and returns None. rng.permutation returns a shuffled copy. "
        "Either way the values are unchanged, only their order.",
        topic="random", level=2),
    ask("After the shared permutation, are the samples still matched with their labels?", C("""
        import numpy as np
        rng = np.random.default_rng(0)
        X = np.arange(10).reshape(5, 2)
        y = X[:, 0] * 10
        idx = rng.permutation(len(X))
        Xs, ys = X[idx], y[idx]
        print((Xs[:, 0] * 10 == ys).all())
        """),
        ["True", "False", "IndexError", "It depends on the seed"], 0,
        "Both arrays are reordered with the SAME index array.",
        "One permutation applied to both X and y keeps every sample matched with its label. Shuffling X and y "
        "separately would scramble the labels.",
        topic="random", level=3),
    ask("Does drawing all at once match drawing one at a time from the same seed?",
        C("""
        import numpy as np
        a = np.random.default_rng(7).random(3)
        rng = np.random.default_rng(7)
        b = np.array([rng.random() for _ in range(3)])
        print(np.array_equal(a, b))
        """),
        ["Yes: the generator produces the same stream either way", "No: batch draws use a different algorithm",
         "No: the second generator is reseeded on every call", "It is random each run"], 0,
        "The generator's state advances by the same amount.",
        "A Generator is a deterministic stream: three single draws consume the same numbers as one draw of size 3. "
        "Any extra call in between, though, shifts everything after it.",
        topic="random", level=3),
    mcq("A data pipeline creates `rng = np.random.default_rng(0)` inside a function called once per batch. What goes wrong?",
        ["Every batch gets the SAME random numbers (same augmentations / same shuffle)",
         "Nothing; each call is independent and random",
         "It raises because a seed can be used only once",
         "Batches get different numbers, but only after the first epoch"], 0,
        "What state does a freshly seeded generator start in?",
        "Re-creating the generator with the same seed restarts the same sequence each time. Create it once and pass it "
        "around, or derive child generators with rng.spawn / SeedSequence.",
        topic="random", level=3),
    mcq("You start 8 worker processes for a simulation. What is the recommended way to give each its own random stream?",
        ["Spawn child seeds from one SeedSequence (e.g. np.random.SeedSequence(42).spawn(8)) and build a Generator from each",
         "Use default_rng(42) in every worker",
         "Use seeds 42, 43, ..., 49 and hope streams don't overlap",
         "Call np.random.seed() in each worker"], 0,
        "You want independent AND reproducible streams.",
        "SeedSequence.spawn produces statistically independent child seeds from one root seed, so the run is reproducible "
        "and workers don't share or correlate streams. Identical seeds would make every worker do the same thing.",
        topic="random", level=4),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        print(rng.integers(0, 2, size=10_000).max(), rng.integers(0, 2, size=10_000, endpoint=True).max())
        """),
        ["1 2", "2 2", "1 1", "0 1"], 0,
        "endpoint=True makes the high value inclusive.",
        "By default integers(low, high) excludes high, so the max is 1. endpoint=True includes it, so 2 appears.",
        topic="random", level=4),
    tf("Two Generators created with `default_rng(0)` on different machines with the same NumPy version produce the same numbers.", True,
       "The algorithm (PCG64) is fully specified.",
       "Bit generators are deterministic and platform-independent for a given NumPy version. NumPy does not promise "
       "the same streams across major versions for every distribution method, so pin versions for exact reproducibility.",
       topic="random", level=4),

    # ------------------------------------------------------------------ ml-idioms
    out(C("""
        import numpy as np
        y_true = np.array([1, 0, 1, 1])
        y_pred = np.array([1, 0, 0, 1])
        print((y_true == y_pred).mean())
        """),
        ["0.75", "3", "0.25", "[ True  True False  True]"], 0,
        "The mean of booleans is the fraction of Trues.",
        "3 of 4 predictions match, so accuracy = 0.75. mean() of a mask is the standard accuracy one-liner.",
        topic="ml-idioms", level=1),
    out(C("""
        import numpy as np
        x = np.array([10.0, 20.0, 30.0])
        print((x - x.min()) / (x.max() - x.min()))
        """),
        ["[0.  0.5 1. ]", "[10. 20. 30.]", "[-1.  0.  1.]", "[0.33 0.67 1.  ]"], 0,
        "Shift so the min is 0, then scale so the max is 1.",
        "Min-max scaling: (x - 10) / 20 gives 0, 0.5, 1.",
        topic="ml-idioms", level=2),
    ask("After standardising, what are the column means and stds?", C("""
        import numpy as np
        rng = np.random.default_rng(0)
        X = rng.normal(50, 10, size=(100, 3))
        Z = (X - X.mean(axis=0)) / X.std(axis=0)
        print(np.allclose(Z.mean(axis=0), 0), np.allclose(Z.std(axis=0), 1))
        """),
        ["True True", "True False", "False True", "ValueError"], 0,
        "axis=0 gives one mean and std per feature (column).",
        "Standardising per column gives every feature mean 0 and std 1. The (3,) stats broadcast across the 100 rows.",
        topic="ml-idioms", level=2),
    out(C("""
        import numpy as np
        y = np.array([0, 2, 1])
        print(np.eye(3)[y])
        """),
        ["[[1. 0. 0.]\n [0. 0. 1.]\n [0. 1. 0.]]", "[[1. 0. 0.]\n [0. 1. 0.]\n [0. 0. 1.]]", "[0. 2. 1.]",
         "[[0. 0. 1.]\n [1. 0. 0.]\n [0. 1. 0.]]"], 0,
        "Row k of the identity matrix is the one-hot vector for class k.",
        "Fancy indexing the rows of eye(3) with the labels picks one identity row per label: one-hot encoding.",
        diagram="""
np.eye(3)        y = [0, 2, 1]
row 0 [1 0 0] <- label 0
row 1 [0 1 0] <- label 1
row 2 [0 0 1] <- label 2
""",
        topic="ml-idioms", level=2),
    ask("What does dividing each row by its norm do?",
        C("""
        import numpy as np
        X = np.array([[3.0, 4.0], [1.0, 0.0]])
        U = X / np.linalg.norm(X, axis=1, keepdims=True)
        print(U)
        print(np.linalg.norm(U, axis=1))
        """),
        ["Makes every row a unit vector (length 1) while keeping its direction", "Makes every column sum to 1",
         "Standardises each column to mean 0", "Raises, because the shapes (2, 2) and (2, 1) don't broadcast"], 0,
        "keepdims makes the norms a (2, 1) column.",
        "Each row is divided by its own length, so rows become unit vectors: [0.6 0.8] and [1 0]. After this, "
        "cosine similarity is just a dot product.",
        topic="ml-idioms", level=2),
    ask("What does the broadcast comparison produce?", C("""
        import numpy as np
        y = np.array([2, 0, 1])
        print((y[:, None] == np.arange(3)).astype(int))
        """),
        ["[[0 0 1]\n [1 0 0]\n [0 1 0]]", "[[1 0 0]\n [0 1 0]\n [0 0 1]]", "[0 0 1 1 0 0 0 1 0]", "ValueError"], 0,
        "(3, 1) compared with (3,) broadcasts to a 3x3 table.",
        "Row i, column j is True where y[i] == j: one-hot encoding by broadcasting, no loop and no identity matrix.",
        topic="ml-idioms", level=3),
    out(C("""
        import numpy as np
        logits = np.array([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]])
        e = np.exp(logits - logits.max(axis=1, keepdims=True))
        p = e / e.sum(axis=1, keepdims=True)
        print(p.sum(axis=1), p.argmax(axis=1), round(p[1, 0], 4))
        """),
        ["[1. 1.] [2 0] 0.3333", "[1. 1.] [2 2] 0.3333", "[6. 3.] [2 0] 1.0", "[1. 1.] [2 0] 0.0"], 0,
        "Softmax rows sum to 1; ties go to the first index.",
        "Each row is a probability distribution (sums to 1). Row 0 is most confident in class 2. Row 1 is uniform "
        "(1/3 each) and argmax returns the first maximum, index 0.",
        topic="ml-idioms", level=3),
    out(C("""
        import numpy as np
        logits = np.array([[1.0, 2.0, 3.0], [3.0, 1.0, 1.0], [0.0, 0.0, 5.0]])
        e = np.exp(logits)
        p = e / e.sum(axis=1)
        print(np.allclose(p.sum(axis=1), 1))
        """),
        ["False", "True", "ValueError", "nan"], 0,
        "e.sum(axis=1) has shape (3,). Which axis does it line up with?",
        "Without keepdims the (3,) row sums broadcast across COLUMNS, so element [i, j] is divided by the sum of row j. "
        "With a square batch there is no error, just wrong probabilities. Always use keepdims=True.",
        diagram="""
e          (3, 3)
row sums   (3,)  -> lined up as (1, 3): one per COLUMN
p[i, j] = e[i, j] / rowsum[j]     wrong!
keepdims   (3, 1): p[i, j] = e[i, j] / rowsum[i]
""",
        topic="ml-idioms", level=3),
    out(C("""
        import numpy as np
        a = np.array([1.0, 0.0])
        b = np.array([1.0, 1.0])
        cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
        print(round(cos, 4))
        """),
        ["0.7071", "1.0", "0.5", "1.4142"], 0,
        "cos = dot / (length x length).",
        "a . b = 1, |a| = 1, |b| = sqrt(2), so cos = 1/sqrt(2) ~ 0.7071: a 45 degree angle.",
        topic="ml-idioms", level=3),
    ask("What shape is the pairwise distance matrix?",
        C("""
        import numpy as np
        A = np.ones((5, 3))
        B = np.zeros((4, 3))
        D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=-1)
        print(D.shape, round(D[0, 0], 4))
        """),
        ["(5, 4), and D[0, 0] = 1.7321", "(5, 3), and D[0, 0] = 3.0", "(4, 5), and D[0, 0] = 1.7321", "(5, 4, 3), and D[0, 0] = 1.0"], 0,
        "(5, 1, 3) - (1, 4, 3) -> (5, 4, 3); then norm over the last axis.",
        "Broadcasting builds every A-row minus B-row pair (5, 4, 3); the norm over the features gives a (5, 4) matrix. "
        "D[0, 0] = |(1, 1, 1)| = sqrt(3).",
        diagram="""
A[:, None, :]  (5, 1, 3)
B[None, :, :]  (1, 4, 3)
difference     (5, 4, 3)
norm(axis=-1)  (5, 4)    D[i, j] = |A[i] - B[j]|
""",
        topic="ml-idioms", level=3),
    out(C("""
        import numpy as np
        probs = np.array([0.1, 0.5, 0.15, 0.25])
        print(np.argsort(probs)[::-1][:2])
        """),
        ["[1 3]", "[0 2]", "[0.5  0.25]", "[3 1]"], 0,
        "argsort is ascending; reverse it for the best first.",
        "Ascending order of indexes is [0 2 3 1]; reversed it is [1 3 2 0]; the top 2 classes are 1 and 3.",
        topic="ml-idioms", level=3),
    mcq("You standardise features before a train/test split, using the mean and std of ALL the data. What is the problem?",
        ["Data leakage: test-set statistics influence training. Fit mean/std on the training set and apply them to test",
         "None; more data gives better statistics",
         "Standardisation must be done after training",
         "std must be computed with ddof=1 for test data"], 0,
        "In production you won't know the future data's mean.",
        "The test set must act like unseen data. Compute the mean and std on train only, then reuse those exact numbers on test.",
        topic="ml-idioms", level=3),
    ask("What shapes do the batched attention-score computations give?",
        C("""
        import numpy as np
        Q = np.ones((2, 4, 8))
        K = np.ones((2, 4, 8))
        S = Q @ K.transpose(0, 2, 1)
        S2 = np.einsum("bqd,bkd->bqk", Q, K)
        print(S.shape, np.array_equal(S, S2), S[0, 0, 0])
        """),
        ["(2, 4, 4), equal, 8.0", "(2, 8, 8), equal, 4.0", "(2, 4, 4), not equal, 8.0", "(4, 4), equal, 16.0"], 0,
        "Transpose only the last two axes of K: (2, 8, 4).",
        "(2, 4, 8) @ (2, 8, 4) -> (2, 4, 4): one query-by-key score matrix per batch item. Each score is a dot of two "
        "8-dim ones vectors = 8. The einsum writes the same thing explicitly.",
        topic="ml-idioms", level=4),
    ask("What do the expanded formula and the direct formula give for the squared distance?", C("""
        import numpy as np
        X = np.array([[1e8 + 1.0, 1e8], [1e8, 1e8 + 1.0]])
        sq = (X ** 2).sum(axis=1)
        D2 = sq[:, None] + sq[None, :] - 2 * X @ X.T
        print(D2[0, 1], ((X[0] - X[1]) ** 2).sum())
        """),
        ["0.0 2.0", "2.0 2.0", "-2.0 2.0", "0.0 0.0"], 0,
        "The expansion subtracts two huge, nearly equal numbers.",
        "|a|^2 + |b|^2 - 2a.b is fast (one matmul) but each term is ~4e16 here, where float64 spacing is 8, so the true "
        "answer 2 is lost. Centre the data first, and clip at 0 before sqrt because results can even go negative.",
        topic="ml-idioms", level=4),
    out(C("""
        import numpy as np
        logits = np.array([2.0, 1.0, 0.1])
        p = np.exp(logits) / np.exp(logits).sum()
        print(np.argmax(p) == np.argmax(logits), np.allclose(p, np.exp(logits - 5) / np.exp(logits - 5).sum()))
        """),
        ["True True", "True False", "False True", "False False"], 0,
        "exp is increasing, and softmax(x) = softmax(x + c).",
        "Because exp preserves order, argmax(softmax) = argmax(logits): you can skip softmax at prediction time. "
        "Shifting all logits by a constant leaves softmax unchanged, which is the basis of the max-subtraction trick.",
        topic="ml-idioms", level=4),

    # ------------------------------------------------------------------ stability
    out(C("""
        import numpy as np
        x = np.array([1000.0, 1001.0])
        with np.errstate(over="ignore", invalid="ignore"):
            naive = np.exp(x) / np.exp(x).sum()
        stable = np.exp(x - x.max()) / np.exp(x - x.max()).sum()
        print(naive, stable)
        """),
        ["[nan nan] [0.26894142 0.73105858]", "[0.26894142 0.73105858] [0.26894142 0.73105858]",
         "[inf inf] [0.26894142 0.73105858]", "[0. 1.] [0.26894142 0.73105858]"], 0,
        "exp(1000) is far beyond the largest float64 (~1.8e308).",
        "exp overflows to inf, and inf / inf = nan. Subtracting the max first makes the largest exponent exp(0) = 1, "
        "so nothing overflows and the answer is unchanged.",
        topic="stability", level=3),
    mcq("Why is subtracting the max before softmax safe, i.e. why doesn't it change the answer?",
        ["softmax(x - c) = softmax(x) for any constant c: the e^-c factor cancels between top and bottom",
         "It changes the answer slightly, but nobody notices",
         "Because the max element is always 0",
         "Because exp(x - c) = exp(x) - exp(c)"], 0,
        "Write exp(x_i - c) as exp(x_i) * exp(-c).",
        "Every term in numerator and denominator gets the same factor e^-c, which cancels. Choosing c = max(x) keeps "
        "every exponent <= 0, so nothing overflows and at least one term is exactly 1.",
        topic="stability", level=3),
    out(C("""
        import numpy as np
        x = np.array([1000.0, 1000.0])
        with np.errstate(over="ignore"):
            print(np.log(np.sum(np.exp(x))))
        m = x.max()
        print(m + np.log(np.sum(np.exp(x - m))))
        """),
        ["inf\n1000.6931471805599", "1000.6931471805599\n1000.6931471805599", "nan\n1000.0", "inf\n1000.0"], 0,
        "log(e^1000 + e^1000) = 1000 + log 2.",
        "The naive log-sum-exp overflows. Factoring out the max gives m + log(sum(exp(x - m))) = 1000 + log(2). "
        "This logsumexp trick is how cross-entropy is computed from logits.",
        topic="stability", level=3),
    tf("Computing `np.log(p)` for predicted probabilities can return `-inf` when a probability underflows to 0, which then turns the loss into inf or nan.", True,
       "What is log(0)?",
       "log(0) = -inf. That is why losses clip p to [eps, 1 - eps] or, better, compute log-softmax directly from logits.",
       topic="stability", level=3),
    out(C("""
        import numpy as np
        print(np.log(1 + 1e-20), np.log1p(1e-20))
        print(np.exp(1e-20) - 1, np.expm1(1e-20))
        """),
        ["0.0 1e-20\n0.0 1e-20", "1e-20 1e-20\n1e-20 1e-20", "0.0 0.0\n0.0 0.0", "1e-20 0.0\n1e-20 0.0"], 0,
        "1 + 1e-20 is exactly 1.0 in float64.",
        "The tiny value is lost when added to 1 before log is applied. log1p and expm1 compute log(1 + x) and exp(x) - 1 "
        "accurately for small x.",
        topic="stability", level=4),
    ask("What do the textbook variance formula and np.var give?", C("""
        import numpy as np
        x = 1e8 + np.array([1.0, 2.0, 3.0, 4.0])
        naive = (x ** 2).mean() - x.mean() ** 2
        print(naive, x.var())
        """),
        ["2.0 1.25", "1.25 1.25", "0.0 1.25", "-2.0 1.25"], 0,
        "E[x^2] - E[x]^2 subtracts two numbers around 1e16.",
        "The textbook formula suffers catastrophic cancellation: both terms are ~1e16, so their tiny difference is "
        "garbage. np.var subtracts the mean first (two-pass), giving the true 1.25.",
        topic="stability", level=4),
    ask("What do sum() and the running cumsum give in float32?", C("""
        import numpy as np
        a = np.ones(2**24 + 10, dtype=np.float32)
        print(a.sum(), a.cumsum()[-1])
        """),
        ["16777226.0 16777216.0", "16777226.0 16777226.0", "16777216.0 16777216.0", "16777216.0 16777226.0"], 0,
        "float32 cannot represent 2**24 + 1.",
        "A running float32 total gets stuck at 2**24 = 16777216, because adding 1 rounds back. np.sum uses pairwise "
        "summation (adds partial sums of similar size), so it stays exact. Accumulate in float64 when unsure.",
        topic="stability", level=4),
    out(C("""
        import numpy as np
        x = np.array([-1000.0, 0.0, 1000.0])
        with np.errstate(over="ignore", divide="ignore"):
            naive = np.log(1 / (1 + np.exp(-x)))
        stable = -np.logaddexp(0, -x)
        print(naive[0], stable[0], np.allclose(naive[1:], stable[1:]))
        """),
        ["-inf -1000.0 True", "-1000.0 -1000.0 True", "nan -1000.0 True", "-inf -inf True"], 0,
        "For x = -1000, exp(1000) overflows, so the sigmoid becomes exactly 0.",
        "log(sigmoid(x)) = -log(1 + e^-x) = -logaddexp(0, -x), which never forms the overflowing value. The naive "
        "form gives -inf at -1000 instead of the correct -1000. This is why frameworks offer 'with logits' losses.",
        topic="stability", level=4),
    mcq("A model trained in float16 suddenly shows `loss = nan`. Which is the most likely cause, and fix?",
        ["Values exceeded float16's max (~65504) or underflowed; use loss scaling / bfloat16 / keep reductions in float32",
         "float16 cannot represent negative numbers",
         "NaN means the learning rate is too small",
         "np.random was not seeded"], 0,
        "float16 has a tiny range.",
        "float16 overflows above 65504 to inf, and inf - inf or 0 * inf gives nan. Mixed-precision training keeps "
        "master weights and sums in float32, scales the loss, or uses bfloat16 (float32's range with fewer digits).",
        topic="stability", level=4),
    mcq("Why do numerically careful libraries compute the norm of a vector without simply doing `np.sqrt(np.sum(x**2))`?",
        ["x**2 can overflow (or underflow) even when the norm itself is representable, so they rescale by max|x| first",
         "np.sqrt is inaccurate",
         "Summation in NumPy is not deterministic",
         "Squaring is slower than taking absolute values"], 0,
        "Try x = 1e200.",
        "(1e200)**2 = inf in float64, yet the norm 1e200 is fine. Scaling by s = max|x| gives s * sqrt(sum((x/s)**2)), "
        "which never overflows (the idea behind hypot).",
        topic="stability", level=4),

    # ------------------------------------------------------------------ extra concept checks
    fill("Which argument of `sum`/`mean`/`max` keeps the reduced axis as size 1 so the result broadcasts back? `____=True`",
         "keepdims",
         "It 'keeps the dimensions'.",
         "keepdims=True turns a (n,) result into (n, 1) (or (1, d)), so X / X.sum(axis=1, keepdims=True) divides each row by its own total.",
         topic="aggregation", level=2),
    fill("Which function keeps values inside a range, e.g. `np.____(p, 1e-7, 1 - 1e-7)` before taking log(p)?", "clip",
         "Like a hair clip holding things in place.",
         "np.clip(x, lo, hi) replaces values below lo with lo and above hi with hi, preventing log(0) = -inf in a loss.",
         topic="compare-where", level=2),
    fill("Which linear-algebra function solves `A @ x = b` for x without computing an inverse? `np.linalg.____(A, b)`",
         "solve",
         "It does exactly what the name says.",
         "np.linalg.solve(A, b) factorises A and back-substitutes: faster and more accurate than inv(A) @ b.",
         topic="linalg", level=3),
    fill("Which Generator method returns a shuffled COPY of `np.arange(n)` (or of an array): `rng.____(n)`?", "permutation",
         "Not shuffle: that one works in place.",
         "rng.permutation(n) returns a new shuffled array; rng.shuffle(a) shuffles a in place and returns None.",
         topic="random", level=2),
    tf("Broadcasting works on any two shapes as long as they have the same total number of elements.", False,
       "The rule is about each axis, not the total.",
       "(2, 3) and (3, 2) both have 6 elements but don't broadcast (3 vs 2 on the last axis). (4, 1) and (3,) have "
       "different sizes but do broadcast, to (4, 3).",
       topic="broadcasting", level=2),
    tf("`a @ b` and `np.matmul(a, b)` are the same operation.", True,
       "@ is an operator that calls a function.",
       "The @ operator calls np.matmul (via __matmul__). np.dot is the one that differs for N-d inputs.",
       topic="linalg", level=2),
    tf("For an int64 array `a`, `a.mean()` returns a float64 even though every element is an integer.", True,
       "What is the mean of 1 and 2?",
       "mean always uses floating point for integer input, so the result is float64 (1.5 for [1, 2]).",
       topic="aggregation", level=1),
    tf("Python loops over NumPy arrays are faster than loops over Python lists, because the data is in an array.", False,
       "Each a[i] in a loop has to create something.",
       "Indexing a NumPy array element by element creates a new NumPy scalar object each time, which is often SLOWER "
       "than reading a list. NumPy is only fast when you hand it the whole array.",
       topic="vectorisation", level=2),
]
