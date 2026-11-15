from textwrap import dedent

from helpers import mcq, tf, out, fill


def C(s):
    return dedent(s).strip("\n")


def ask(question, code, options, correct, hint, explanation, **kw):
    """An mcq about a code snippet (the snippet is shown and must run)."""
    return mcq(question, options, correct, hint, explanation, code=code, **kw)


SUBJECT = "np-arrays"

TOPICS = [
    ("why-arrays", "Arrays vs Python lists"),
    ("creating", "Creating arrays"),
    ("attributes", "shape, ndim, size, dtype, itemsize, nbytes"),
    ("dtypes", "dtypes, casting and upcasting"),
    ("indexing", "Indexing and slicing (1D, 2D, 3D)"),
    ("masks-fancy", "Boolean masks and fancy indexing"),
    ("views-copies", "Views vs copies"),
    ("reshaping", "Reshape, transpose, newaxis, squeeze"),
    ("stack-split", "Stacking and splitting"),
    ("memory-layout", "Memory layout: C/F order, strides, contiguity"),
    ("special-values", "NaN, inf and structured arrays"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ why-arrays
    mcq("What is the main reason ML code stores numbers in a NumPy array instead of a Python list?",
        ["Maths on the whole array runs in fast compiled code, with no Python loop",
         "Arrays can hold any mix of types, lists cannot",
         "Arrays are the only way to store more than 1000 items",
         "Lists cannot hold decimal numbers"], 0,
        "Think about who does the looping: Python or C.",
        "An array is one block of same-typed numbers, so NumPy can loop over it in compiled C. "
        "Lists can hold anything, which is exactly why they are slow for maths.",
        analogy="A list is a drawer of labelled boxes you open one by one; an array is a single "
                "spreadsheet column you can apply a formula to in one go.",
        topic="why-arrays", level=1),
    out(C("""
        import numpy as np
        lst = [1, 2, 3]
        arr = np.array([1, 2, 3])
        print(lst * 2)
        print(arr * 2)
        """),
        ["[1, 2, 3, 1, 2, 3]\n[2 4 6]", "[2, 4, 6]\n[2 4 6]",
         "[1, 2, 3, 1, 2, 3]\n[1 2 3 1 2 3]", "[2 4 6]\n[2, 4, 6]"], 0,
        "* means something different for a list.",
        "For a list, * 2 repeats the list. For an array, * 2 multiplies every element. "
        "Note arrays print without commas.",
        topic="why-arrays", level=1),
    tf("Every element of a NumPy array has the same data type (dtype).", True,
       "One array, one ...?",
       "An array has a single dtype for all elements. That uniformity is what lets NumPy store "
       "them packed together and process them fast.",
       topic="why-arrays", level=1),
    out(C("""
        import numpy as np
        print([1, 2] + [3, 4])
        print(np.array([1, 2]) + np.array([3, 4]))
        """),
        ["[1, 2, 3, 4]\n[4 6]", "[4, 6]\n[4 6]", "[1, 2, 3, 4]\n[1 2 3 4]", "[4 6]\n[1 2 3 4]"], 0,
        "List + list joins; array + array ...?",
        "List + list concatenates. Array + array adds element by element.",
        topic="why-arrays", level=1),
    out(C("""
        import numpy as np
        a = np.array([1, 2.5, 3])
        print(a)
        """),
        ["[1.  2.5 3. ]", "[1 2.5 3]", "[1, 2.5, 3]", "[1 2 3]"], 0,
        "One int and one float in the same array: everything must share a type.",
        "The ints are upcast to float64 so they match 2.5. NumPy pads printed floats to line up, "
        "hence '1. ' and '3. '.",
        topic="why-arrays", level=2),
    mcq("You store one million int64 numbers. Roughly how much memory does the NumPy array need, "
        "versus a Python list of the same numbers?",
        ["About 8 MB for the array; the list needs about 8 MB of pointers PLUS a separate int object per number",
         "Both need exactly 8 MB",
         "The list is smaller because Python compresses ints",
         "The array needs 28 MB, the list 8 MB"], 0,
        "int64 = 8 bytes. What does a list actually hold?",
        "The array is one raw buffer of 8-byte values. A list holds 8-byte pointers to full Python int "
        "objects (about 28 bytes each), so it uses several times more memory.",
        diagram="""
array:  | 1 | 2 | 3 | 4 |   raw 8-byte values, side by side
list:   | * | * | * | * |   pointers...
          |   |   |   |
         int int int int    ...to separate Python objects
""",
        topic="why-arrays", level=2),
    mcq("Why is `arr.sum()` on a big array much faster than `sum(lst)` on a list of the same numbers?",
        ["The array is a contiguous typed buffer summed in a C loop; the list loop unboxes a Python object at each step",
         "NumPy uses the GPU by default",
         "Python's sum() is written in Python",
         "NumPy caches the sum when the array is created"], 0,
        "What does each step of the list loop have to do?",
        "For a list, every step must follow a pointer, check the object's type and unbox the value. "
        "NumPy knows the dtype once and runs a tight C loop over packed memory (cache-friendly, SIMD).",
        topic="why-arrays", level=3),
    out(C("""
        import numpy as np
        a = np.array([1, "a"])
        print(a.dtype)
        print(a[0] + a[0])
        """),
        ["<U21\n11", "object\n2", "int64\n2", "<U1\n11"], 0,
        "Mixing a number and a string: what single type can hold both?",
        "NumPy converts everything to a fixed-width unicode string (<U21, wide enough for any int64). "
        "So a[0] is the string '1' and '1' + '1' is '11'.",
        topic="why-arrays", level=3),
    mcq("`np.array([1, None, 3])` creates an array of dtype `object`. What does that mean for performance?",
        ["It stores Python object pointers, so most operations fall back to slow per-element Python calls",
         "It is just as fast as int64 because NumPy ignores None",
         "It raises an error, NumPy arrays cannot contain None",
         "It is converted to float64 with NaN automatically"], 0,
        "An object array is basically a list in disguise.",
        "dtype=object arrays hold pointers to Python objects. You lose the packed buffer and the C loops; "
        "maths calls each object's Python method. Use float with np.nan for missing numbers instead.",
        topic="why-arrays", level=4),

    # ------------------------------------------------------------------ creating
    out(C("""
        import numpy as np
        print(np.arange(5))
        """),
        ["[0 1 2 3 4]", "[1 2 3 4 5]", "[0 1 2 3 4 5]", "[0, 1, 2, 3, 4]"], 0,
        "Like Python's range(): the stop value is excluded.",
        "np.arange(5) works like range(5): it starts at 0 and stops before 5.",
        topic="creating", level=1),
    out(C("""
        import numpy as np
        print(np.ones(3))
        """),
        ["[1. 1. 1.]", "[1 1 1]", "[1, 1, 1]", "[[1. 1. 1.]]"], 0,
        "What is the default dtype of np.ones?",
        "np.zeros and np.ones default to float64, which prints as '1.' (the dot means float).",
        topic="creating", level=1),
    fill("Complete the call to make a 3x3 array full of zeros: `np.____((3, 3))`", "zeros",
         "The name says what is inside.",
         "np.zeros((3, 3)) makes a 3x3 float array of 0.0. The shape goes in as one tuple.",
         topic="creating", level=1),
    out(C("""
        import numpy as np
        a = np.zeros(2, 3)
        print(a.shape)
        """),
        ["TypeError", "(2, 3)", "(2,)", "(3, 2)"], 0,
        "What is the SECOND positional parameter of np.zeros?",
        "np.zeros(shape, dtype). Here 3 is taken as the dtype and is not a valid one, so TypeError. "
        "Write np.zeros((2, 3)) with the shape as one tuple.",
        topic="creating", level=1),
    mcq("What does `np.linspace(0, 1, 5)` return?",
        ["[0.   0.25 0.5  0.75 1.  ]  (5 evenly spaced points, end included)",
         "[0.  0.2 0.4 0.6 0.8]  (step 0.2, end excluded)",
         "[0 1 2 3 4]",
         "[0.   0.25 0.5  0.75]  (4 points)"], 0,
        "linspace asks for HOW MANY points, not the step size.",
        "linspace(start, stop, num) gives num points evenly spaced, and includes stop by default. "
        "5 points from 0 to 1 means a gap of 0.25.",
        topic="creating", level=1),
    out(C("""
        import numpy as np
        print(np.arange(0, 1, 0.25))
        """),
        ["[0.   0.25 0.5  0.75]", "[0.   0.25 0.5  0.75 1.  ]", "[0 0 0 0]", "[0.25 0.5  0.75 1.  ]"], 0,
        "arange takes a STEP and excludes the stop.",
        "arange(start, stop, step) steps by 0.25 and stops before 1. Use linspace when you need the end point included.",
        topic="creating", level=2),
    out(C("""
        import numpy as np
        print(np.full((2, 2), 7))
        """),
        ["[[7 7]\n [7 7]]", "[[7. 7.]\n [7. 7.]]", "[7 7 7 7]", "[[7, 7], [7, 7]]"], 0,
        "np.full takes its dtype from the fill value.",
        "np.full(shape, value) fills the shape with value. 7 is an int, so the array is int.",
        topic="creating", level=2),
    out(C("""
        import numpy as np
        print(np.eye(2))
        """),
        ["[[1. 0.]\n [0. 1.]]", "[[1 0]\n [0 1]]", "[[1. 1.]\n [1. 1.]]", "[1. 1.]"], 0,
        "eye = 'I', the identity matrix.",
        "np.eye(n) is the n x n identity matrix: ones on the diagonal, zeros elsewhere, float by default.",
        topic="creating", level=2),
    mcq("What is inside `np.empty((2, 3))` right after you create it?",
        ["Whatever bytes were already in that memory: arbitrary values",
         "All zeros, guaranteed",
         "All NaN",
         "Nothing: it has shape (0,)"], 0,
        "'empty' skips a step to save time.",
        "np.empty allocates memory without clearing it, so the values are leftovers. Only use it when "
        "you will overwrite every element anyway.",
        analogy="Like malloc in C versus calloc: you get the memory, not a clean slate.",
        topic="creating", level=2),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        a = rng.integers(0, 10, size=3)
        rng2 = np.random.default_rng(0)
        b = rng2.integers(0, 10, size=3)
        print((a == b).all(), a.shape)
        """),
        ["True (3,)", "False (3,)", "True (1, 3)", "False (3, 1)"], 0,
        "Same seed, same generator recipe.",
        "Two generators built with the same seed produce the same sequence, so a and b are identical. "
        "size=3 gives shape (3,).",
        topic="creating", level=2),
    fill("Which NumPy function gives `num` evenly spaced values between start and stop, including stop by default?",
         "linspace",
         "Think 'linear space'.",
         "np.linspace(start, stop, num). Its partner np.arange takes a step instead and excludes stop.",
         topic="creating", level=2),
    out(C("""
        import numpy as np
        print(np.linspace(0, 1, 5, endpoint=False))
        """),
        ["[0.  0.2 0.4 0.6 0.8]", "[0.   0.25 0.5  0.75 1.  ]", "[0.   0.25 0.5  0.75]", "[0.2 0.4 0.6 0.8 1. ]"], 0,
        "Without the end point, the interval is split into 5 equal steps.",
        "endpoint=False splits [0, 1) into 5 steps of 0.2 and drops the 1.0.",
        topic="creating", level=2),
    out(C("""
        import numpy as np
        a = np.arange(1, 1.3, 0.1)
        print(len(a))
        """),
        ["4", "3", "2", "ValueError"], 0,
        "0.1 is not exactly representable in binary.",
        "arange computes the length as ceil((1.3 - 1) / 0.1), and (1.3 - 1) / 0.1 is 3.0000000000000004, "
        "so it rounds up to 4 and includes ~1.3. Float steps in arange are risky; use linspace.",
        topic="creating", level=3),
    ask("What does z hold after the assignment?", C("""
        import numpy as np
        a = np.array([1, 2, 3])
        z = np.zeros_like(a)
        z[0] = 2.9
        print(z)
        """),
        ["[2 0 0]", "[2.9 0.  0. ]", "[3 0 0]", "[0. 0. 0.]"], 0,
        "zeros_like copies the shape AND the dtype.",
        "zeros_like(a) makes an int64 array because a is int64. Assigning 2.9 truncates to 2.",
        topic="creating", level=3),
    out(C("""
        import numpy as np
        print(np.full(3, 2.7, dtype=int))
        """),
        ["[2 2 2]", "[3 3 3]", "[2.7 2.7 2.7]", "TypeError"], 0,
        "Converting float to int in NumPy truncates.",
        "The explicit dtype wins: 2.7 is cast to int, which truncates toward zero to 2.",
        topic="creating", level=3),
    tf("Calling `np.random.seed(42)` also fixes the output of a generator made with `np.random.default_rng()`.", False,
       "Global state versus a generator object.",
       "np.random.seed only seeds the old global RandomState. A Generator from default_rng() has its own state; "
       "seed it directly: default_rng(42).",
       topic="creating", level=3),
    mcq("Why is `rng = np.random.default_rng(seed)` passed around in modern code instead of calling `np.random.rand()`?",
        ["Each generator owns its state, so components don't silently share or reset one global random stream",
         "np.random.rand() was removed in NumPy 2",
         "default_rng is always cryptographically secure",
         "Generators are faster only on GPU"], 0,
        "Think about global mutable state in a big codebase.",
        "The legacy functions share one hidden global state: any library that reseeds it changes your results. "
        "A Generator is an explicit object (dependency injection for randomness) and uses the better PCG64 algorithm.",
        analogy="Global random state is like a global mutable singleton; a Generator is an injected dependency.",
        topic="creating", level=4),

    # ------------------------------------------------------------------ attributes
    out(C("""
        import numpy as np
        a = np.array([[1, 2, 3], [4, 5, 6]])
        print(a.size)
        """),
        ["6", "2", "3", "(2, 3)"], 0,
        "size counts elements, not rows.",
        "size is the total number of elements: 2 rows x 3 columns = 6.",
        topic="attributes", level=1),
    mcq("An array has shape `(2, 3, 4)`. What is its `ndim`?",
        ["3", "24", "4", "2"], 0,
        "ndim = number of axes = length of the shape tuple.",
        "ndim counts how many numbers are in the shape: (2, 3, 4) has 3 axes. 24 would be the size.",
        topic="attributes", level=1),
    ask("What is the shape of np.zeros(5)?", C("""
        import numpy as np
        print(np.zeros(5).shape)
        """),
        ["(5,)", "(5)", "5", "(1, 5)"], 0,
        "A 1D shape is still a tuple.",
        "Shapes are always tuples. A one-element tuple is written (5,) with a trailing comma.",
        topic="attributes", level=1),
    out(C("""
        import numpy as np
        a = np.zeros((3, 4), dtype=np.float32)
        print(a.itemsize, a.nbytes)
        """),
        ["4 48", "8 96", "4 12", "32 384"], 0,
        "float32 = 32 bits.",
        "float32 is 32 bits = 4 bytes per item. nbytes = size * itemsize = 12 * 4 = 48.",
        topic="attributes", level=2),
    ask("What does len() return for this 2D array?", C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        print(len(a))
        """),
        ["2", "6", "3", "(2, 3)"], 0,
        "len() only looks at the first axis.",
        "len(a) is the length of axis 0, here the number of rows (2). Use a.size for all elements.",
        topic="attributes", level=2),
    tf("An array of shape `(5,)` and an array of shape `(5, 1)` are the same thing.", False,
       "Count the axes.",
       "(5,) is 1D (a flat vector). (5, 1) is 2D (a column of 5 rows). They behave very differently in "
       "broadcasting and matrix maths.",
       diagram="""
(5,)    [a b c d e]        1 axis

(5, 1)  [[a]               2 axes
         [b]
         [c] ...]
""",
       topic="attributes", level=2),
    ask("What are the shape, ndim and size of this 0-d array?", C("""
        import numpy as np
        s = np.array(5)
        print(s.shape, s.ndim, s.size)
        """),
        ["() 0 1", "(1,) 1 1", "(5,) 1 5", "() 1 1"], 0,
        "A single number wrapped in an array has no axes.",
        "np.array(5) is a 0-d array: shape () (empty tuple), ndim 0, but it still holds 1 element.",
        topic="attributes", level=3),
    mcq("For a 1,000 x 1,000 float64 array `a`, which is closest to `a.nbytes`?",
        ["8,000,000 (8 MB)", "1,000,000 (1 MB)", "64,000,000 (64 MB)", "8,000 (8 KB)"], 0,
        "float64 = 8 bytes; how many elements?",
        "1e6 elements x 8 bytes = 8e6 bytes. Quick estimates like this matter when you decide whether data fits in RAM.",
        topic="attributes", level=3),
    out(C("""
        import numpy as np
        a = np.zeros((0, 3))
        print(a.size, a.shape, a.sum())
        """),
        ["0 (0, 3) 0.0", "3 (0, 3) 0.0", "0 (3,) nan", "ValueError"], 0,
        "Zero rows is a legal shape.",
        "Empty arrays are valid: size is 0 * 3 = 0 and the sum of nothing is the identity of +, which is 0.0.",
        topic="attributes", level=4),
    out(C("""
        import numpy as np
        a = np.arange(10)
        b = a[::2]
        print(b.nbytes, b.base.nbytes)
        """),
        ["40 80", "80 80", "40 40", "80 40"], 0,
        "nbytes is size * itemsize of THIS array, not the memory it lives in.",
        "b has 5 int64 elements, so b.nbytes = 40, even though it is a view into a's 80-byte buffer. "
        "nbytes does not tell you how much memory a view keeps alive.",
        topic="attributes", level=4),

    # ------------------------------------------------------------------ dtypes
    out(C("""
        import numpy as np
        print(np.array([1, 2, 3]).dtype)
        print(np.array([1.0, 2, 3]).dtype)
        """),
        ["int64\nfloat64", "int32\nfloat32", "int\nfloat", "int64\nint64"], 0,
        "One decimal point changes everything.",
        "Whole numbers default to int64 (NumPy 2, on every platform). A single float makes the whole array float64.",
        topic="dtypes", level=1),
    ask("What does the int array hold after assigning 9.7?", C("""
        import numpy as np
        a = np.array([1, 2, 3])
        a[0] = 9.7
        print(a)
        """),
        ["[9 2 3]", "[9.7 2.  3. ]", "[10  2  3]", "TypeError"], 0,
        "Assigning into an array never changes its dtype.",
        "a stays int64, so 9.7 is truncated to 9. The array does not 'upgrade' itself to float.",
        topic="dtypes", level=2),
    out(C("""
        import numpy as np
        a = np.array([1.7, -1.7])
        print(a.astype(int))
        """),
        ["[ 1 -1]", "[ 2 -2]", "[ 1 -2]", "[2 -1]"], 0,
        "Truncation goes toward zero, not down.",
        "astype(int) truncates toward zero: 1.7 -> 1 and -1.7 -> -1. Use np.round or np.floor first if you need those.",
        topic="dtypes", level=2),
    ask("What dtype does int array + float array produce?", C("""
        import numpy as np
        a = np.array([1, 2]) + np.array([0.5, 0.5])
        print(a.dtype)
        """),
        ["float64", "int64", "float32", "object"], 0,
        "Upcasting picks a type that can hold both.",
        "int64 + float64 upcasts to float64 so no fractional part is lost.",
        topic="dtypes", level=2),
    out(C("""
        import numpy as np
        a = np.array([True, False, True])
        print(a + 1)
        print(a.sum())
        """),
        ["[2 1 2]\n2", "[True True True]\n2", "[2 1 2]\nTrue", "TypeError"], 0,
        "True behaves like 1 in arithmetic.",
        "Booleans upcast to int in arithmetic: True=1, False=0. That is why mask.sum() counts the True values.",
        topic="dtypes", level=2),
    out(C("""
        import numpy as np
        a = np.array([1.0, 2.0], dtype=np.float32)
        print((a + 1.0).dtype)
        print((a + np.array([1.0])).dtype)
        """),
        ["float32\nfloat64", "float64\nfloat64", "float32\nfloat32", "float64\nfloat32"], 0,
        "A plain Python number is treated as 'weak'.",
        "NumPy 2 (NEP 50): a Python scalar adapts to the array's dtype, so float32 stays float32. "
        "A float64 ARRAY is a real dtype and wins, so the result is float64.",
        topic="dtypes", level=3),
    ask("Which dtypes do the two mixed-type additions produce?", C("""
        import numpy as np
        a = np.array([1, 2], dtype=np.int8)
        b = np.array([1, 2], dtype=np.int16)
        c = np.array([1, 2], dtype=np.uint8)
        print((a + b).dtype, (a + c).dtype)
        """),
        ["int16 int16", "int16 int8", "int8 uint8", "int64 int64"], 0,
        "Find the smallest type that can hold every value of both inputs.",
        "int8 + int16 -> int16. int8 (-128..127) + uint8 (0..255) needs negatives and 255, so -> int16.",
        topic="dtypes", level=3),
    out(C("""
        import numpy as np
        a = np.array([1, 2], dtype=np.int8)
        print((a + 1).dtype)
        print(a + 300)
        """),
        ["int8\nOverflowError", "int64\n[301 302]", "int8\n[45 46]", "int16\n[301 302]"], 0,
        "NumPy 2 keeps the array's dtype for a Python int, then checks it fits.",
        "Under NEP 50 the Python int adopts int8. 1 fits, so the result is int8. 300 does not fit in int8, "
        "so NumPy 2 raises OverflowError instead of silently upcasting (old NumPy 1 gave int16).",
        topic="dtypes", level=3),
    tf("`a.astype(np.float32)` returns a new array even if `a` is already float32.", True,
       "Check the default of the copy argument.",
       "astype has copy=True by default, so it always allocates. Pass copy=False to reuse a when no conversion is needed.",
       topic="dtypes", level=3),
    out(C("""
        import numpy as np
        a = np.array([-1, 256, 300])
        print(a.astype(np.uint8))
        """),
        ["[255   0  44]", "[  0 255 255]", "OverflowError", "[-1 256 300]"], 0,
        "astype on arrays does not check ranges; it keeps the low 8 bits.",
        "Integer astype wraps modulo 2**8: -1 -> 255, 256 -> 0, 300 -> 44. No error, no warning: a classic "
        "image-processing bug.",
        topic="dtypes", level=4),
    out(C("""
        import numpy as np
        print(np.float32(0.1) == 0.1)
        print(np.float32(0.1) == np.float64(0.1))
        """),
        ["True\nFalse", "False\nFalse", "True\nTrue", "False\nTrue"], 0,
        "In NumPy 2 a plain Python float takes on the dtype of the NumPy value it meets.",
        "Line 1: the Python float 0.1 is 'weak' (NEP 50), so it is converted to float32 first and the two match. "
        "Line 2: both are real dtypes, so float32 is upcast to float64; 0.1 rounded to float32 is not the float64 0.1.",
        topic="dtypes", level=4),
    out(C("""
        import numpy as np
        print(np.can_cast(np.int64, np.float64))
        print(int(np.float64(2**53 + 1)) == 2**53 + 1)
        """),
        ["True\nFalse", "False\nFalse", "True\nTrue", "False\nTrue"], 0,
        "float64 has a 53-bit mantissa.",
        "NumPy calls int64 -> float64 a 'safe' cast, yet integers above 2**53 lose precision. "
        "'Safe' means the kind is preserved, not that every value survives.",
        topic="dtypes", level=4),

    # ------------------------------------------------------------------ indexing
    out(C("""
        import numpy as np
        a = np.array([10, 20, 30, 40])
        print(a[1], a[-1])
        """),
        ["20 40", "10 40", "20 30", "10 30"], 0,
        "Indexing starts at 0; -1 is the last one.",
        "a[1] is the second element (20) and a[-1] counts from the end (40), just like Python lists.",
        topic="indexing", level=1),
    out(C("""
        import numpy as np
        a = np.array([10, 20, 30, 40])
        print(a[1:3])
        """),
        ["[20 30]", "[20 30 40]", "[10 20 30]", "[10 20]"], 0,
        "Slices include the start and exclude the stop.",
        "a[1:3] takes indexes 1 and 2: [20 30].",
        topic="indexing", level=1),
    mcq("In a 2D array `a`, what does `a[1, 2]` select?",
        ["The element in row 1, column 2", "Rows 1 and 2", "The element in row 2, column 1", "Columns 1 to 2"], 0,
        "The first number is always the row (axis 0).",
        "a[row, col]. With 0-based indexing, a[1, 2] is the second row, third column.",
        diagram="""
         col0 col1 col2
row0  [[  0    1    2 ]
row1   [  3    4   (5)]]   a[1, 2] = 5
""",
        topic="indexing", level=1),
    out(C("""
        import numpy as np
        a = np.arange(12).reshape(3, 4)
        print(a[:, 1])
        """),
        ["[1 5 9]", "[4 5 6 7]", "[[1]\n [5]\n [9]]", "[1 2 3]"], 0,
        "':' means 'all rows'.",
        "a[:, 1] takes column 1 from every row. The result is 1D.",
        diagram="""
[[ 0  1  2  3]
 [ 4  5  6  7]      a[:, 1] -> [1 5 9]
 [ 8  9 10 11]]
     ^
""",
        topic="indexing", level=2),
    ask("What shapes do an integer index and a length-1 slice produce?", C("""
        import numpy as np
        a = np.arange(12).reshape(3, 4)
        print(a[:, 1].shape, a[:, 1:2].shape)
        """),
        ["(3,) (3, 1)", "(3, 1) (3, 1)", "(3,) (3,)", "(1, 3) (3, 1)"], 0,
        "An integer index removes an axis; a slice keeps it.",
        "a[:, 1] drops the column axis (1D). a[:, 1:2] is a slice of length 1, so the axis stays: a column vector.",
        topic="indexing", level=2),
    out(C("""
        import numpy as np
        a = np.arange(6)
        print(a[::-1])
        print(a[::2])
        """),
        ["[5 4 3 2 1 0]\n[0 2 4]", "[5 4 3 2 1 0]\n[1 3 5]", "[0 1 2 3 4 5]\n[0 2 4]", "[5 4 3 2 1]\n[0 2 4]"], 0,
        "The third slice number is the step.",
        "A step of -1 walks backwards over everything; a step of 2 takes every second element from 0.",
        topic="indexing", level=2),
    tf("For a NumPy 2D array, `a[0][1]` and `a[0, 1]` give the same element.", True,
       "a[0] is itself an array.",
       "Both give the same value. a[0, 1] is preferred: it is one indexing operation instead of two and it "
       "is the only form that works with slices like a[:, 1].",
       topic="indexing", level=2),
    out(C("""
        import numpy as np
        a = np.arange(24).reshape(2, 3, 4)
        print(a[1, 2, 3], a[:, 0, 0])
        """),
        ["23 [ 0 12]", "23 [0 4]", "11 [ 0 12]", "IndexError"], 0,
        "Shape (2, 3, 4) = 2 blocks of 3 rows of 4 columns.",
        "a[1, 2, 3] is the last element (23). a[:, 0, 0] takes the first element of each block: 0 and 12.",
        diagram="""
block 0          block 1
[[ 0  1  2  3]   [[12 13 14 15]
 [ 4  5  6  7]    [16 17 18 19]
 [ 8  9 10 11]]   [20 21 22 23]]
""",
        topic="indexing", level=3),
    ask("What shapes do these Ellipsis indexes give?", C("""
        import numpy as np
        a = np.zeros((2, 3, 4))
        print(a[..., 0].shape, a[0, ...].shape)
        """),
        ["(2, 3) (3, 4)", "(2, 3, 1) (1, 3, 4)", "(4,) (2,)", "(2, 3) (2, 3)"], 0,
        "... stands for 'as many : as needed'.",
        "a[..., 0] = a[:, :, 0] (shape (2, 3)); a[0, ...] = a[0, :, :] (shape (3, 4)). "
        "Ellipsis is handy for code that works on any number of batch dimensions.",
        topic="indexing", level=3),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        print(a[2:100])
        print(a[10])
        """),
        ["[3 4]\nIndexError", "IndexError", "[3 4]\n4", "[3 4 0 0]\nIndexError"], 0,
        "Slices are forgiving; single indexes are not.",
        "Slices clip to the valid range, so a[2:100] is [3 4]. A single index past the end raises IndexError.",
        topic="indexing", level=3),
    out(C("""
        import numpy as np
        a = np.arange(10)
        print(a[-1:-4:-1], a[7:2:-2])
        """),
        ["[9 8 7] [7 5 3]", "[9 8 7 6] [7 5 3]", "[] [7 5 3]", "[9 8 7] [7 5]"], 0,
        "With a negative step the slice runs from start DOWN to (but not including) stop.",
        "a[-1:-4:-1] takes indexes 9, 8, 7 (stops before -4 = 6). a[7:2:-2] takes 7, 5, 3 (stops before 2).",
        topic="indexing", level=4),

    # ------------------------------------------------------------------ masks-fancy
    out(C("""
        import numpy as np
        a = np.array([3, 8, 1, 9])
        print(a > 4)
        """),
        ["[False  True False  True]", "[8 9]", "[0 1 0 1]", "True"], 0,
        "Comparison on an array is done element by element.",
        "a > 4 gives a boolean array of the same shape: a 'mask'. (NumPy pads False/True to line up.)",
        topic="masks-fancy", level=1),
    out(C("""
        import numpy as np
        a = np.array([3, 8, 1, 9])
        print(a[a > 4])
        """),
        ["[8 9]", "[False  True False  True]", "[1 3]", "[0 8 0 9]"], 0,
        "A mask inside [] keeps the True positions.",
        "a[mask] keeps only the elements where the mask is True. This is how you filter rows in ML code.",
        analogy="Like SQL: SELECT value FROM a WHERE value > 4.",
        topic="masks-fancy", level=1),
    out(C("""
        import numpy as np
        a = np.array([3, 8, 1, 9])
        print(a[(a > 2) & (a < 9)])
        """),
        ["[3 8]", "[3 8 9]", "[8]", "ValueError"], 0,
        "& is element-wise AND.",
        "Use & (and), | (or), ~ (not) on masks, with brackets around each comparison because & binds tighter than >.",
        topic="masks-fancy", level=2),
    out(C("""
        import numpy as np
        a = np.array([3, 8, 1, 9])
        print(a[(a > 2) and (a < 9)])
        """),
        ["ValueError", "[3 8]", "[8 9]", "TypeError"], 0,
        "Python's `and` wants ONE True/False.",
        "`and` calls bool() on the whole array, which is ambiguous for more than one element: "
        "ValueError 'The truth value of an array ... is ambiguous'. Use & instead.",
        topic="masks-fancy", level=2),
    ask("Which elements does the index list pick?", C("""
        import numpy as np
        a = np.array([3, 8, 1, 9])
        print(a[[0, 2, 0]])
        """),
        ["[3 1 3]", "[3 1]", "[3 8 1]", "IndexError"], 0,
        "A list of indexes picks those positions, repeats allowed.",
        "Fancy indexing with a list returns the elements at those positions, in that order, repeats included.",
        topic="masks-fancy", level=2),
    ask("What is `a` after the masked assignment?", C("""
        import numpy as np
        a = np.array([3, -8, 1, -9])
        a[a < 0] = 0
        print(a)
        """),
        ["[3 0 1 0]", "[3 1]", "[0 -8 0 -9]", "[3 -8 1 -9]"], 0,
        "Masks work on the left side of = too.",
        "Assigning through a mask writes into the original array. This is how you clip negatives (ReLU by hand).",
        topic="masks-fancy", level=2),
    fill("Complete to count how many values are above 4: `(a > 4).____()`", "sum",
         "True counts as 1.",
         "(a > 4).sum() adds up the booleans, so it counts the Trues. np.count_nonzero(a > 4) does the same.",
         topic="masks-fancy", level=2),
    out(C("""
        import numpy as np
        a = np.arange(9).reshape(3, 3)
        print(a[[0, 2], [1, 2]])
        """),
        ["[1 8]", "[[1 2]\n [7 8]]", "[0 1 2 6 7 8]", "[1 2 7 8]"], 0,
        "Two index lists are paired up element by element.",
        "a[[0, 2], [1, 2]] picks (0, 1) and (2, 2): values 1 and 8. To get the 2x2 sub-grid use a[np.ix_([0, 2], [1, 2])].",
        diagram="""
