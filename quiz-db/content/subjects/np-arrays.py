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
    ("ml-arrays", "Arrays in ML code: batches, images, sequences"),
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

    # ------------------------------------------------------------------ round 2 depth: memory-layout
    out(C("""
        import numpy as np
        from numpy.lib.stride_tricks import as_strided
        a = np.arange(5)
        print(as_strided(a, shape=(3, 3), strides=(8, 8)))
        """),
        ["[[0 1 2]\n [1 2 3]\n [2 3 4]]", "[[0 1 2]\n [3 4 0]\n [0 0 0]]",
         "[[0 0 0]\n [1 1 1]\n [2 2 2]]", "ValueError"], 0,
        "Both axes step 8 bytes, i.e. one int64.",
        "as_strided builds a view with any shape and strides you ask for. Row stride 8 means each row starts one element "
        "later, so the rows overlap: sliding windows with no copy. The tempting [[0 1 2] [3 4 ...]] answer assumes a row "
        "stride of 24 (three elements), which is what reshape would use.",
        topic="memory-layout", level=3),
    ask("What strides does a C-ordered int32 array of shape (2, 3, 4) have?", C("""
        import numpy as np
        print(np.zeros((2, 3, 4), dtype=np.int32).strides)
        """),
        ["(48, 16, 4)", "(4, 16, 48)", "(96, 32, 8)", "(24, 12, 4)"], 0,
        "Last axis moves one item; each earlier axis jumps over a whole block of the later ones.",
        "itemsize is 4. Last axis: 4 bytes. Middle axis: 4 items x 4 = 16. First axis: 3 x 4 items x 4 = 48. "
        "(96, 32, 8) is the int64 answer; (4, 16, 48) is Fortran order.",
        diagram=C("""
            shape (2, 3, 4), int32, C order
            axis 2: next item        ->  4 bytes
            axis 1: skip 4 items     -> 16 bytes
            axis 0: skip 3*4 items   -> 48 bytes
            """),
        topic="memory-layout", level=3),
    ask("What strides does a Fortran-ordered float64 array of shape (3, 4) have?", C("""
        import numpy as np
        print(np.zeros((3, 4), order="F").strides)
        """),
        ["(8, 24)", "(32, 8)", "(24, 8)", "(8, 32)"], 0,
        "In F order the FIRST index changes fastest.",
        "Column-major: walking down a column moves 8 bytes, moving to the next column skips 3 rows = 24 bytes. "
        "(32, 8) is the C-order layout of the same shape. Fortran order is what LAPACK and MATLAB use natively.",
        topic="memory-layout", level=3),
    ask("Why does `np.zeros((10_000, 10_000))[:, 0].sum()` touch far more memory than the 10,000 numbers it adds?",
        None,
        ["Each value sits in a different cache line, so the CPU loads 64 bytes to use 8",
         "NumPy copies the whole array before slicing a column",
         "Column slices are converted to Python floats first",
         "sum always reads the base array, not the view"], 0,
        "Think about what the CPU fetches from RAM: single numbers or whole lines?",
        "A column of a C-ordered array has a stride of 80,000 bytes, so every element is in its own 64-byte cache line: "
        "you pay for 8x the bytes you use and the prefetcher can't help. No copy happens; the slice is a view. "
        "Like scanning one column of a row-store database table: every row page gets read anyway.",
        analogy="Reading one field from every record in a row-oriented database: you fetch every page even though you need one value per row.",
        topic="memory-layout", level=3),
    ask("What strides does the reversed, stepped view have?", C("""
        import numpy as np
        a = np.arange(12).reshape(4, 3)
        print(a[::2, ::-1].strides)
        """),
        ["(48, -8)", "(48, 8)", "(24, -8)", "(-48, 8)"], 0,
        "A step multiplies the stride; a negative step flips its sign.",
        "Row stride is 24 bytes; step 2 doubles it to 48. Column stride 8 with step -1 becomes -8, and the view's start "
        "pointer moves to the last column. Negative strides are why a[::-1] is O(1), and why some C libraries "
        "(and torch.from_numpy) reject such arrays until you call np.ascontiguousarray.",
        topic="memory-layout", level=4),
    ask("What do the two memory-overlap checks report for the even and odd elements?", C("""
        import numpy as np
        a = np.arange(10)
        print(np.may_share_memory(a[::2], a[1::2]), np.shares_memory(a[::2], a[1::2]))
        """),
        ["True False", "True True", "False False", "False True"], 0,
        "One check only compares the memory bounds; the other solves the exact problem.",
        "Even and odd elements interleave in the same byte range, so the quick bounds test may_share_memory says True. "
        "shares_memory does the exact (potentially expensive) check and finds no byte in common. "
        "Use may_share_memory as a cheap conservative guard, shares_memory when you need the truth.",
        analogy="Like a Bloom filter versus a real lookup: the quick check can say 'maybe' when the answer is no.",
        topic="memory-layout", level=4),
    out(C("""
        import numpy as np
        from numpy.lib.stride_tricks import sliding_window_view
        img = np.zeros((5, 5))
        print(sliding_window_view(img, (3, 3)).shape)
        """),
        ["(3, 3, 3, 3)", "(9, 3, 3)", "(3, 3)", "(5, 5, 3, 3)"], 0,
        "How many 3x3 positions fit along each axis of a 5x5 image?",
        "3 positions down x 3 across, each a 3x3 patch: (3, 3, 3, 3), all a zero-copy view. This is im2col, the trick "
        "behind a naive convolution: reshape to (9, 9) and one matmul with the flattened kernel does every patch. "
        "The reshape to (9, 9) is the moment a copy happens.",
        topic="memory-layout", level=4),
    mcq("Why is `np.lib.stride_tricks.as_strided` considered dangerous, while `sliding_window_view` is safe?",
        ["as_strided does no bounds checks, so wrong strides read or write memory outside the buffer",
         "as_strided always copies, which can exhaust memory",
         "as_strided only works on float arrays",
         "sliding_window_view runs in Python, as_strided in C"], 0,
        "What stops you from asking for shape (100, 100) on a 5-element array?",
        "as_strided trusts whatever shape and strides you give it: one wrong number and you see garbage or crash the "
        "process. sliding_window_view computes the strides for you and returns a read-only view. "
        "It's like raw pointer arithmetic in C versus a bounds-checked slice API.",
        analogy="as_strided is pointer arithmetic with no bounds check; sliding_window_view is the safe library wrapper around it.",
        topic="memory-layout", level=4),

    # ------------------------------------------------------------------ round 2 depth: views-copies
    ask("Which of these two reshapes can return a view?", C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        print(np.shares_memory(a.T, a.T.reshape(6)), np.shares_memory(a, a.reshape(3, 2)))
        """),
        ["False True", "True True", "True False", "False False"], 0,
        "Can the transposed elements, read in C order, be reached with one fixed stride?",
        "a.T in C order is 0 3 1 4 2 5: no single stride walks that through the buffer, so reshape must copy. "
        "a.reshape(3, 2) on a contiguous array only regroups the same order, so it's a view. "
        "Interview point: reshape is 'view if possible, copy if necessary', and you can't tell without checking.",
        topic="views-copies", level=3),
    out(C("""
        import numpy as np
        a = np.zeros(4)
        a[[1, 2]][0] = 5
        a[1:3][0] = 7
        print(a)
        """),
        ["[0. 7. 0. 0.]", "[0. 5. 0. 0.]", "[0. 7. 5. 0.]", "[0. 0. 0. 0.]"], 0,
        "Which of the two chained indexes returns a temporary copy?",
        "a[[1, 2]] makes a copy, and [0] = 5 writes into that temporary, which is then thrown away. a[1:3] is a view, "
        "so writing into it reaches a. Same idea as pandas' chained-assignment warning: write with ONE index "
        "operation, e.g. a[[1]] = 5.",
        topic="views-copies", level=3),
    out(C("""
        import numpy as np
        a = np.arange(12).reshape(3, 4)
        print(np.shares_memory(a, a[:, :2].reshape(-1)),
              np.shares_memory(a, a[:2].reshape(-1)),
              np.shares_memory(a, a[:, ::2].reshape(3, 1, 2)))
        """),
        ["False True True", "True True True", "False True False", "False False False"], 0,
        "Flattening needs one constant stride; adding a size-1 axis needs none.",
        "a[:, :2] has a gap after every 2 items, so flattening it must copy. a[:2] is a contiguous block of rows: view. "
        "a[:, ::2].reshape(3, 1, 2) only inserts a length-1 axis, which any strided array can do as a view. "
        "So 'non-contiguous means copy' is too simple: it depends on which axes you merge.",
        topic="views-copies", level=4),
    ask("What do the two ravel calls give on a Fortran-ordered array, and is the second one a view?", C("""
        import numpy as np
        a = np.arange(6).reshape(2, 3)
        f = np.asfortranarray(a)
        print(f.ravel(), f.ravel(order="K"), np.shares_memory(f, f.ravel(order="K")))
        """),
        ["[0 1 2 3 4 5] [0 3 1 4 2 5] True", "[0 3 1 4 2 5] [0 3 1 4 2 5] True",
         "[0 1 2 3 4 5] [0 1 2 3 4 5] False", "[0 1 2 3 4 5] [0 3 1 4 2 5] False"], 0,
        "ravel's default is C order whatever the memory layout; order='K' means 'as stored'.",
        "f holds the same values in column-major memory. ravel() promises logical C order, so it must copy. "
        "ravel(order='K') reads in memory order (0 3 1 4 2 5) and can return a view. "
        "Tempting wrong answer: assuming ravel() follows the memory layout; it follows the logical one unless you ask.",
        topic="views-copies", level=4),
    out(C("""
        import numpy as np
        buf = np.empty(2)
        batches = []
        for i in range(3):
            buf[:] = i
            batches.append(buf)
        print(np.array(batches))
        """),
        ["[[2. 2.]\n [2. 2.]\n [2. 2.]]", "[[0. 0.]\n [1. 1.]\n [2. 2.]]",
         "[[0. 0.]\n [0. 0.]\n [0. 0.]]", "ValueError"], 0,
        "How many distinct arrays does the list hold?",
        "The list holds three references to the SAME buffer, which ends up full of 2s. A reused buffer in a "
        "data loader causes exactly this: every saved batch equals the last one. Append buf.copy() instead. "
        "It's the classic JavaScript bug of pushing the same mutable object into an array in a loop.",
        analogy="Like pushing the same object into a JS array inside a loop and mutating it: every slot shows the last state.",
        topic="views-copies", level=4),
    tf("`b = a[...]` gives a new array object that shares memory with `a`, so `b is a` is False but writes through `b` change `a`.",
       True,
       "Ellipsis on its own is a full basic slice.",
       "a[...] (like a[:]) is basic indexing, so it returns a fresh view: a new object with the same buffer. "
       "That's why `b[...] = 0` or `a[:] = new` are the idioms for overwriting an array in place, e.g. updating "
       "a weight buffer that other code already holds a reference to.",
       topic="views-copies", level=3),

    # ------------------------------------------------------------------ round 2 depth: masks-fancy
    out(C("""
        import numpy as np
        a = np.zeros(3)
        a[[0, 0, 0]] = [1, 2, 3]
        print(a)
        """),
        ["[3. 0. 0.]", "[6. 0. 0.]", "[1. 0. 0.]", "ValueError"], 0,
        "Three writes to the same slot: which one survives?",
        "Fancy assignment with repeated indices performs the writes in order, so the last value wins (3). It does "
        "NOT add them up (that is np.add.at). Don't rely on 'last wins' in production code: it's the observed "
        "behaviour, and the docs only promise one of the values ends up there.",
        topic="masks-fancy", level=3),
    ask("What is `a` after assigning through np.ix_?", C("""
        import numpy as np
        a = np.arange(9).reshape(3, 3)
        a[np.ix_([0, 2], [1, 2])] = 0
        print(a)
        """),
        ["[[0 0 0]\n [3 4 5]\n [6 0 0]]", "[[0 0 2]\n [3 4 5]\n [6 7 0]]",
         "[[0 1 2]\n [3 4 5]\n [6 7 8]]", "[[0 0 0]\n [3 4 5]\n [0 0 0]]"], 0,
        "np.ix_ turns two lists into an open mesh: every row with every column.",
        "np.ix_([0, 2], [1, 2]) addresses the 2x2 block rows {0, 2} x columns {1, 2}, and the assignment writes "
        "through to a. Without ix_, a[[0, 2], [1, 2]] = 0 would only zero the two pairs (0, 1) and (2, 2).",
        diagram=C("""
                  col1 col2
            row0   x    x      np.ix_: every row x every col
            row2   x    x      pairs : only (0,1) and (2,2)
            """),
        topic="masks-fancy", level=3),
    out(C("""
        import numpy as np
        a = np.arange(4)
        print(a[np.array([True, False])])
        """),
        ["IndexError", "[0]", "[0 2]", "[0 1 2 3]"], 0,
        "Does NumPy repeat or pad a short mask?",
        "A boolean index must match the axis length exactly; a length-2 mask on 4 elements raises IndexError. "
        "In ML code this catches mask/feature misalignment early, e.g. a mask built on the train rows applied to "
        "the full dataset.",
        topic="masks-fancy", level=3),
    ask("What do np.nonzero and np.argwhere return for a 2D array?", C("""
        import numpy as np
        a = np.array([[0, 5], [7, 0]])
        print(np.nonzero(a), np.argwhere(a).shape)
        """),
        ["(array([0, 1]), array([1, 0])) (2, 2)", "[[0 1] [1 0]] (2,)",
         "(array([1, 2]),) (2, 2)", "(array([0, 1]), array([1, 0])) (4, 2)"], 0,
        "One groups by axis, the other by element.",
        "nonzero returns one index array per axis (rows, cols), ready to use as a[np.nonzero(a)]. argwhere returns "
        "one row per hit, shape (k, ndim), which is nicer to loop over or print as coordinates.",
        topic="masks-fancy", level=3),
    ask("What does the weighted bincount return?", C("""
        import numpy as np
        idx = np.array([0, 2, 0])
        w = np.array([1.0, 2.0, 3.0])
        print(np.bincount(idx, weights=w, minlength=4))
        """),
        ["[4. 0. 2. 0.]", "[1. 0. 2. 3.]", "[3. 0. 2. 0.]", "[4. 2.]"], 0,
        "Each weight is added into the bin named by its index.",
        "bincount sums weights per index: bin 0 gets 1 + 3, bin 2 gets 2, minlength pads to 4 bins. For 1D "
        "non-negative int keys this is a fast alternative to np.add.at (scatter-add), e.g. summing loss per class "
        "or counting tokens per id. a[idx] += w would give bin 0 only 3, because repeated indices are buffered.",
        diagram=C("""
            idx : 0    2    0
            w   : 1.0  2.0  3.0
            bin 0 <- 1.0 + 3.0 = 4.0
            bin 2 <- 2.0
            bins 1, 3 stay 0 (minlength=4)
            """),
        topic="masks-fancy", level=4),
    mcq("In a hand-written embedding layer, `grad_E[token_ids] += grad_out` is used to accumulate gradients for a batch "
        "where some token ids repeat. What goes wrong?",
        ["Repeated ids get only one of their gradient rows; use np.add.at(grad_E, token_ids, grad_out)",
         "Nothing: += with fancy indexing adds every row",
         "It raises IndexError on repeated ids",
         "It adds every row but in a random order, so results are not reproducible"], 0,
        "Fancy-index += is read all, add, write all.",
        "a[idx] += v is a[idx] = a[idx] + v: the reads happen first, then the writes, so duplicates overwrite each "
        "other and frequent tokens get too little gradient. No error is raised, so the model just trains worse. "
        "np.add.at is unbuffered and adds every occurrence, which is what frameworks do for embedding backward.",
        topic="masks-fancy", level=4),

    # ------------------------------------------------------------------ round 2 depth: dtypes
    out(C("""
        import numpy as np
        img = np.array([250, 10], dtype=np.uint8)
        print(img + 10, img.astype(np.int16) + 10)
        """),
        ["[ 4 20] [260  20]", "[260  20] [260  20]", "[255  20] [260  20]", "OverflowError"], 0,
        "uint8 holds 0-255 and Python's 10 adopts the array's dtype.",
        "uint8 arithmetic wraps mod 256: 250 + 10 = 260 -> 4. Brightening an image this way turns white pixels "
        "black. Cast to a wider type first (or use np.clip on a wider copy) and convert back with clipping.",
        diagram=C("""
            uint8 wheel: ... 253 254 255 | 0 1 2 3 4 ...
            250 + 10 ->  goes past 255   -> wraps to 4
            """),
        topic="dtypes", level=3),
    ask("Two uint8 grayscale frames are subtracted to find motion. What does the difference show?", C("""
        import numpy as np
        a = np.array([10, 200], dtype=np.uint8)
        b = np.array([20, 190], dtype=np.uint8)
        print(a - b, np.abs(a.astype(np.int16) - b))
        """),
        ["[246  10] [10 10]", "[-10  10] [10 10]", "[0 10] [10 10]", "[246  10] [246  10]"], 0,
        "There is no -10 in uint8.",
        "10 - 20 wraps to 246, so a small change looks like a huge one. np.abs(a - b) can't fix it: the wrap already "
        "happened. Upcast first (int16 holds -255..255) and then take the absolute value. Same trap as unsigned "
        "subtraction in C.",
        analogy="Like a car odometer rolling back past 000000 to 999990: the reading is huge, not negative.",
        topic="dtypes", level=3),
    ask("How does float16 store 2049 and 2051?", C("""
        import numpy as np
        print(np.float16(2049), np.float16(2051))
        """),
        ["2048.0 2052.0", "2049.0 2051.0", "2048.0 2050.0", "2050.0 2052.0"], 0,
        "float16 has 11 significant bits; above 2048 the gap between floats is 2.",
        "float16 stores integers exactly only up to 2048. Between 2048 and 4096 the spacing is 2, so 2049 and 2051 "
        "are both halfway cases and round to the even mantissa: 2048 and 2052. That's why fp16 counters and "
        "token-id arrays are a bug, and why mixed-precision training keeps master weights in float32.",
        topic="dtypes", level=3),
    out(C("""
        import numpy as np
        print(np.float16(65519), np.float16(65520))
        """),
        ["65500.0 inf", "65519.0 65520.0", "65500.0 65500.0", "inf inf"], 0,
        "float16's largest finite value is 65504.",
        "65519 still rounds down to 65504 (printed as 65500.0 with float16's short repr); 65520 is the halfway point "
        "to the next would-be value and rounds up to inf. One large activation or squared loss in fp16 is enough "
        "to make inf and then NaN, which is why fp16 training needs loss scaling and bf16 is preferred.",
        diagram=C("""
            ... 65472   65504 | (65536 would be next)
                              ^ halfway = 65520
            65519 -> 65504      65520 -> inf
            """),
        topic="dtypes", level=4),
    out(C("""
        import numpy as np
        u = np.array([200, 100], dtype=np.uint8)
        print((u[0] + u[1]) / 2, u.mean())
        """),
        ["22.0 150.0", "150.0 150.0", "22.0 22.0", "OverflowError"], 0,
        "The two uint8 scalars are added before the division happens.",
        "u[0] + u[1] is uint8 + uint8 = 300 mod 256 = 44 (a RuntimeWarning, silenced here), then 44 / 2 = 22.0. "
        "mean() accumulates in float64, so it gives 150.0. Hand-written averages of image pixels are a classic "
        "source of dark blotches in augmented images.",
        topic="dtypes", level=4),
    out(C("""
        import numpy as np
        try:
            print(np.array([1], dtype=np.uint8) + -1)
        except Exception as e:
            print(type(e).__name__)
        print(np.array([1.0], dtype=np.float32) * 1e300)
        """),
        ["OverflowError\n[inf]", "[0]\n[1.e+300]", "[0]\n[inf]", "OverflowError\n[1.e+300]"], 0,
        "NEP 50: a Python scalar takes the array's dtype, if it fits.",
        "Under NumPy 2's weak-scalar rules, -1 must be converted to uint8 and can't be, so you get OverflowError "
        "(NumPy 1 silently upcast to int16). 1e300 is a valid float, so it becomes float32 inf and the result is "
        "float32 inf, not a float64 1e300. Code written for NumPy 1 can break or change dtype on upgrade.",
        analogy="Like TypeScript literal types widening to the declared variable type: the literal adapts to the array, not the other way round.",
        topic="dtypes", level=4),

    # ------------------------------------------------------------------ round 2 depth: special-values
    ask("How many elements does each mask count?", C("""
        import numpy as np
        a = np.array([np.nan, 1.0, -1.0])
        print((a > 0).sum(), (~(a <= 0)).sum())
        """),
        ["1 2", "1 1", "2 2", "nan nan"], 0,
        "Every comparison with NaN is False, including <=.",
        "NaN > 0 is False and NaN <= 0 is also False, so negating the second mask flips NaN to True. "
        "'Not non-positive' is not the same as 'positive' once NaNs exist. In a data filter this silently keeps "
        "or drops missing rows depending on how the condition was phrased; handle np.isnan explicitly.",
        diagram=C("""
            value     a > 0    a <= 0   ~(a <= 0)
            nan       False    False    True
            1.0       True     False    True
            -1.0      False    True     False
            """),
        topic="special-values", level=4),
    out(C("""
        import numpy as np
        try:
            print(np.nanargmax(np.array([np.nan, np.nan])))
        except ValueError as e:
            print("ValueError")
        print(np.nanargmax(np.array([np.nan, 2.0, 5.0])))
        """),
        ["ValueError\n2", "0\n2", "nan\n2", "-1\n2"], 0,
        "There is no valid index to return if every value is missing.",
        "nanargmax skips NaNs, so [nan, 2, 5] gives 2. With nothing but NaNs there is no answer, and it raises "
        "ValueError instead of returning a fake index. A predict step that hits an all-NaN row (e.g. a broken feature "
        "pipeline) fails loudly here, which is better than silently picking class 0.",
        topic="special-values", level=3),
    ask("What does np.nan_to_num replace NaN and infinities with by default?", C("""
        import numpy as np
        r = np.nan_to_num(np.array([np.nan, np.inf, -np.inf, 1.0]))
        print(r[0], r[1] == np.finfo(np.float64).max, r[3])
        """),
        ["NaN -> 0.0, inf -> the largest finite float, -inf -> the most negative float",
         "Everything non-finite becomes 0.0",
         "NaN -> 0.0, infinities are left unchanged",
         "NaN -> the column mean, infinities -> 0.0"], 0,
        "Infinities are clamped, not zeroed.",
        "nan_to_num maps NaN to 0.0 and +/-inf to +/-1.8e308 (pass nan=, posinf=, neginf= to choose). Those huge "
        "finite values can still blow up a later sum, so in a feature pipeline it's often better to impute on "
        "purpose than to rely on the defaults.",
        topic="special-values", level=3),
    ask("What do the field view's strides, the record size and the updated age come out as?", C("""
        import numpy as np
        dt = np.dtype([("name", "U10"), ("age", "i4")])
        p = np.array([("Ann", 30), ("Bob", 25)], dtype=dt)
        ages = p["age"]
        ages += 1
        print(ages.strides, p.itemsize, p[0]["age"])
        """),
        ["(44,) 44 31", "(4,) 44 31", "(44,) 14 30", "(4,) 14 30"], 0,
        "A field is a view that steps over whole records.",
        "U10 takes 40 bytes (4 per character) plus 4 for the int32: 44-byte records. p['age'] is a strided view "
        "with stride 44, so += 1 updates p itself. This 'array of structs' layout is why columnar tools (pandas, "
        "Arrow) store each field as its own contiguous array instead.",
        topic="special-values", level=4),

    # ------------------------------------------------------------------ round 2 depth: creating
    out(C("""
        import numpy as np
        print(np.linspace(0, 1, 5, dtype=int))
        """),
        ["[0 0 0 0 1]", "[0 1 2 3 4]", "[0 0 1 1 1]", "[0. 0.25 0.5 0.75 1.]"], 0,
        "The floats are computed first, then cast.",
        "linspace computes 0, 0.25, 0.5, 0.75, 1.0 and casting to int truncates toward zero: four zeros and a one. "
        "If you wanted evenly spaced integer indices (e.g. frames to sample from a video), round first: "
        "np.linspace(0, n - 1, k).round().astype(int).",
        topic="creating", level=4),
    ask("What do these two grids look like?", C("""
        import numpy as np
        X, Y = np.meshgrid(np.arange(3), np.arange(2))
        Xi, Yi = np.meshgrid(np.arange(3), np.arange(2), indexing="ij")
        print(X.shape, Xi.shape)
        """),
        ["(2, 3) (3, 2)", "(3, 2) (3, 2)", "(2, 3) (2, 3)", "(3, 2) (2, 3)"], 0,
        "The default indexing is 'xy', plotting style: x runs along columns.",
        "With the default indexing='xy' the first input (length 3) runs along columns, giving shape (len(y), len(x)) "
        "= (2, 3), which matches images and matplotlib. indexing='ij' gives matrix-style (3, 2). Mixing the two "
        "is a common transposed-heatmap bug when evaluating a model on a grid of points.",
        topic="creating", level=3),
    out(C("""
        import numpy as np
        rng = np.random.default_rng(0)
        print(rng.random(3, dtype=np.float32).dtype, rng.integers(0, 10, size=(2, 3)).dtype)
        """),
        ["float32 int64", "float64 int64", "float32 int32", "float64 float64"], 0,
        "Generator methods take a dtype argument; integers defaults to int64.",
        "rng.random(..., dtype=np.float32) generates float32 directly (no float64 temporary to cast), useful for big "
        "weight initialisations. integers defaults to int64. The legacy np.random.rand has no dtype argument at all.",
        topic="creating", level=3),

    # ------------------------------------------------------------------ round 2 depth: attributes / indexing
    ask("What dtype and itemsize does the string array have?", C("""
        import numpy as np
        a = np.array(["ab", "cdefg"])
        print(a.dtype, a.itemsize)
        """),
        ["<U5 20", "<U5 5", "<U2 8", "object 8"], 0,
        "Unicode arrays are fixed width: every slot is as wide as the longest string.",
        "dtype <U5 means up to 5 characters, each stored as 4 bytes (UTF-32), so 20 bytes per element even for 'ab'. "
        "A million short labels padded to one long one can waste a lot of memory; map labels to int ids instead.",
        topic="attributes", level=3),
    ask("What shapes do these None (np.newaxis) insertions give for `a` of shape (4, 5)?", C("""
        import numpy as np
        a = np.zeros((4, 5))
        print(a[:, None, :].shape, a[..., None].shape, a[None].shape)
        """),
        ["(4, 1, 5) (4, 5, 1) (1, 4, 5)", "(4, 5, 1) (4, 5, 1) (1, 4, 5)",
         "(1, 4, 5) (4, 5, 1) (4, 1, 5)", "(4, 1, 5) (1, 4, 5) (4, 5, 1)"], 0,
        "None goes exactly where you write it; ... stands for all the other axes.",
        "Each None inserts a length-1 axis at its position: middle, end, front. These are the shapes you build "
        "on purpose for broadcasting, e.g. x[:, None, :] - c[None, :, :] for distances from every point to every centroid.",
        topic="indexing", level=3),

    # ------------------------------------------------------------------ ml-arrays
    mcq("A dataset of 1,000 samples with 20 features each is stored as one NumPy array. What shape is it, by convention?",
        ["(1000, 20): one row per sample, one column per feature",
         "(20, 1000): one row per feature",
         "(20000,): all numbers in one line",
         "(1000,): one number per sample"], 0,
        "Think of a spreadsheet: what is a row?",
        "ML libraries (scikit-learn, PyTorch) expect X with shape (n_samples, n_features): rows are examples, "
        "columns are features. The first axis is the 'batch' axis that you slice to make mini-batches.",
        analogy="Like a database table: each row is one record (sample), each column one field (feature).",
        topic="ml-arrays", level=1),
    out(C("""
        import numpy as np
        img = np.zeros((28, 28, 3))
        print(img.shape[0], img.shape[2])
        """),
        ["28 3", "3 28", "28 28", "784 3"], 0,
        "A colour image is height x width x colour channels.",
        "A colour image is usually a 3D array (height, width, channels). Here 28 rows of pixels, and 3 channels "
        "(red, green, blue).",
        topic="ml-arrays", level=1),
    tf("In an image array of shape (height, width, 3), `img[10, 20]` is the pixel in row 10, column 20, so the first index is the y coordinate.",
       True,
       "Rows go down the image.",
       "Arrays index (row, col), so the first index is the vertical position (y) and the second the horizontal (x). "
       "Libraries that take (x, y) points (OpenCV drawing, matplotlib scatter) use the opposite order, a frequent "
       "source of swapped coordinates.",
       topic="ml-arrays", level=2),
    ask("What batch sizes does the slicing loop produce?", C("""
        import numpy as np
        X = np.arange(10)
        print([len(X[i:i + 4]) for i in range(0, len(X), 4)])
        """),
        ["[4, 4, 2]", "[4, 4, 4]", "[4, 4]", "[3, 3, 4]"], 0,
        "Slicing past the end just stops at the end.",
        "Batches of 4 from 10 samples: 4, 4 and a last partial batch of 2. Slices never raise when they run off the "
        "end. Training code must handle the short last batch (or drop it, like PyTorch's drop_last=True).",
        topic="ml-arrays", level=2),
    out(C("""
        import numpy as np
        y = np.array([2, 0])
        print(np.eye(3, dtype=int)[y])
        print(np.eye(3)[y].argmax(axis=1))
        """),
        ["[[0 0 1]\n [1 0 0]]\n[2 0]", "[[0 1 0]\n [1 0 0]]\n[1 0]",
         "[[0 0 1]\n [1 0 0]]\n[0 2]", "[[1 0 0]\n [0 0 1]]\n[2 0]"], 0,
        "Row k of the identity matrix is the one-hot vector for class k.",
        "Fancy-indexing rows of np.eye turns labels into one-hot rows; argmax along axis 1 turns them back. "
        "The index list makes a copy, so the identity matrix itself is untouched.",
        topic="ml-arrays", level=2),
    mcq("A batch of 64 RGB images at 224 x 224 is stored as float32. Roughly how much memory does the input batch take?",
        ["About 37 MB", "About 9 MB", "About 74 MB", "About 3.7 GB"], 0,
        "64 x 3 x 224 x 224 x bytes-per-float32.",
        "64 * 3 * 224 * 224 = 9.6 million values; x 4 bytes = 38.5 million bytes, about 37 MiB. 9 MB is the uint8 "
        "size, 74 MB the float64 size. Keeping images as uint8 until the GPU step is why loaders are 4x lighter.",
        topic="ml-arrays", level=3),
    ask("A loader gives images as NHWC `(8, 32, 32, 3)` but the model wants NCHW. What does the conversion give?", C("""
        import numpy as np
        x = np.zeros((8, 32, 32, 3)).transpose(0, 3, 1, 2)
        print(x.shape, x.flags["C_CONTIGUOUS"])
        """),
        ["(8, 3, 32, 32) False", "(8, 3, 32, 32) True", "(8, 32, 3, 32) False", "(3, 8, 32, 32) False"], 0,
        "transpose moves axes by rewriting strides; does it move any data?",
        "transpose(0, 3, 1, 2) puts channels second: (8, 3, 32, 32). It's a view, so it isn't C-contiguous. "
        "reshape(8, 3, 32, 32) would give the right shape but scramble pixels across channels. Call "
        "np.ascontiguousarray before handing it to code that needs a packed buffer.",
        diagram=C("""
            NHWC (8, 32, 32, 3)
                 0   1   2   3     axes
            transpose(0, 3, 1, 2)
            NCHW (8, 3, 32, 32)    same bytes, new strides
            """),
        topic="ml-arrays", level=3),
    ask("What dtypes do these pixel normalisations produce for a uint8 image?", C("""
        import numpy as np
        img = np.zeros((4, 5, 3), dtype=np.uint8)
        print((img / 255).dtype, (img / np.float32(255)).dtype, (img.astype(np.float32) / 255).dtype)
        """),
        ["float64 float32 float32", "float32 float32 float32", "uint8 float32 float32", "float64 float64 float32"], 0,
        "True division always makes floats. Which float does a Python scalar pick?",
        "img / 255 gives float64 (uint8 has to become a float, and the default is float64), doubling memory versus "
        "float32. Dividing by a NumPy float32 scalar, or casting first, keeps float32, which is what models train in. "
        "A float64 batch handed to a float32 PyTorch model raises a dtype mismatch error.",
        topic="ml-arrays", level=3),
    ask("What padding mask does the broadcast comparison build?", C("""
        import numpy as np
        lengths = np.array([3, 1, 2])
        mask = np.arange(3) < lengths[:, None]
        print(mask.astype(int))
        """),
        ["[[1 1 1]\n [1 0 0]\n [1 1 0]]", "[[1 1 1]\n [1 1 1]\n [1 1 1]]",
         "[[1 0 0]\n [1 1 1]\n [1 1 0]]", "[1 1 0]"], 0,
        "Compare every position (columns) with every sequence length (rows).",
        "(3,) against (3, 1) broadcasts to a (3, 3) table: position j < length i. This is the padding mask for a batch "
        "of variable-length sequences: 1 marks real tokens, 0 marks padding that attention and the loss must ignore.",
        diagram=C("""
                       pos 0  1  2
            len 3  ->      1  1  1
            len 1  ->      1  0  0
            len 2  ->      1  1  0
            """),
        topic="ml-arrays", level=3),
    out(C("""
        import numpy as np
        g = np.zeros((4, 5))
        print(np.repeat(g[..., None], 3, axis=-1).shape, np.broadcast_to(g[..., None], (4, 5, 3)).strides)
        """),
        ["(4, 5, 3) (40, 8, 0)", "(4, 5, 3) (120, 24, 8)", "(4, 5, 1) (40, 8, 0)", "(12, 5) (40, 8, 0)"], 0,
        "One of these copies the channel three times; the other just pretends to.",
        "Both give a (4, 5, 3) 'RGB' version of a grayscale image. np.repeat allocates 3x the memory. broadcast_to "
        "uses stride 0 on the channel axis, so all three channels read the same bytes; it is read-only, which is "
        "fine for feeding a model and wrong if you later want to edit one channel.",
        topic="ml-arrays", level=3),
    out(C("""
        import numpy as np
        from numpy.lib.stride_tricks import sliding_window_view
        s = np.arange(6)
        X = sliding_window_view(s[:-1], 3)
        y = s[3:]
        print(X.shape, y.shape, X[-1], y[-1])
        """),
        ["(3, 3) (3,) [2 3 4] 5", "(4, 3) (3,) [3 4 5] 5", "(3, 3) (3,) [3 4 5] 5", "(3, 3) (4,) [2 3 4] 5"], 0,
        "Each window of 3 past values should predict the value right after it.",
        "Dropping the last value leaves 5 points, so 3 windows; the targets are s[3:], the value after each window. "
        "This is how you turn a time series into a supervised (X, y) dataset with zero copying. Off-by-one here "
        "leaks the target into the input window, and the model looks brilliant offline.",
        topic="ml-arrays", level=3),
    out(C("""
        import numpy as np
        seqs = [[1, 2], [3]]
        try:
            print(np.array(seqs))
        except ValueError:
            print("ValueError")
        """),
        ["ValueError", "[[1 2]\n [3 0]]", "[list([1, 2]) list([3])]", "[[1 2] [3]]"], 0,
        "Arrays must be rectangular.",
        "NumPy 2 refuses ragged nested lists (an inhomogeneous shape) instead of quietly making an object array "
        "as old versions did. Variable-length token sequences must be padded to a common length (plus a mask) "
        "before they can become one batch array.",
        analogy="Like a SQL table: every row needs the same columns, so short rows get NULL (padding) values.",
        topic="ml-arrays", level=3),
    out(C("""
        import numpy as np
        x = np.arange(6).reshape(3, 2)   # (time=3, batch=2)
        print(x.reshape(2, 3).tolist())
        print(x.T.tolist())
        """),
        ["[[0, 1, 2], [3, 4, 5]]\n[[0, 2, 4], [1, 3, 5]]", "[[0, 2, 4], [1, 3, 5]]\n[[0, 2, 4], [1, 3, 5]]",
         "[[0, 1, 2], [3, 4, 5]]\n[[0, 1, 2], [3, 4, 5]]", "[[0, 2, 4], [1, 3, 5]]\n[[0, 1, 2], [3, 4, 5]]"], 0,
        "Column 0 is sequence 0. Which result keeps its values together?",
        "Sequence 0 is 0, 2, 4. Only the transpose produces [0, 2, 4] as a row; reshape(2, 3) re-reads memory in order "
        "and mixes the two sequences. Shapes match so nothing errors: the RNN just trains on scrambled sequences. "
        "Rule: reshape regroups, transpose reorders axes.",
        diagram=C("""
            x (time, batch)     reshape(2,3)      x.T (batch, time)
            t0: 0 1             [0 1 2]           [0 2 4]  seq 0
            t1: 2 3             [3 4 5]           [1 3 5]  seq 1
            t2: 4 5             mixed!            correct
            """),
        topic="ml-arrays", level=4),
    out(C("""
        import numpy as np
        from numpy.lib.stride_tricks import sliding_window_view
        w = sliding_window_view(np.arange(5.0), 3)
        try:
            w -= w.mean(axis=1, keepdims=True)
        except ValueError:
            print("ValueError")
        """),
        ["ValueError", "Nothing: every window is centred in place", "[[-1. 0. 1.]]", "TypeError"], 0,
        "Overlapping windows share elements. What would writing to one do to its neighbours?",
        "sliding_window_view returns a read-only view: windows overlap, so an in-place write to one window would "
        "corrupt the others. Writing raises ValueError (assignment destination is read-only). Compute "
        "w - w.mean(...) into a new array instead.",
        topic="ml-arrays", level=4),
    ask("What is `X` after centring the training slice in place?", C("""
        import numpy as np
        X = np.arange(6.0)
        X_train = X[:4]
        X_train -= X_train.mean()
        print(X)
        """),
        ["[-1.5 -0.5  0.5  1.5  4.   5. ]", "[0. 1. 2. 3. 4. 5.]", "[-1.5 -0.5  0.5  1.5]",
         "[-2.5 -1.5 -0.5  0.5  1.5  2.5]"], 0,
        "Is X_train its own array?",
        "X[:4] is a view, so the in-place -= centres the first four rows of X itself. Any later code that re-splits "
        "X, or saves it, gets half-normalised data. Use X_train = X[:4].copy(), or the out-of-place "
        "X_train = X_train - mean.",
        analogy="Like passing a mutable object by reference to a 'pure' helper that mutates it: the caller's data changes too.",
        topic="ml-arrays", level=4),
    out(C("""
        import numpy as np
        probs = np.array([[0.2, 0.5, 0.3]])     # a batch of ONE prediction
        p = probs.squeeze()
        try:
            print(p.argmax(axis=1))
        except Exception as e:
            print(type(e).__name__)
        """),
        ["AxisError", "[1]", "1", "IndexError"], 0,
        "What did squeeze remove: just the size-1 axis you meant, or every one?",
        "squeeze() drops ALL length-1 axes, so a batch of one loses its batch axis and axis=1 no longer exists "
        "(AxisError, a subclass of ValueError and IndexError). Code that works for batch size 32 breaks at inference "
        "with batch size 1. Use squeeze(axis=0) or index explicitly.",
        analogy="Like an API that returns a bare object instead of a one-element list: the client's list handling breaks only when there's exactly one result.",
        topic="ml-arrays", level=4),
    fill("Which function checks EXACTLY whether two arrays have any bytes in common: `np.____(a, b)`?", "shares_memory",
         "Its cheaper cousin only compares memory bounds and is called may_...",
         "np.shares_memory solves the overlap exactly; np.may_share_memory only checks address ranges and can say True "
         "for interleaved views like a[::2] and a[1::2]. Use it in tests that assert a function returns a copy.",
         topic="views-copies", level=3),
    fill("Pad a sequence with two zeros on the right so it reaches the batch length: `np.____(seq, (0, 2))`", "pad",
         "A three-letter word for adding filler around data.",
         "np.pad(seq, (0, 2)) adds 0 values before (0) and after (2); the default mode is constant zeros. For a 2D "
         "batch, pass one (before, after) pair per axis, e.g. ((0, 0), (0, 2)) to pad only the time axis.",
         topic="ml-arrays", level=3),
    tf("`np.ascontiguousarray(a)` returns `a` itself, without copying, when `a` is already C-contiguous.", True,
       "It only does work when it has to.",
       "If the layout and dtype already match, you get the same object back (ascontiguousarray(a) is a is True). "
       "So it's cheap to call defensively before handing an array to a C extension, ONNX runtime or torch.from_numpy.",
       topic="memory-layout", level=3),
    tf("`np.random.default_rng(42)` and `np.random.default_rng(np.random.SeedSequence(42))` produce the same random stream.",
       True,
       "What does default_rng do with a plain int seed?",
       "default_rng wraps an int seed in a SeedSequence and feeds it to PCG64, so both calls give identical numbers. "
       "SeedSequence is the piece that hashes the seed into a well-mixed state and can spawn independent child "
       "seeds, e.g. one per data-loader worker, so passing a SeedSequence around is the scalable version of 'seed 42'.",
       topic="creating", level=4),
    tf("`x.reshape(len(x), -1)` and `x.reshape(-1, x.shape[1] * x.shape[2])` give the same result for an image batch `x` of shape (N, H, W).",
       True,
       "Both keep N rows of H*W numbers each.",
       "Both produce (N, H*W) with each image flattened into its own row, because C-order reshape keeps the first "
       "axis intact. The bug is reshape(H*W, -1) or reshape(-1, N), which slice across images. Prefer the "
       "len(x) form: it doesn't hard-code the image size.",
       topic="reshaping", level=3),
    tf("Transposing a (10000, 10000) array with `a.T` takes time proportional to the number of elements.", False,
       "What actually changes: the bytes or the metadata?",
       "a.T only swaps the shape and strides tuples: O(1), no data moved. The cost shows up later if you need a "
       "contiguous copy (np.ascontiguousarray, reshape of the transpose) or if you iterate along the now-strided axis.",
       diagram=C("""
           a   : shape (10000, 10000) strides (80000, 8)
           a.T : shape (10000, 10000) strides (8, 80000)
                 same buffer, two numbers swapped
           """),
       topic="memory-layout", level=3),
    tf("`torch.from_numpy(a[::-1])` works, because PyTorch tensors share NumPy's stride model.", False,
       "Look at the sign of the stride.",
       "a[::-1] has a negative stride, and PyTorch tensors don't support negative strides, so from_numpy raises "
       "ValueError and suggests a copy. Positive steps like a[::2] are fine (stride 2, still zero-copy). This bites "
       "image code that flips with img[:, ::-1] (or OpenCV's BGR -> RGB via [..., ::-1]) right before the model.",
       diagram=C("""
           a        : strides (8,)     start at a[0]
           a[::2]   : strides (16,)    ok for torch
           a[::-1]  : strides (-8,)    start at a[-1]
                      torch.from_numpy -> ValueError
           """),
       topic="memory-layout", level=4),
    tf("`a[a > 0] += 1` increments every positive element exactly once, unlike `a[idx] += 1` with repeated indices.",
       True,
       "Can a boolean mask select the same element twice?",
       "A boolean mask picks each position at most once, so the buffered read-add-write of fancy += is harmless "
       "and every positive element goes up by 1. The 'only once' surprise needs repeated integer indices, where "
       "np.add.at is the fix.",
       code=C("""
           import numpy as np
           a = np.array([1, -2, 3])
           a[a > 0] += 1
           print(a)
           """),
       topic="masks-fancy", level=3),
    tf("For an int8 array `a`, `a.astype(np.int64) + a.astype(np.int64)` cannot overflow for any values a can hold.", True,
       "What is the largest possible sum of two int8 values?",
       "int8 values are in [-128, 127], so sums are in [-256, 254], far inside int64. Widening BEFORE the arithmetic "
       "is the general fix for uint8/int8 overflow; widening after (e.g. (a + a).astype(np.int64)) only preserves the "
       "already-wrapped result.",
       topic="dtypes", level=3),
    fill("A float16's largest finite value is ____ (exact integer).", "65504",
         "Just under 2**16.",
         "np.finfo(np.float16).max is 65504. Anything rounding above it becomes inf, which is why fp16 training "
         "uses loss scaling and why bf16 (float32's range) is popular.",
         topic="dtypes", level=3),
    fill("Which stride_tricks function gives a safe, read-only view of all length-k windows: `np.lib.stride_tricks.____(a, k)`?",
         "sliding_window_view",
         "It literally slides a window.",
         "sliding_window_view(a, k) returns shape (len(a) - k + 1, k) as a stride trick: no copy, read-only. "
         "Use it for rolling features and 1D convolutions instead of hand-written as_strided.",
         topic="memory-layout", level=3),
    fill("To turn a C-ordered (N, H, W, C) batch into (N, C, H, W) you call `x.____(0, 3, 1, 2)`.", "transpose",
         "Not reshape: you're reordering axes, not regrouping elements.",
         "x.transpose(0, 3, 1, 2) (or np.moveaxis(x, -1, 1)) moves the channel axis to position 1 as a view. "
         "reshape would give the right shape and the wrong pixels.",
         diagram=C("""
             axes  : N  H  W  C      (0, 1, 2, 3)
             order : 0  3  1  2  ->  N  C  H  W
             """),
         topic="ml-arrays", level=3),
    fill("Which NumPy function turns a list of equal-shape (H, W) images into ONE (N, H, W) batch, adding a new first axis: `np.____(images)`?",
         "stack",
         "concatenate joins along an existing axis; this one creates one.",
         "np.stack(images) adds axis 0 by default. np.concatenate(images) would join along rows and give (N*H, W), "
         "losing the image boundaries.",
         topic="ml-arrays", level=2),

    # ============================================================ Round 3: conceptual mix
    # ------------------------------------------------------------------ why-arrays
    mcq("People say NumPy code should be \"vectorised\". What does that mean?",
        ["You write one operation on the whole array (like `a * 2`) and NumPy runs the loop in compiled code",
         "You split the array across CPU cores by hand before doing any maths",
         "You convert the array into a Python list of vectors first",
         "You write a `for` loop, but over `range(len(a))` instead of over the items"], 0,
        "Who writes the loop: you, or NumPy?",
        "Vectorised means expressing the work as whole-array operations, so the per-element loop runs in C "
        "instead of the Python interpreter. It is not about multithreading: most element-wise ops run on one "
        "core and are still 10-100x faster than a Python loop. In interviews, 'replace the loop with array ops' "
        "is the expected first optimisation.",
        analogy="Like one SQL `UPDATE prices SET p = p * 2` instead of fetching every row into your app, "
                "changing it and saving it back one at a time.",
        topic="why-arrays", level=1),
    tf("`np.array([1, 2, 3]) + [10, 20, 30]` adds element by element, because NumPy converts the list to an array first.",
       True,
       "When one side of + is an ndarray, whose rules apply?",
       "If either operand is an ndarray, NumPy turns the other into an array and adds element-wise: [11 22 33]. "
       "Only list + list concatenates. The convenience hides a cost: the list is converted on every call, so "
       "convert once up front in hot code.",
       topic="why-arrays", level=2),
    mcq("A teammate wraps a Python function with `f = np.vectorize(slow_fn)` and expects a big speed-up on a million elements. What actually happens?",
        ["It is still a Python-level loop calling `slow_fn` per element, so it is roughly as slow as a list comprehension",
         "NumPy compiles `slow_fn` to C, so it runs as fast as built-in ufuncs",
         "It runs `slow_fn` on all CPU cores in parallel",
         "It raises unless `slow_fn` already uses only NumPy operations"], 0,
        "Read the docs' own warning about np.vectorize.",
        "np.vectorize is a convenience for broadcasting and output shaping; the docs say it is essentially a for "
        "loop. Real speed comes from rewriting the body with array ops (np.where, ufuncs, masks) or using numba. "
        "On a million ints it is typically dozens of times slower than the equivalent `arr * 2`.",
        analogy="Like wrapping a synchronous function in an `async` signature: the call looks modern, but the "
                "work underneath is exactly as sequential as before.",
        topic="why-arrays", level=3),
    mcq("Why is `[x + 1 for x in arr]` over a NumPy array usually SLOWER than the same comprehension over a Python list?",
        ["Each element read from the array has to be boxed into a new NumPy scalar object, while a list already holds Python objects",
         "NumPy arrays are stored on disk and each element read goes to disk",
         "Iterating a NumPy array copies the whole array once per element",
         "It isn't: element-wise Python loops are always faster on arrays"], 0,
        "What object does `for x in arr` hand you on each step?",
        "An array stores raw machine numbers, so every iteration creates a fresh np.int64 object and the + goes "
        "through NumPy's scalar machinery. A list just hands back pointers to existing ints. The array only wins "
        "when you stop looping in Python: `arr + 1`. Mixing the two (arrays with Python loops) gets the worst of both.",
        diagram=C("""
            list : [ptr]->int  [ptr]->int   loop reads pointers
            array: |8B|8B|8B|8B|            loop must box each:
                    |  -> np.int64 object (new every step)
            """),
        topic="why-arrays", level=4),

    # ------------------------------------------------------------------ creating
    tf("`np.arange(1, 5)` includes the number 5.", False,
       "Same rule as Python's range().",
       "arange follows range(): the stop value is excluded, so you get [1 2 3 4]. linspace is the one that "
       "includes its stop by default. Off-by-one bugs in bin edges and epoch counters often come from mixing "
       "the two conventions.",
       topic="creating", level=1),
    mcq("You need exactly 11 evenly spaced points from 0 to 1 inclusive (0.0, 0.1, ..., 1.0). Which call is the reliable choice?",
        ["np.linspace(0, 1, 11)",
         "np.arange(0, 1.1, 0.1)",
         "np.arange(0, 1, 0.1)",
         "np.linspace(0, 1, 10)"], 0,
        "Do you want to fix the step, or the number of points?",
        "linspace fixes the count and includes the end point, so you always get 11 values. arange with a float "
        "step can gain or lose a point because 0.1 is not exact in binary; arange(0, 1, 0.1) also stops before 1. "
        "linspace(0, 1, 10) gives a step of 1/9, the classic fence-post mistake.",
        topic="creating", level=2),
    fill("Give each of 4 data-loader workers its own independent random stream: `children = np.random.SeedSequence(42).____(4)`, then `default_rng(child)` per worker.",
         "spawn",
         "The word for creating offspring.",
         "SeedSequence.spawn(n) derives n child seeds that are statistically independent but fully reproducible "
         "from 42. Seeding workers with 42, 43, 44 is the naive version and gives no independence guarantee. "
         "Generator.spawn(n) does the same directly from an existing rng.",
         analogy="Like deriving per-service keys from one master key with a KDF instead of hand-picking "
                 "key1, key2, key3.",
         topic="creating", level=4),

    # ------------------------------------------------------------------ attributes
    fill("Which attribute gives the total number of elements in an array (the product of its shape): `a.____`?",
         "size",
         "Not len(): that only counts the first axis.",
         "a.size multiplies the shape out, so a (3, 4) array has size 12. len(a) would give 3, the length of "
         "axis 0. Use size when you need element counts, e.g. to compute memory as a.size * a.itemsize.",
         topic="attributes", level=1),
    mcq("`big = np.zeros(1_000_000)` and `v = big[:10]`. Why does `sys.getsizeof(v)` report only about 112 bytes?",
        ["v is a view: getsizeof counts only its header, not the buffer it borrows from big",
         "NumPy compresses the zeros, so ten of them take almost no space",
         "getsizeof always ignores the data of NumPy arrays, even for big itself",
         "The slice is lazy and no memory is reserved until you read it"], 0,
        "Who owns the data buffer?",
        "getsizeof includes the data only when the array owns it (big reports about 8 MB), while a view reports "
        "just its ~112-byte object header. Neither tells you the real story: v keeps all 8 MB alive. For memory "
        "profiling use a.nbytes for the logical size and check a.base to see what a view is pinning.",
        topic="attributes", level=3),
    tf("`b = np.broadcast_to(np.arange(1000.0), (1000, 1000))` reports `b.nbytes == 8_000_000`, even though only 8,000 bytes of data exist.",
       True,
       "Is nbytes measured from the buffer, or from shape times itemsize?",
       "nbytes is just size * itemsize, a logical number. The broadcast view has strides (0, 8), so every row "
       "re-reads the same 1000 floats. Memory dashboards that sum nbytes over-count such views; the moment you "
       "call b.copy() or do b + 1, the 8 MB becomes real.",
       diagram=C("""
           buffer : [x0 x1 ... x999]          8,000 bytes
           b      : shape (1000, 1000) strides (0, 8)
           row 0 --> same buffer
           row 1 --> same buffer   nbytes says 8,000,000
           """),
       topic="attributes", level=4),

    # ------------------------------------------------------------------ dtypes
    tf("`np.zeros(3)` and `np.ones(3)` give float arrays unless you pass a `dtype`.", True,
       "Do the values look like 0 or 0.?",
       "zeros, ones and eye default to float64, so they print as [0. 0. 0.]. If you use one as an index array "
       "or a counter you need dtype=int (or np.zeros_like on an int array); otherwise indexing with it raises "
       "IndexError because floats are not valid indices.",
       topic="dtypes", level=1),
    fill("`np.array([4, 6]) / 2` gives float64 even for an int array. Which operator keeps the result as integers? `a ____ 2`",
         "//",
         "Python 3 has two division operators.",
         "/ is true division and always returns floats; // is floor division and keeps int64. Note it floors, "
         "so -7 // 2 is -4, not -3. Mixing them up is a common reason a bucket or index array suddenly "
         "becomes float and breaks indexing.",
         topic="dtypes", level=2),
    mcq("`x` is a float32 batch. Under NumPy 2's promotion rules (NEP 50), which expression silently returns float64 and doubles the memory?",
        ["x * np.float64(0.5)",
         "x * 0.5",
         "x / 255",
         "x + np.float32(1)"], 0,
        "Python scalars are 'weak'; are NumPy scalars?",
        "Plain Python numbers (0.5, 255) adopt the array's dtype, so those stay float32. A NumPy scalar like "
        "np.float64(0.5), or a 0-d float64 array, is 'strong' and promotes the result to float64. These often "
        "sneak in from np.mean() or np.sqrt() of a float64 config value, and the model input quietly doubles in size.",
        code=C("""
            import numpy as np
            x = np.ones(3, dtype=np.float32)
            scale = np.float64(0.5)      # e.g. read from a float64 stats array
            print(x.dtype)
            """),
        topic="dtypes", level=3),
    mcq("For a uint8 image `u = np.array([200, 100], dtype=np.uint8)`, `u + u` wraps to `[144 200]`, but `u.sum()` correctly gives 300. Why?",
        ["sum() uses a wider accumulator (uint64 here) for small integer types, while + keeps the uint8 dtype",
         "sum() converts to float64 first, like mean() does",
         "sum() detects the overflow and retries in a bigger type",
         "Python ints are used inside sum(), so it can never overflow"], 0,
        "Check the dtype of u.sum().",
        "Reductions like sum and prod upcast small ints to the platform integer (int64, or uint64 for unsigned), "
        "so u.sum() is a uint64 300. Element-wise + has no such rule, so it wraps mod 256. The trap is "
        "assuming 'sum is safe' means 'arithmetic is safe': widen before element-wise maths on images.",
        topic="dtypes", level=3),
    mcq("What dtype does NumPy produce for `np.result_type(np.int64, np.uint64)`, and why?",
        ["float64, because no integer type can hold every int64 and every uint64 value",
         "int64, because signed types always win",
         "uint64, because the unsigned type is listed second",
         "int128, the next wider integer"], 0,
        "What range would a common integer type need?",
        "Promotion picks the smallest type that can represent both inputs. Covering -2**63 to 2**64-1 needs 65 "
        "bits and NumPy has no int128, so it falls back to float64, which loses exactness above 2**53. Mixing "
        "uint64 ids or hashes with int64 offsets can silently corrupt them this way.",
        topic="dtypes", level=4),

    # ------------------------------------------------------------------ indexing
    tf("For `a = np.arange(10)`, `a[5:2]` raises an IndexError because the start is after the stop.", False,
       "Slices are forgiving; single indexes are not.",
       "A slice whose start is past its stop (with a positive step) is simply empty: shape (0,). Slices never "
       "raise for out-of-range bounds; only integer indexes like a[10] do. Empty slices are a quiet source of "
       "bugs: a .mean() on them gives nan with a warning rather than failing loudly.",
       topic="indexing", level=2),
    mcq("A helper returns the last k values with `a[-k:]`. What goes wrong when k == 0?",
        ["-0 is 0, so a[-0:] is a[0:] and it returns the WHOLE array instead of nothing",
         "It raises IndexError because -0 is not a valid index",
         "It returns an empty array, which is correct",
         "It returns only the last element"], 0,
        "What is -0 as a Python int?",
        "Python ints have no negative zero, so a[-0:] means 'from index 0 to the end'. The safe form is "
        "a[len(a) - k:], which gives an empty slice for k = 0. This shows up in 'last k tokens / last k "
        "checkpoints' code where k is computed and can hit zero.",
        diagram=C("""
            a      = [0 1 2 3 4 5 6 7 8 9]
            k = 3 : a[-3:]       -> [7 8 9]
            k = 0 : a[-0:]=a[0:] -> [0 1 2 ... 9]   whole array
            fix   : a[len(a)-k:] -> []              empty
            """),
        topic="indexing", level=4),

    # ------------------------------------------------------------------ masks-fancy
    mcq("You need a NEW array with negatives replaced by 0, leaving `a` untouched. Which is correct?",
        ["np.where(a < 0, 0, a)",
         "a[a < 0] = 0",
         "a[a >= 0]",
         "np.where(a < 0)"], 0,
        "One of these mutates, one drops elements, one returns positions.",
        "np.where(cond, x, y) builds a fresh array choosing x where cond is True and y elsewhere (np.maximum(a, 0) "
        "or np.clip(a, 0, None) also work). a[a < 0] = 0 edits a in place, a[a >= 0] removes elements and changes "
        "the length, and np.where with one argument returns index arrays, not values.",
        topic="masks-fancy", level=2),
    mcq("`a = np.array([1, 0, 3])` is an int array of flags. A teammate writes `a[~a]` to select the zero entries. Why is that a bug?",
        ["On integers ~ is bitwise NOT, so ~a is [-2 -1 -4]: an index array, not a mask",
         "~ only works on float arrays and raises TypeError on ints",
         "~a gives [False True False], which is exactly the zero entries",
         "~ flips the array's order, like a[::-1]"], 0,
        "~ means 'not' only for booleans.",
        "~x on an int is -x - 1, so a[~a] fancy-indexes positions -2, -1, -4 (the last one raises IndexError on "
        "a 3-element array). Make it boolean first: a[~a.astype(bool)] or a[a == 0]. Pandas users hit this when "
        "a 0/1 column is used as a mask.",
        topic="masks-fancy", level=3),
    mcq("Why does `a[a > 2 & a < 9]` raise ValueError even though the author used `&` instead of `and`?",
        ["& binds tighter than >, so it parses as `a > (2 & a) < 9`, a chained comparison that calls bool() on an array",
         "& cannot combine two boolean arrays; you need np.logical_and",
         "The mask has a different length than a",
         "Comparisons inside [] are not allowed; build the mask on its own line first"], 0,
        "Think about operator precedence in Python.",
        "In Python, & has higher precedence than comparisons, so 2 & a is computed first and the result is a "
        "chained comparison a > b < 9, which needs bool() of an array: ambiguous truth value. Always bracket "
        "each condition: a[(a > 2) & (a < 9)]. Linters will not catch this; only the brackets do.",
        diagram=C("""
            written : a > 2 & a < 9
            parsed  : a > (2 & a) < 9
                    = (a > b) and (b < 9)   # chained -> bool(array)
            fix     : (a > 2) & (a < 9)
            """),
        topic="masks-fancy", level=3),

    # ------------------------------------------------------------------ views-copies
    mcq("In Python, `lst[:]` is the idiom for copying a list. What does `s = a[:]` give you for a NumPy array `a`?",
        ["A view: a new array object over the same data, so `s[0] = 9` also changes `a`",
         "An independent copy, exactly like the list idiom",
         "The very same object, so `s is a` is True",
         "A read-only snapshot of `a`"], 0,
        "NumPy slicing never copies data.",
        "a[:] is a basic slice, so it returns a view: s is a different object (s is a is False) but shares the "
        "buffer. Habits carried over from lists cause 'I copied it, why did the original change?' bugs. When you "
        "need a real copy, say so: a.copy().",
        analogy="list[:] is a shallow clone; ndarray[:] is a second reference to the same database row, "
                "just with its own cursor.",
        diagram=C("""
            lst[:] : [1,2,3]  ->  [1,2,3]    new storage
            a[:]   : a --+
                         +--> |1|2|3|        one buffer
                     s --+
            """),
        topic="views-copies", level=2),
    mcq("`a = np.arange(6).reshape(2, 3)`. Both `a[:, [0]]` and `a[:, 0:1]` have shape (2, 1). Which one is a view of `a`?",
        ["a[:, 0:1]: a slice is basic indexing; the list [0] triggers fancy indexing, which copies",
         "a[:, [0]]: a list of one index is turned into a slice automatically",
         "Both, because they select the same elements",
         "Neither, because selecting a column always copies"], 0,
        "Same shape does not mean same mechanism.",
        "Whether you get a view depends on the kind of index, not the result's shape. Any list or integer array "
        "means fancy indexing and a copy, so writes into a[:, [0]] are lost. If you plan to modify a column in "
        "place, use the slice form, and confirm with np.shares_memory when in doubt.",
        topic="views-copies", level=3),
    mcq("A function returns an internal cached array `self._table`. What is the cheapest way to stop callers from mutating your cache by accident?",
        ["Return a view with `v.flags.writeable = False`: zero-copy, and writes through it raise ValueError",
         "Return `self._table.copy()` on every call",
         "Return `tuple(self._table)` so it is immutable",
         "Wrap it in `np.asarray(self._table)`"], 0,
        "You want read-only access, not a duplicate.",
        "v = self._table.view(); v.flags.writeable = False shares the buffer but any v[...] = x raises "
        "'assignment destination is read-only'. A copy per call is safe but costs O(n) memory and time; "
        "np.asarray returns the same writable object. Note the view still sees later updates you make to the cache.",
        analogy="Like exposing a read-only interface (or a frozen DTO) to callers instead of cloning the whole "
                "object for each request.",
        topic="views-copies", level=3),
    tf("`x.astype(np.float64, copy=False)` returns `x` itself, with no copy, when `x` is already float64.", True,
       "astype copies by default; what does copy=False change?",
       "With copy=False, astype skips the copy if the dtype already matches, returning the same object. "
       "That makes it a cheap 'ensure float64' guard at the top of a function. Without the flag, astype always "
       "allocates, which adds up when called on every batch.",
       topic="views-copies", level=3),

    # ------------------------------------------------------------------ reshaping
    mcq("`M` has shape (3, 4) and `c` holds one value per ROW, shape (3,). `M + c` raises. Which fix adds `c` row-wise?",
        ["M + c[:, None]  (c becomes a (3, 1) column)",
         "M + c[None, :]",
         "M + c.T",
         "M + c.repeat(4)"], 0,
        "Broadcasting lines shapes up from the right.",
        "Broadcasting compares trailing axes: (3, 4) vs (3,) puts 3 against 4 and fails. c[:, None] makes it "
        "(3, 1), which stretches across the 4 columns. c.T does nothing on a 1D array, (1, 3) still clashes with 4, and "
        "repeat(4) gives a flat (12,). Per-row normalisation (e.g. dividing by row sums) needs exactly this.",
        diagram=C("""
            M        : (3, 4)
            c        :    (3,)    -> 3 vs 4: error
            c[:,None]: (3, 1)     -> 1 stretches to 4
            result   : (3, 4)
            """),
        topic="reshaping", level=2),
    mcq("In multi-head attention, `x` has shape (B, T, H*D). Which gives per-head tensors of shape (B, H, T, D) with the RIGHT values?",
        ["x.reshape(B, T, H, D).transpose(0, 2, 1, 3)",
         "x.reshape(B, H, T, D)",
         "x.reshape(B, T, H, D).reshape(B, H, T, D)",
         "x.transpose(0, 2, 1).reshape(B, H, T, D)"], 0,
        "First split the last axis, then move axes.",
        "The H*D numbers for each token are contiguous, so reshape can only split that last axis into (H, D); "
        "putting H in front of T needs a transpose. reshape(B, H, T, D) gives the right shape but mixes tokens "
        "into heads, a bug that trains without errors and just performs worse.",
        diagram=C("""
            (B, T, H*D) --reshape--> (B, T, H, D)   split last axis
                        --transpose(0,2,1,3)--> (B, H, T, D)
            reshape(B, H, T, D) directly: right shape,
            but head 1 gets token 0's second half, etc.
            """),
        topic="reshaping", level=4),
    fill("Which method flattens an array to 1D and returns a view whenever the layout allows (copying only when it must): `a.____()`?",
         "ravel",
         "flatten always copies; its sibling doesn't.",
         "ravel() returns a view for contiguous arrays and copies only for awkward layouts like a.T; flatten() "
         "always copies. Prefer ravel or reshape(-1) for read-only work; prefer flatten when you will modify the "
         "result and must not touch the original.",
         topic="reshaping", level=2),

    # ------------------------------------------------------------------ stack-split
    fill("Which function splits an array into n nearly equal parts without raising when the length doesn't divide evenly: `np.____(a, 3)`?",
         "array_split",
         "np.split refuses uneven sections.",
         "np.array_split(np.arange(10), 3) gives parts of length 4, 3, 3, while np.split raises ValueError. "
         "Handy for sharding work across processes when the row count isn't a multiple of the worker count.",
         topic="stack-split", level=2),
    tf("The pieces returned by `np.split(a, [3, 7])` are views of `a`, so writing into a piece changes `a`.", True,
       "Can each piece be described as a slice?",
       "np.split just slices along the axis, so each part is a view sharing a's buffer (np.shares_memory is True). "
       "If you split a dataset into train/val/test and then normalise one part in place, the original array "
       "changes too. Copy the part first if it must be independent.",
       topic="stack-split", level=3),
    tf("`s = np.stack([a, b])` returns a view that still shares memory with `a` and `b`.", False,
       "Can two separate buffers become one array without moving bytes?",
       "An ndarray needs ONE buffer with regular strides, and a and b live in separate allocations, so stack "
       "(like concatenate, vstack, hstack) always allocates and copies. Stacking inside a training loop therefore "
       "costs O(batch size) memory traffic each time; preallocate and fill slices if it shows up in a profile.",
       topic="stack-split", level=4),

    # ------------------------------------------------------------------ memory-layout
    mcq("An algorithm reads a huge (n, n) float64 matrix one COLUMN at a time, thousands of times. What layout change helps most?",
        ["Convert once with np.asfortranarray(a) so each column is contiguous in memory",
         "Call a.T inside the loop so the columns become rows",
         "Convert to a Python list of lists for faster column access",
         "Nothing: memory layout never affects NumPy speed"], 0,
        "In which order do C-ordered elements sit in memory?",
        "In C order the elements of one column are n * 8 bytes apart, so each read pulls in a cache line mostly "
        "wasted. One O(n^2) conversion to Fortran order makes every column a contiguous run. a.T inside the loop "
        "is free but changes nothing physical: its rows are still the same scattered bytes.",
        diagram=C("""
            C order : row0 | row1 | row2      column j = every n-th
                      a0 a1 a2 | b0 b1 b2      a1 . . b1 . . c1
            F order : col0 | col1 | col2      column j = one run
                      a0 b0 c0 | a1 b1 c1      a1 b1 c1
            """),
        analogy="Like choosing a column store (Parquet) over a row store (CSV) when every query aggregates one column.",
        topic="memory-layout", level=3),
    tf("A 1-D contiguous array like `np.arange(5.0)` reports BOTH `C_CONTIGUOUS` and `F_CONTIGUOUS` as True.", True,
       "With one axis, is there any difference between 'last index fastest' and 'first index fastest'?",
       "With a single axis both orders describe the same layout, so both flags are True (the same holds for "
       "shapes like (3, 1) where only one axis has length > 1). Code that branches on 'C or F?' must handle "
       "'both', and checks like `not a.flags.f_contiguous` to mean 'C order' break on vectors.",
       topic="memory-layout", level=4),

    # ------------------------------------------------------------------ special-values
    fill("Which function returns a boolean mask of the NaN entries in `a`: `np.____(a)`?",
         "isnan",
         "a == np.nan never works.",
         "np.isnan(a) is True exactly where a holds NaN, because NaN is not equal to anything, itself included. "
         "Count missing values with np.isnan(a).sum() and drop them with a[~np.isnan(a)].",
         topic="special-values", level=1),
    mcq("A hand-written binary cross-entropy `-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()` returns nan when one prediction is exactly 0.0 and its label is 0. Why?",
        ["np.log(0) is -inf, and 0 * -inf is nan, which then poisons the mean",
         "np.log raises on 0, and NumPy converts the exception to nan",
         "The mean of any array containing 0 is nan",
         "y and p have different dtypes, so the product is undefined"], 0,
        "Evaluate y * log(p) for y = 0, p = 0 step by step.",
        "log(0) gives -inf (with a warning), and IEEE says 0 * inf is nan; one nan makes the whole mean nan. "
        "Frameworks avoid this by clipping, e.g. p = np.clip(p, 1e-7, 1 - 1e-7), or by computing from logits. "
        "A loss that turns nan after hours of training is very often this.",
        analogy="Like SQL NULL: one NULL in an arithmetic expression makes the whole result NULL.",
        topic="special-values", level=3),
    mcq("Two result arrays both contain NaN in the same positions. Which check correctly reports them as equal in a unit test?",
        ["np.array_equal(a, b, equal_nan=True)",
         "np.array_equal(a, b)",
         "(a == b).all()",
         "np.allclose(a, b)"], 0,
        "By default, NaN is never equal to NaN.",
        "The default array_equal, ==, and allclose all treat NaN != NaN, so identical arrays with a NaN compare "
        "False. Pass equal_nan=True (array_equal or allclose), or use np.testing.assert_array_equal, which treats "
        "NaNs in the same places as equal and gives a readable diff.",
        topic="special-values", level=2),
    tf("In NumPy 2, `np.unique(np.array([np.nan, 1.0, np.nan]))` returns ONE nan, not two.", True,
       "Check the equal_nan parameter of np.unique.",
       "Since NumPy 1.21, np.unique has equal_nan=True by default, so all NaNs collapse into a single trailing "
       "nan: [1. nan]. Pass equal_nan=False for the old behaviour. This matters when you count categories: a "
       "column with 1,000 missing values contributes just one 'nan' category.",
       topic="special-values", level=4),

    # ------------------------------------------------------------------ ml-arrays
    mcq("A batch of 32 grayscale images, each 28 x 28 pixels, is stored in one array. What shape does it have by convention?",
        ["(32, 28, 28)", "(28, 28, 32)", "(28, 28)", "(32, 784, 1)"], 0,
        "The batch axis comes first.",
        "ML code puts the sample (batch) axis first, then the per-sample shape, so 32 images of 28 x 28 are "
        "(32, 28, 28). With an explicit channel axis it becomes (32, 28, 28, 1) or (32, 1, 28, 28). Putting the "
        "batch last makes every slicing and reshape step harder.",
        topic="ml-arrays", level=1),
    mcq("`X` has shape (n_samples, n_features). Which line computes the per-FEATURE mean for standardising?",
        ["X.mean(axis=0)  -> shape (n_features,)",
         "X.mean(axis=1)  -> shape (n_samples,)",
         "X.mean()        -> one number",
         "X.mean(axis=-1) -> shape (n_features,)"], 0,
        "axis=k means 'collapse axis k'.",
        "axis=0 collapses the rows, giving one mean per column (feature), which then broadcasts in X - mu. "
        "axis=1 averages each sample's features, which is meaningless for standardisation. Remember: the axis "
        "you name is the one that disappears.",
        topic="ml-arrays", level=2),
    mcq("You must shuffle features `X` and labels `y` while keeping each row matched to its label. Which approach is correct?",
        ["idx = rng.permutation(len(X)); X, y = X[idx], y[idx]",
         "rng.shuffle(X); rng.shuffle(y)",
         "X = rng.permutation(X); y = rng.permutation(y)",
         "np.random.shuffle(X); y stays in the original order"], 0,
        "Draw ONE permutation and apply it to both.",
        "One index permutation applied to both arrays keeps pairs aligned. Two separate shuffles use different "
        "random orders, so labels get scrambled and the model learns noise (accuracy near chance is the tell). "
        "The fancy index also returns copies, so the originals are left unshuffled.",
        analogy="Like sorting two parallel arrays in JavaScript: sort the indices once and reorder both, "
                "never sort each array on its own.",
        topic="ml-arrays", level=2),
    mcq("A regression model outputs `pred` with shape (N, 1); the targets `y` have shape (N,). What does `((pred - y) ** 2).mean()` compute?",
        ["The mean over an (N, N) matrix of every prediction minus every target, not the MSE",
         "The correct MSE, because NumPy aligns the two automatically",
         "A ValueError, because the shapes differ",
         "An (N, 1) array of squared errors"], 0,
        "Line the shapes up from the right and stretch the 1s.",
        "(N, 1) - (N,) broadcasts to (N, N): every prediction is compared with every target. No error is raised "
        "and the number looks plausible, so training just goes badly. Fix the shapes: pred.reshape(-1) or "
        "pred[:, 0], or make y a column with y[:, None]. Asserting shapes in the loss function catches it.",
        diagram=C("""
            pred : (N, 1)
            y    :    (N,)  -> treated as (1, N)
            diff : (N, N)   all pairs, N^2 numbers
            fix  : pred[:, 0] - y  -> (N,)
            """),
        topic="ml-arrays", level=3),
]