[[0 (1) 2]       pairs: (0,1) -> 1
 [3  4  5]              (2,2) -> 8
 [6  7 (8)]]
""",
        topic="masks-fancy", level=3),
    ask("What shape does a boolean mask over a 2D array return?", C("""
        import numpy as np
        a = np.arange(12).reshape(3, 4)
        r = a[a % 2 == 0]
        print(r.shape)
        """),
        ["(6,)", "(3, 2)", "(3, 4)", "(2, 3)"], 0,
        "Each row could keep a different number of elements.",
        "A boolean mask over a 2D array returns a flat 1D array of the selected elements, because the "
        "result cannot be guaranteed to be rectangular.",
        topic="masks-fancy", level=3),
    out(C("""
        import numpy as np
        X = np.arange(12).reshape(4, 3)
        y = np.array([0, 1, 0, 1])
        print(X[y == 1])
        """),
        ["[[ 3  4  5]\n [ 9 10 11]]", "[ 3  4  5  9 10 11]", "[[0 1 2]\n [6 7 8]]", "IndexError"], 0,
        "A 1D mask of length 4 applies to the rows.",
        "A 1D boolean mask on axis 0 selects whole rows, keeping the 2D shape. This is the everyday "
        "'take the samples of class 1' idiom.",
        topic="masks-fancy", level=3),
    out(C("""
        import numpy as np
        a = np.zeros(3)
        a[[0, 0, 1]] += 1
        print(a)
        b = np.zeros(3)
        np.add.at(b, [0, 0, 1], 1)
        print(b)
        """),
        ["[1. 1. 0.]\n[2. 1. 0.]", "[2. 1. 0.]\n[2. 1. 0.]", "[1. 1. 0.]\n[1. 1. 0.]", "[2. 1. 0.]\n[1. 1. 0.]"], 0,
        "a[idx] += 1 is really a[idx] = a[idx] + 1.",
        "The fancy += reads a[[0,0,1]] once, adds 1, then writes back, so index 0 is written twice with the "
        "same value 1. np.add.at is 'unbuffered' and really accumulates. Matters for histograms and embedding gradients.",
        topic="masks-fancy", level=4),
    out(C("""
        import numpy as np
        a = np.arange(24).reshape(2, 3, 4)
        print(a[:, [0, 1], [0, 1]].shape)
        print(a[0, :, [0, 1]].shape)
        """),
        ["(2, 2)\n(2, 3)", "(2, 2)\n(3, 2)", "(2, 2, 2)\n(3, 2)", "(2, 2)\n(2, 2)"], 0,
        "When advanced indexes are separated by a slice, NumPy puts their dimension first.",
        "Case 1: the two lists are adjacent, so their broadcast dim (2) replaces axes 1-2 in place: (2, 2). "
        "Case 2: the scalar 0 and list [0, 1] are both advanced but split by ':', so the advanced dim goes "
        "first: (2, 3), not (3, 2).",
        topic="masks-fancy", level=4),

    # ------------------------------------------------------------------ views-copies
    tf("Changing an element of a slice like `b = a[1:3]` also changes `a`.", True,
       "A slice is a window, not a photocopy.",
       "Basic slicing returns a view: b looks at a's memory. Write to b and a changes. Use .copy() if you want independence.",
       analogy="A view is like a reference to the same object in JS or Java, not a clone.",
       topic="views-copies", level=1),
    ask("What is `a` after writing through the slice?", C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        b = a[1:3]
        b[0] = 99
        print(a)
        """),
        ["[ 1 99  3  4]", "[1 2 3 4]", "[99  2  3  4]", "[ 1 99 99  4]"], 0,
        "b is a view of a.",
        "b[0] is a[1], so the 99 shows up in a.",
        topic="views-copies", level=2),
    ask("What is `a` after writing through the list-indexed result?", C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        b = a[[1, 2]]
        b[0] = 99
        print(a)
        """),
        ["[1 2 3 4]", "[ 1 99  3  4]", "[99  2  3  4]", "IndexError"], 0,
        "Indexing with a list is 'fancy' indexing.",
        "Fancy indexing (lists or masks) always returns a copy, so changing b leaves a alone.",
        topic="views-copies", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = a.copy()
        b[0] = 50
        c = a
        c[1] = 60
        print(a)
        """),
        ["[ 1 60  3]", "[50 60  3]", "[1 2 3]", "[50  2  3]"], 0,
        "Plain = does not copy anything.",
        "b is a real copy, so 50 does not affect a. c = a just makes another name for the same array, so 60 does.",
        topic="views-copies", level=2),
    out(C("""
        import numpy as np
        a = np.arange(6)
        print(np.shares_memory(a, a[::2]), np.shares_memory(a, a[[0, 2, 4]]))
        """),
        ["True False", "True True", "False False", "False True"], 0,
        "One of these can be described with a step; the other is an arbitrary list.",
        "a[::2] is a view (same buffer, bigger stride). a[[0, 2, 4]] is fancy indexing, so it is a fresh copy, "
        "even though it holds the same values.",
        topic="views-copies", level=3),
    ask("What do the two `.base` checks report?", C("""
        import numpy as np
        a = np.arange(6)
        b = a.reshape(2, 3)
        print(b.base is a, a.base is None)
        """),
        ["True True", "False True", "True False", "False False"], 0,
        ".base points at the array that owns the memory.",
        "reshape of a contiguous array is a view, so b.base is a. a owns its data, so a.base is None.",
        topic="views-copies", level=3),
    out(C("""
        import numpy as np
        a = np.zeros((2, 3))
        col = a[:, 0]
        col += 1
        col = col + 1
        print(a[:, 0])
        """),
        ["[1. 1.]", "[2. 2.]", "[0. 0.]", "[1. 2.]"], 0,
        "One of these lines writes into memory; the other makes a new array.",
        "col += 1 is in-place on the view, so a changes. col = col + 1 builds a NEW array and rebinds the name; "
        "a is not touched by that second line.",
        topic="views-copies", level=3),
    ask("Which call returns the very same object, and which makes a new one?", C("""
        import numpy as np
        lst = [1, 2, 3]
        a = np.array([1, 2, 3])
        b = np.asarray(a)
        c = np.array(a)
        print(b is a, c is a)
        """),
        ["True False", "False False", "True True", "False True"], 0,
        "One of these copies by default.",
        "np.asarray returns its input unchanged if it is already a matching array. np.array copies by default.",
        topic="views-copies", level=3),
    out(C("""
        import numpy as np
        def scale(x):
            x *= 2
        def scale2(x):
            x = x * 2
        a = np.array([1, 2])
        scale(a)
        scale2(a)
        print(a)
        """),
        ["[2 4]", "[4 8]", "[1 2]", "[1 2 4]"], 0,
        "Which function mutates the caller's buffer?",
        "x *= 2 writes into the shared array, so the caller sees [2 4]. x = x * 2 only rebinds the local name.",
        analogy="Same as passing an object in JS: mutate a property and the caller sees it; reassign the parameter and it doesn't.",
        topic="views-copies", level=3),
    out(C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        print(np.shares_memory(a, a.ravel()))
        print(np.shares_memory(a, a.T.ravel()))
        print(np.shares_memory(a, a.flatten()))
        """),
        ["True\nFalse\nFalse", "True\nTrue\nFalse", "False\nFalse\nFalse", "True\nTrue\nTrue"], 0,
        "ravel returns a view only when it can.",
        "a is C-contiguous, so ravel can be a view. a.T read row by row is not a single stride pattern, so "
        "ravel must copy. flatten always copies.",
        topic="views-copies", level=4),
    mcq("You slice a 10 MB view `small = big[:10]` from a 2 GB array, delete `big`, and keep `small` in a cache. "
        "What happens to memory?",
        ["The whole 2 GB buffer stays alive, because small.base still references it",
         "Only 10 MB is kept; NumPy trims the buffer",
         "small becomes invalid and raises on access",
         "Python frees the 2 GB, and small now holds garbage"], 0,
        "A view keeps its owner alive.",
        "A view holds a reference to the base buffer, so the full 2 GB cannot be freed. Store small.copy() "
        "instead when caching a tiny piece of a huge array.",
        topic="views-copies", level=4),
    tf("`b = a[a > 0]` followed by `b[:] = 0` sets the positive elements of `a` to zero.", False,
       "Is boolean indexing a view?",
       "Boolean indexing makes a copy, so b[:] = 0 only clears the copy. Write a[a > 0] = 0 to change a.",
       topic="views-copies", level=4),

    # ------------------------------------------------------------------ reshaping
    out(C("""
        import numpy as np
        print(np.arange(6).reshape(2, 3))
        """),
        ["[[0 1 2]\n [3 4 5]]", "[[0 2 4]\n [1 3 5]]", "[[0 1]\n [2 3]\n [4 5]]", "[0 1 2 3 4 5]"], 0,
        "Fill the rows one at a time.",
        "reshape fills row by row (C order): first row 0 1 2, then 3 4 5.",
        topic="reshaping", level=1),
    mcq("Which reshape of a 12-element array is NOT allowed?",
        ["(5, 2)", "(3, 4)", "(2, 2, 3)", "(12, 1)"], 0,
        "Multiply the numbers in each shape.",
        "reshape cannot add or drop elements: the product of the new shape must equal 12. 5 x 2 = 10.",
        topic="reshaping", level=1),
    ask("What shape does reshape(3, -1) give for 12 elements?", C("""
        import numpy as np
        a = np.arange(12)
        print(a.reshape(3, -1).shape)
        """),
        ["(3, 4)", "(3, 1)", "(4, 3)", "ValueError"], 0,
        "-1 means 'work this one out for me'.",
        "With 12 elements and 3 rows, the -1 becomes 12 / 3 = 4.",
        topic="reshaping", level=2),
    out(C("""
        import numpy as np
        a = np.arange(12)
        print(a.reshape(5, -1))
        """),
        ["ValueError", "[[ 0  1]\n ...]", "(5, 2)", "IndexError"], 0,
        "-1 still has to give a whole number.",
        "12 is not divisible by 5, so no size works for -1 and reshape raises ValueError.",
        topic="reshaping", level=2),
    ask("What shape is the transpose?", C("""
        import numpy as np
        a = np.zeros((2, 5))
        print(a.T.shape)
        """),
        ["(5, 2)", "(2, 5)", "(10,)", "(5,)"], 0,
        ".T swaps rows and columns.",
        "The transpose of a 2x5 matrix is 5x2.",
        topic="reshaping", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3, 4])
        print(a[:, np.newaxis].shape, a[np.newaxis, :].shape)
        """),
        ["(4, 1) (1, 4)", "(1, 4) (4, 1)", "(4,) (4,)", "(4, 1) (4, 1)"], 0,
        "np.newaxis inserts a length-1 axis where it appears.",
        "a[:, None] turns the vector into a column (4, 1); a[None, :] makes a row (1, 4). np.newaxis is just None.",
        topic="reshaping", level=2),
    ask("What shape is left after squeeze?", C("""
        import numpy as np
        a = np.zeros((1, 3, 1))
        print(np.squeeze(a).shape)
        """),
        ["(3,)", "(1, 3)", "(3, 1)", "(1, 3, 1)"], 0,
        "squeeze removes every axis of length 1.",
        "Both length-1 axes go, leaving (3,). Pass axis= to remove only one of them.",
        topic="reshaping", level=2),
    fill("Which function adds a new axis of length 1 at a given position, as in `np.____(a, axis=0)`?",
         "expand_dims",
         "The opposite of squeeze.",
         "np.expand_dims(a, axis=0) turns shape (3,) into (1, 3). Same as a[np.newaxis, :].",
         topic="reshaping", level=2),
    ask("What shapes do transpose(1, 0, 2) and moveaxis(-1, 0) give?", C("""
        import numpy as np
        a = np.zeros((2, 3, 4))
        print(a.transpose(1, 0, 2).shape, np.moveaxis(a, -1, 0).shape)
        """),
        ["(3, 2, 4) (4, 2, 3)", "(2, 3, 4) (4, 3, 2)", "(3, 2, 4) (2, 3, 4)", "(4, 3, 2) (4, 2, 3)"], 0,
        "transpose takes the NEW order of the old axes.",
        "transpose(1, 0, 2) means new axes = old axes 1, 0, 2 -> (3, 2, 4). moveaxis(-1, 0) moves the last axis "
        "to the front -> (4, 2, 3), e.g. channels-last to channels-first.",
        topic="reshaping", level=3),
    out(C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        print(a.T.reshape(-1))
        """),
        ["[0 3 1 4 2 5]", "[0 1 2 3 4 5]", "[0 2 4 1 3 5]", "[5 4 3 2 1 0]"], 0,
        "reshape reads elements in the LOGICAL row-by-row order of a.T.",
        "a.T is [[0 3] [1 4] [2 5]]; reading its rows gives 0 3 1 4 2 5. Transpose and reshape are not the same operation.",
        diagram="""
a = [[0 1 2]      a.T = [[0 3]
     [3 4 5]]            [1 4]
                         [2 5]]
a.T read row by row: 0 3 1 4 2 5
""",
        topic="reshaping", level=3),
    out(C("""
        import numpy as np
        a = np.arange(12)
        print(a.reshape(-1, -1))
        """),
        ["ValueError", "[[ 0  1  2 ...]]", "(12, 1)", "TypeError"], 0,
        "How many unknowns can NumPy solve for?",
        "Only one dimension may be -1. With two unknowns the shape is ambiguous, so ValueError.",
        topic="reshaping", level=3),
    mcq("A batch of images has shape `(32, 28, 28)`. Which call flattens each image into a row for a linear model?",
        ["X.reshape(32, -1)  -> (32, 784)", "X.reshape(-1)  -> (25088,)", "X.flatten()  -> (25088,)",
         "X.reshape(-1, 32)  -> (784, 32)"], 0,
        "Keep the batch axis, merge the rest.",
        "reshape(32, -1) keeps one row per image and merges 28 x 28 = 784 pixels. reshape(-1, 32) has the "
        "right numbers but mixes pixels from different images in each column.",
        diagram="""
(32, 28, 28)
  |    \\___/
batch   pixels: 28 * 28 = 784
reshape(32, -1) -> (32, 784)   one row per image
""",
        topic="reshaping", level=3),
    out(C("""
        import numpy as np
        a = np.arange(6)
        print(a.reshape(2, 3, order="F"))
        """),
        ["[[0 2 4]\n [1 3 5]]", "[[0 1 2]\n [3 4 5]]", "[[0 3]\n [1 4]\n [2 5]]", "[[5 4 3]\n [2 1 0]]"], 0,
        "F (Fortran) order fills down the columns first.",
        "order='F' makes the FIRST index change fastest, so values fill column by column: 0 1 go in column 0, 2 3 in column 1...",
        topic="reshaping", level=4),
    out(C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        b = a.T
        b.shape = (6,)
        print(b)
        """),
        ["AttributeError", "[0 3 1 4 2 5]", "[0 1 2 3 4 5]", "ValueError"], 0,
        "Setting .shape must never copy.",
        "Assigning to .shape changes the shape in place, which is only possible without a copy. a.T cannot be "
        "flattened as a view, so NumPy raises AttributeError ('Incompatible shape for in-place modification'). "
        "reshape would quietly copy instead.",
        topic="reshaping", level=4),

    # ------------------------------------------------------------------ stack-split
    out(C("""
        import numpy as np
        print(np.concatenate([np.array([1, 2]), np.array([3, 4])]))
        """),
        ["[1 2 3 4]", "[[1 2]\n [3 4]]", "[4 6]", "[1 3 2 4]"], 0,
        "concatenate joins along an EXISTING axis.",
        "Two 1D arrays joined along axis 0 give one longer 1D array.",
        topic="stack-split", level=1),
    ask("What shapes do vstack and hstack give for two 1D arrays?", C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        print(np.vstack([a, b]).shape, np.hstack([a, b]).shape)
        """),
        ["(2, 3) (6,)", "(3, 2) (6,)", "(6,) (2, 3)", "(2, 3) (2, 3)"], 0,
        "v = vertical (pile up), h = horizontal (side by side).",
        "vstack treats each 1D array as a row and piles them: (2, 3). hstack on 1D arrays just joins them: (6,).",
        diagram="""
vstack:  [1 2 3]       hstack: [1 2 3 4 5 6]
         [4 5 6]
""",
        topic="stack-split", level=2),
    ask("What shapes does np.stack give with axis=0 and axis=1?", C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        print(np.stack([a, b]).shape, np.stack([a, b], axis=1).shape)
        """),
        ["(2, 3) (3, 2)", "(6,) (3, 2)", "(2, 3) (2, 3)", "(3, 2) (2, 3)"], 0,
        "stack creates a NEW axis at the given position.",
        "stack adds an axis: axis=0 puts the arrays as rows (2, 3), axis=1 puts them as columns (3, 2).",
        diagram="""
a = [1 2 3]   b = [4 5 6]
axis=0: [[1 2 3]      axis=1: [[1 4]
         [4 5 6]]              [2 5]
         (2, 3)                [3 6]]  (3, 2)
""",
        topic="stack-split", level=2),
    ask("What shapes do the two concatenations give?", C("""
        import numpy as np
        a = np.zeros((2, 3))
        b = np.ones((2, 3))
        print(np.concatenate([a, b], axis=1).shape, np.concatenate([a, b]).shape)
        """),
        ["(2, 6) (4, 3)", "(4, 3) (2, 6)", "(2, 6) (2, 6)", "(2, 2, 3) (4, 3)"], 0,
        "The default axis is 0.",
        "axis=1 joins side by side (more columns): (2, 6). The default axis=0 stacks rows: (4, 3).",
        topic="stack-split", level=2),
    out(C("""
        import numpy as np
        a = np.zeros((2, 3))
        b = np.zeros((3, 3))
        print(np.concatenate([a, b], axis=1).shape)
        """),
        ["ValueError", "(2, 6)", "(5, 3)", "(3, 6)"], 0,
        "All axes except the join axis must match.",
        "Joining along axis 1 requires the same number of rows (2 vs 3), so ValueError. Along axis 0 it would work: (5, 3).",
        topic="stack-split", level=3),
    out(C("""
        import numpy as np
        parts = np.split(np.arange(6), 3)
        print(len(parts), parts[1])
        """),
        ["3 [2 3]", "2 [3 4 5]", "3 [1 2]", "6 [1]"], 0,
        "An integer means 'this many equal parts'.",
        "np.split(a, 3) cuts 6 elements into 3 equal arrays of 2: [0 1], [2 3], [4 5].",
        topic="stack-split", level=3),
    out(C("""
        import numpy as np
        a = np.arange(7)
        print([len(p) for p in np.array_split(a, 3)])
        print(np.split(a, 3))
        """),
        ["[3, 2, 2]\nValueError", "[3, 2, 2]\n[3, 2, 2]", "[2, 2, 3]\nValueError", "ValueError"], 0,
        "One of these insists on equal parts.",
        "array_split allows uneven parts (the first ones get the extra). split requires an exact division "
        "and raises ValueError for 7 into 3.",
        topic="stack-split", level=3),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        print(np.column_stack([a, b]))
        """),
        ["[[1 4]\n [2 5]\n [3 6]]", "[[1 2 3]\n [4 5 6]]", "[1 2 3 4 5 6]", "[[1 2 3 4 5 6]]"], 0,
        "Each 1D input becomes one column.",
        "column_stack turns 1D arrays into columns, e.g. building a feature matrix from separate feature vectors. "
        "Same as np.stack([a, b], axis=1).",
        topic="stack-split", level=3),
    out(C("""
        import numpy as np
        parts = np.split(np.arange(10), [3, 7])
        print([p.tolist() for p in parts])
        """),
        ["[[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]", "[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]",
         "[[0, 1, 2], [3, 4, 5, 6, 7], [8, 9]]", "[[3], [7]]"], 0,
        "A list means 'cut BEFORE these indexes'.",
        "Split points [3, 7] give a[:3], a[3:7], a[7:]. Handy for train/val/test cuts on shuffled data.",
        topic="stack-split", level=4),
    mcq("You build a 100,000-row array inside a loop with `arr = np.append(arr, row)`. Why is this slow, and what is the fix?",
        ["Each append copies the whole array (O(n^2) total); collect rows in a list and call np.array / np.stack once",
         "np.append is slow only for floats; switch to int",
         "The loop is slow because NumPy locks the array; use threads",
         "It is not slow, np.append grows the buffer like a Python list"], 0,
        "Do NumPy arrays have spare capacity like a list or ArrayList?",
        "Arrays have a fixed size; np.append allocates a new array and copies everything every time. "
        "Python lists over-allocate (amortised O(1) append), so build a list, then convert once.",
        analogy="Like building a string with += in a loop in Java instead of using a StringBuilder.",
        topic="stack-split", level=4),

    # ------------------------------------------------------------------ memory-layout
    tf("In C order (NumPy's default), the LAST index changes fastest as you walk through memory.", True,
       "C order = row-major.",
       "Row-major: a[0,0], a[0,1], a[0,2], then a[1,0]... so neighbours in a row are neighbours in memory. "
       "F (Fortran) order is column-major: the first index changes fastest.",
       diagram="""
a = [[0 1 2]
     [3 4 5]]
C order memory: 0 1 2 3 4 5
F order memory: 0 3 1 4 2 5
""",
       topic="memory-layout", level=3),
    ask("What are the strides of the array and of its transpose?", C("""
        import numpy as np
        a = np.zeros((3, 4))
        print(a.strides, a.T.strides)
        """),
        ["(32, 8) (8, 32)", "(8, 32) (32, 8)", "(4, 1) (1, 4)", "(32, 8) (32, 8)"], 0,
        "A stride is how many BYTES to jump to move one step along an axis.",
        "float64 is 8 bytes. Next column: +8 bytes; next row: 4 columns x 8 = 32 bytes. Transpose just swaps "
        "the strides, no data is moved.",
        diagram="""
memory (float64, 8 bytes each):
[a00 a01 a02 a03 a10 a11 ...]
 +8 -> next column
 +32 -> next row (4 columns x 8)
a.T swaps the strides: (8, 32)
""",
        topic="memory-layout", level=3),
    ask("What do the contiguity flags report?", C("""
        import numpy as np
        a = np.zeros((3, 4))
        print(a.flags["C_CONTIGUOUS"], a.T.flags["C_CONTIGUOUS"], a.T.flags["F_CONTIGUOUS"])
        """),
        ["True False True", "True True True", "True False False", "False False True"], 0,
        "Transposing a row-major block gives a column-major view.",
        "a is C-contiguous. a.T uses the same memory with swapped strides, which is exactly an F-contiguous layout.",
        topic="memory-layout", level=3),
    ask("What strides are printed?", C("""
        import numpy as np
        a = np.arange(10)
        print(a.strides, a[::3].strides, a.astype(np.int32)[::3].strides)
        """),
        ["(8,) (24,) (12,)", "(8,) (8,) (4,)", "(1,) (3,) (3,)", "(8,) (24,) (24,)"], 0,
        "Stride = step x itemsize.",
        "int64 is 8 bytes; stepping 3 elements jumps 24 bytes. In int32 (4 bytes) the same step is 12 bytes.",
        topic="memory-layout", level=3),
    mcq("For a big C-ordered 2D array, why is summing each row usually faster than summing each column?",
        ["Each row is contiguous in memory, so reading it is cache-friendly; a column jumps by a full row each step",
         "Columns are stored on disk",
         "NumPy only vectorises along axis 0",
         "There is no difference; memory layout never matters"], 0,
        "Think CPU cache lines.",
        "The CPU loads memory in cache lines (64 bytes). Walking along a row uses every byte loaded; walking "
        "down a column skips a whole row per step and wastes most of each line.",
        topic="memory-layout", level=3),
    ask("What are the strides and the writeable flag of the broadcast view?", C("""
        import numpy as np
        b = np.broadcast_to(np.arange(3), (4, 3))
        print(b.strides, b.flags["WRITEABLE"])
        """),
        ["(0, 8) False", "(24, 8) True", "(8, 0) False", "(0, 8) True"], 0,
        "How do you repeat a row 4 times without copying?",
        "A stride of 0 on axis 0 means 'every row starts at the same address': the row is shared, not copied. "
        "It is read-only because writing one element would change all 4 rows.",
        diagram="""
memory:   [0][1][2]
row 0 ----^
row 1 ----^   stride 0: all rows point here
row 2 ----^
""",
        topic="memory-layout", level=4),
    ask("What shape, strides and memory sharing does the contiguous copy have?", C("""
        import numpy as np
        a = np.zeros((3, 4))
        c = np.ascontiguousarray(a.T)
        print(c.shape, c.strides, np.shares_memory(a, c))
        """),
        ["(4, 3) (24, 8) False", "(4, 3) (8, 32) True", "(3, 4) (32, 8) False", "(4, 3) (24, 8) True"], 0,
        "A C-contiguous (4, 3) float64 array: what are its strides?",
        "ascontiguousarray must copy a.T into row-major order: the next row is 3 x 8 = 24 bytes away. "
        "Libraries that need C-contiguous input (some C extensions, torch.from_numpy views) rely on this.",
        topic="memory-layout", level=4),
    mcq("Why is `a[::2]` a view but `a[[0, 2]]` a copy?",
        ["A view must be describable as (start pointer, shape, strides); a regular step fits that, an arbitrary index list does not",
         "Lists are slower than slices, so NumPy copies to speed them up",
         "It is a historical accident with no technical reason",
         "Both are views; only assignment makes a copy"], 0,
        "What metadata does an ndarray have to describe its memory?",
        "An ndarray is a buffer + offset + shape + strides. Every step-based slice is expressible that way. "
        "[0, 2, 3] or a mask has no constant stride in general, so NumPy has to gather values into new memory.",
        topic="memory-layout", level=4),
    ask("What shape and strides does the sliding-window view have, and does it copy?", C("""
        import numpy as np
        from numpy.lib.stride_tricks import sliding_window_view
        a = np.arange(6)
        w = sliding_window_view(a, 3)
        print(w.shape, w.strides, np.shares_memory(a, w))
        """),
        ["(4, 3) (8, 8) True", "(4, 3) (24, 8) False", "(2, 3) (24, 8) True", "(6, 3) (8, 8) True"], 0,
        "Consecutive windows start one element apart.",
        "4 windows of length 3. Moving to the next window AND to the next element both advance 8 bytes, so "
        "strides are (8, 8): overlapping windows with zero copying (rolling means, 1D convolutions).",
        topic="memory-layout", level=4),

    # ------------------------------------------------------------------ special-values
    tf("`np.nan == np.nan` is True.", False,
       "NaN means 'not a number': is unknown equal to unknown?",
       "By the IEEE float rules NaN is not equal to anything, itself included. Use np.isnan(x) to test for it.",
       topic="special-values", level=1),
    ask("What do sum and nansum return?", C("""
        import numpy as np
        a = np.array([1, np.nan, 3])
        print(a.sum(), np.nansum(a))
        """),
        ["nan 4.0", "4.0 4.0", "nan nan", "4.0 nan"], 0,
        "NaN poisons every calculation it touches.",
        "Any arithmetic with NaN gives NaN, so the plain sum is nan. np.nansum treats NaNs as missing and skips them.",
        topic="special-values", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, np.nan, 3])
        print(np.isnan(a))
        print(a == np.nan)
        """),
        ["[False  True False]\n[False False False]", "[False  True False]\n[False  True False]",
         "[ True False  True]\n[False False False]", "True\nFalse"], 0,
        "Only one of these really finds the NaN.",
        "np.isnan checks each element. a == np.nan is all False because NaN never compares equal.",
        topic="special-values", level=2),
    out(C("""
        import numpy as np
        with np.errstate(divide="ignore"):
            print(np.array([1.0, -2.0]) / 0)
        """),
        ["[ inf -inf]", "ZeroDivisionError", "[nan nan]", "[0. 0.]"], 0,
        "Floats have special values for 'too big'.",
        "Float division by zero gives +inf or -inf (with a RuntimeWarning, silenced here) instead of an error.",
        topic="special-values", level=2),
    out(C("""
        import numpy as np
        a = np.array([1, 2, 3])
        a[0] = np.nan
        print(a)
        """),
        ["ValueError", "[nan  2.  3.]", "[0 2 3]", "[nan 2 3]"], 0,
        "Integers have no NaN.",
        "NaN only exists for floats. Writing it into an int array raises ValueError (cannot convert float NaN to integer). "
        "That is why pandas turns int columns with missing values into float.",
        topic="special-values", level=3),
    out(C("""
        import numpy as np
        with np.errstate(invalid="ignore"):
            print(np.array([0.0]) / 0, np.inf - np.inf, np.inf * 0)
        """),
        ["[nan] nan nan", "[inf] 0.0 0.0", "[nan] 0.0 nan", "ZeroDivisionError"], 0,
        "These are the 'undefined' operations.",
        "0/0, inf - inf and inf * 0 have no sensible value, so IEEE floats give NaN. A NaN loss in training "
        "often starts with one of these.",
        topic="special-values", level=3),
    ask("What do max, nanmax and nanmean return?", C("""
        import numpy as np
        a = np.array([1, np.nan, 3])
        print(np.max(a), np.nanmax(a), np.nanmean(a))
        """),
        ["nan 3.0 2.0", "3.0 3.0 2.0", "nan 3.0 1.3333333333333333", "3.0 nan nan"], 0,
        "max also propagates NaN.",
        "max / mean / min return nan when any element is NaN. The nan-versions ignore them: nanmean = (1 + 3) / 2.",
        topic="special-values", level=3),
    out(C("""
        import numpy as np
        print(np.isfinite(np.array([1.0, np.inf, np.nan])))
        print(np.float16(70000))
        """),
        ["[ True False False]\ninf", "[ True  True False]\n70000.0", "[ True False  True]\n65504.0", "[ True False False]\n70000.0"], 0,
        "float16 tops out around 65 thousand.",
        "isfinite is False for both inf and nan. float16's largest value is 65504, so 70000 overflows to inf: "
        "one reason mixed-precision training uses loss scaling and bfloat16.",
        topic="special-values", level=3),
    out(C("""
        import numpy as np
        print(np.nan in [np.nan], np.nan == np.nan)
        x = float("nan")
        print(x in [float("nan")])
        """),
        ["True False\nFalse", "False False\nFalse", "True False\nTrue", "False False\nTrue"], 0,
        "Python's `in` checks identity before equality.",
        "list membership tries `is` first, and np.nan is one shared object, so it is found. Two different "
        "float('nan') objects are not identical and not equal, so the second check is False.",
        topic="special-values", level=4),
    out(C("""
        import numpy as np
        dt = np.dtype([("name", "U10"), ("age", "i4")])
        p = np.array([("Ann", 30), ("Bob", 25)], dtype=dt)
        print(p["age"].mean(), p[np.argsort(p["age"])]["name"])
        print(dt.itemsize)
        """),
        ["27.5 ['Bob' 'Ann']\n44", "27.5 ['Ann' 'Bob']\n14", "27.5 ['Bob' 'Ann']\n14", "TypeError"], 0,
        "Unicode strings in NumPy take 4 bytes per character.",
        "A structured array is like a table: p['age'] is a column. U10 = 10 chars x 4 bytes = 40, plus 4 for i4 = 44 "
        "bytes per record. Sorting by age puts Bob first.",
        topic="special-values", level=4),
    out(C("""
        import numpy as np
        a = np.array([3.0, np.nan, 1.0, 2.0])
        print(np.sort(a), np.argmax(a))
        """),
        ["[ 1.  2.  3. nan] 1", "[nan  1.  2.  3.] 0", "[ 1.  2.  3. nan] 0", "[ 1.  2.  3.] 1"], 0,
        "NumPy treats NaN as 'bigger than everything' for sorting and propagates it for max.",
        "np.sort pushes NaNs to the end. argmax returns the position of the first NaN, because max of an array "
        "with NaN is NaN. Use np.nanargmax to ignore them.",
        topic="special-values", level=4),

    # ------------------------------------------------------------------ extra concept checks
    tf("A Python list can hold an int, a string and another list at the same time; a normal numeric NumPy array cannot.", True,
       "Remember: one array, one dtype.",
       "Lists are heterogeneous containers of pointers. A numeric array stores raw values of a single dtype.",
       topic="why-arrays", level=1),
    fill("Which attribute tells you the data type of every element in array `a`? `a.____`", "dtype",
         "Short for 'data type'.",
         "a.dtype, e.g. int64 or float32. Change it with a.astype(...).",
         topic="attributes", level=1),
    fill("Which attribute gives the number of axes (dimensions) of an array? `a.____`", "ndim",
         "'n' dimensions.",
         "a.ndim equals len(a.shape): 1 for a vector, 2 for a matrix, 3 for a batch of matrices.",
         topic="attributes", level=1),
    tf("`np.arange(5)` and `np.linspace(0, 4, 5)` hold the same values with the same dtype.", False,
       "Check the default dtype of each.",
       "Same values 0..4, but arange(5) is int64 while linspace always returns float64 by default.",
       topic="creating", level=2),
    mcq("Which dtype would you choose for pixel values 0-255 to save memory, and what is the catch?",
        ["uint8 (1 byte each); arithmetic can wrap around, so convert to float before maths",
         "int64; it is the only dtype images can use",
         "float16; it is exact for all integers",
         "bool; it stores 0-255 in one bit"], 0,
        "Smallest type that fits 0..255.",
        "uint8 holds exactly 0..255 in one byte. But 200 + 100 wraps to 44 in uint8, so cast to float32 "
        "(and scale to 0..1) before normalising.",
        topic="dtypes", level=2),
    tf("Indexing a 2D array with a single integer, `a[0]`, returns the first row as a 1D array.", True,
       "Missing indexes mean ':'.",
       "a[0] is short for a[0, :]: the whole first row, with the row axis removed.",
       topic="indexing", level=1),
    fill("Complete the call so `idx` holds the positions where `a > 0`: `idx = np.____(a > 0)`", "flatnonzero",
         "A 'non-zero' finder that always returns a flat index array.",
         "np.flatnonzero(mask) returns the 1D indexes of True values. np.nonzero / np.where(mask) return a tuple "
         "of index arrays, one per axis.",
         topic="masks-fancy", level=3),
    tf("Fancy indexing with a boolean mask on the left of `=` (e.g. `a[mask] = 0`) modifies `a` in place.", True,
       "Reading and writing are different operations.",
       "Reading a[mask] makes a copy, but a[mask] = value is a __setitem__ call on a itself, so it writes into a.",
       topic="masks-fancy", level=2),
    tf("`a.reshape(...)` always returns a view.", False,
       "What if the data is not laid out in a way the new shape can describe?",
       "reshape returns a view when the strides allow it and silently copies otherwise (for example after a transpose). "
       "Never rely on reshape for in-place writes without checking np.shares_memory.",
       topic="views-copies", level=3),
    tf("`np.stack` requires all input arrays to have exactly the same shape.", True,
       "It builds a NEW axis.",
       "stack creates a new axis and puts each input along it, so every input must have identical shape. "
       "concatenate only needs the non-joined axes to match.",
       topic="stack-split", level=3),
    mcq("A C extension expects a C-contiguous float32 buffer. You have `x = big[:, ::2].T` in float64. "
        "What is the cheapest correct conversion?",
        ["np.ascontiguousarray(x, dtype=np.float32): one copy that fixes both layout and dtype",
         "x.astype(np.float32) then np.ascontiguousarray: always one copy",
         "x.view(np.float32)",
         "x.reshape(x.shape)"], 0,
        "Can one call do both jobs?",
        "ascontiguousarray with dtype converts and lays out in one pass. astype(...) defaults to order='K' "
        "(keeps the strided layout), so a second copy may follow. view reinterprets bytes (wrong values) and reshape changes nothing.",
        topic="memory-layout", level=4),
    tf("`np.isnan` works on integer arrays and always returns all False for them.", True,
       "Integers can't hold NaN, but is the function defined for them?",
       "np.isnan accepts integer input and returns False everywhere, since integers have no NaN. "
       "It does raise TypeError on object or string arrays.",
       code=C("""
           import numpy as np
           print(np.isnan(np.array([1, 2, 3])))
           """),
       topic="special-values", level=3),
]
