from helpers import mcq, tf, out, fill

SUBJECT = "py-conditions"

TOPICS = [
    ("comparisons", "Comparison operators and chaining"),
    ("truthiness", "Truthy and falsy values"),
    ("logic-ops", "and / or / not, short-circuit"),
    ("identity", "is vs ==, None checks"),
    ("ternary", "Conditional expressions"),
    ("match-case", "Structural pattern matching"),
    ("precedence", "Operator precedence"),
    ("any-all", "any() and all()"),
    ("if-structure", "if / elif / else and guard clauses"),
    ("type-checks", "isinstance and type checks"),
    ("ml-patterns", "Conditions in ML code: thresholds, masks, early stopping"),
]

QUESTIONS = [
    # ---------------------------------------------------------------- level 1
    out('print(5 >= 5, 3 != 3)',
        ["True False", "False False", "True True", "False True"], 0,
        ">= means 'greater than OR equal'.",
        "5 >= 5 is True because they're equal; 3 != 3 ('not equal') is False.",
        topic="comparisons", level=1),
    out('age = 20\nprint(age > 18)',
        ["True", "False", "20", "age > 18"], 0,
        "A comparison is a question with a yes/no answer.",
        "Comparisons evaluate to a bool: 20 > 18 is True.",
        topic="comparisons", level=1),
    out('name = "ravi"\nprint(name == "Ravi")',
        ["False", "True", "None", "TypeError"], 0,
        "Is 'r' the same character as 'R'?",
        "String comparison is case-sensitive, so 'ravi' and 'Ravi' are different. Compare name.lower() == 'ravi' to ignore case.",
        topic="comparisons", level=1),
    mcq("Which of these values counts as False in an `if`?",
        ["0", "'hello'", "[1]", "-1"], 0,
        "Think 'zero or empty'.",
        "0 is falsy. Non-empty strings, non-empty lists and any non-zero number (even -1) are truthy.",
        topic="truthiness", level=1),
    out('name = ""\nif name:\n    print("hi", name)\nelse:\n    print("no name")',
        ["no name", "hi", "hi ", "Error"], 0,
        "What is the truth value of an empty string?",
        "An empty string is falsy, so the else branch runs. `if name:` is the Python way to say 'if name is not empty'.",
        topic="truthiness", level=1,
        diagram="""
 falsy:   False  None  0  0.0  ""  []  {}  ()  set()
 truthy:  everything else, e.g. "0"  " "  [0]  -1
"""),
    out('print(bool(None), bool(42))',
        ["False True", "True True", "None 42", "False False"], 0,
        "bool() asks 'is this truthy?'",
        "None is falsy; any non-zero number is truthy.",
        topic="truthiness", level=1),
    out('is_admin = False\nprint(not is_admin)',
        ["True", "False", "None", "not False"], 0,
        "not flips the value.",
        "not False is True. Python spells it `not`, where JS and Java use `!`.",
        topic="logic-ops", level=1,
        analogy="`and` is like `&&`, `or` is like `||`, `not` is like `!` in JS/Java, just written as words."),
    out('has_ticket = True\nhas_id = False\nprint(has_ticket and has_id, has_ticket or has_id)',
        ["False True", "True True", "False False", "True False"], 0,
        "and needs both; or needs at least one.",
        "True and False -> False; True or False -> True.",
        topic="logic-ops", level=1,
        diagram="""
  a      b     | a and b | a or b
  True   True  |  True   |  True
  True   False |  False  |  True
  False  True  |  False  |  True
  False  False |  False  |  False
"""),
    out('result = None\nif result is None:\n    print("nothing yet")',
        ["nothing yet", "None", "Nothing is printed", "SyntaxError"], 0,
        "`is None` asks 'is this the None object?'",
        "result is None is True, so the message prints. `x is None` is the standard None check (like `x === null` in JS).",
        topic="identity", level=1),
    mcq("What is the recommended way to check if a variable `x` is None?",
        ["if x is None:", "if x == None:", "if x = None:", "if None(x):"], 0,
        "None is a single, unique object.",
        "`is None` checks identity with the one None object. `== None` usually works but can be fooled by custom classes; `x = None` is an assignment and a SyntaxError in an if.",
        topic="identity", level=1),
    out('temp = 30\nlabel = "hot" if temp > 25 else "mild"\nprint(label)',
        ["hot", "mild", "True", "hot mild"], 0,
        "Read it as: 'hot' if (temp > 25), otherwise 'mild'.",
        "This is Python's one-line if/else (like JS temp > 25 ? 'hot' : 'mild'). 30 > 25, so 'hot'.",
        topic="ternary", level=1),
    fill("Fill in the keyword: `status = 'pass' if score >= 50 ____ 'fail'`", "else",
         "Same word as in a normal if/else block.",
         "A conditional expression is `a if condition else b`; the else part is required.",
         topic="ternary", level=1),
    out('marks = 72\nif marks >= 90:\n    print("A")\nelif marks >= 70:\n    print("B")\nelif marks >= 50:\n    print("C")\nelse:\n    print("F")',
        ["B", "C", "B\nC", "A"], 0,
        "Python stops at the first branch that is True.",
        "72 >= 90 is False, 72 >= 70 is True -> prints 'B' and skips the rest, even though 72 >= 50 is also True.",
        topic="if-structure", level=1,
        diagram="""
 marks >= 90? --no--> marks >= 70? --yes--> "B"  (done)
                                   (later checks are skipped)
"""),
    mcq("How does Python know which lines belong inside an `if` block?",
        ["By indentation (usually 4 spaces)", "By curly braces { }", "By the keyword `end`", "By a semicolon after the condition"], 0,
        "Python has no braces for blocks.",
        "The block is the indented lines after the colon. Wrong indentation gives an IndentationError.",
        topic="if-structure", level=1),
    tf("In Python, `elif` is short for 'else if'.", True,
       "JS and Java write two words for it.",
       "Python uses `elif` for 'else if'. You can have as many elif branches as you need, and else is optional.",
       topic="if-structure", level=1),
    out('x = 3\nif x > 1:\n    print("a")\nif x > 2:\n    print("b")',
        ["a\nb", "a", "b", "Nothing"], 0,
        "These are two separate ifs, not if/elif.",
        "Separate if statements are each checked, so both print. With elif only the first True one would run.",
        topic="if-structure", level=1,
        diagram="""
 if / if:    check 1 -> run;  check 2 -> run   (both)
 if / elif:  check 1 -> run -> skip the rest   (one)
"""),

    # ---------------------------------------------------------------- level 2
    out('x = 3\nprint(1 < x < 5, 1 < x < 2)',
        ["True False", "True True", "False False", "TypeError"], 0,
        "Python reads it like maths.",
        "1 < x < 5 means (1 < x) and (x < 5). In JS, 1 < x < 5 compares a boolean to 5 and is a classic bug; Python does it right.",
        topic="comparisons", level=2,
        diagram="""
 1 < x < 5   ==   (1 < x) and (x < 5)
             ==    True   and  True   -> True
"""),
    out('print("apple" < "banana", "Zebra" < "apple")',
        ["True True", "True False", "False True", "TypeError"], 0,
        "Strings compare character by character using character codes.",
        "'a' < 'b' so apple < banana. All uppercase letters come before lowercase ones, so 'Zebra' < 'apple' too.",
        topic="comparisons", level=2),
    out('print(3 == "3", 3 == 3.0)',
        ["False True", "True True", "False False", "TypeError"], 0,
        "Python doesn't convert strings to numbers for you.",
        "There's no type coercion: the int 3 isn't equal to the string '3' (unlike JS ==). 3 == 3.0 is True because they're the same number.",
        topic="comparisons", level=2,
        analogy="Python's == is closer to JS ===: no type conversion. 3 == 3.0 is still True because both are numbers of the same value."),
    out('print(bool("False"), bool("0"), bool([0]), bool(0.0))',
        ["True True True False", "False False False False", "False False True False", "True False True False"], 0,
        "Non-empty strings and non-empty lists are truthy, whatever is inside.",
        "'False' and '0' are non-empty strings (truthy); [0] is a list with one item (truthy); 0.0 is a zero number (falsy).",
        topic="truthiness", level=2),
    out('print(True + True, True * 10)',
        ["2 10", "True True", "TypeError", "True 10"], 0,
        "bool is a subclass of int.",
        "True behaves like 1 and False like 0 in arithmetic. Handy trick: sum(x > 0 for x in nums) counts the positives.",
        topic="truthiness", level=2,
        analogy='Like a light switch wired as 1 for on and 0 for off: you can add up how many lights are on.'),
    out('print(0 or "default", "set" or "default")',
        ["default set", "False set", "True True", "default default"], 0,
        "`or` hands back one of its operands.",
        "`or` returns the first truthy operand (or the last one). 0 is falsy so you get 'default'; 'set' is truthy so you get 'set'.",
        topic="logic-ops", level=2,
        diagram="""
 0 or "default":     0 falsy -> go on -> "default"
 "set" or "default": "set" truthy -> stop -> "set"
"""),
    out('print(5 and 7, 0 and 7)',
        ["7 0", "True False", "5 0", "7 7"], 0,
        "`and` stops at the first falsy value, otherwise gives the last.",
        "5 is truthy so `and` moves on and returns 7. 0 is falsy so `and` returns 0 straight away.",
        topic="logic-ops", level=2),
    out('a = [1, 2]\nb = [1, 2]\nprint(a == b, a is b)',
        ["True False", "True True", "False False", "False True"], 0,
        "Same contents, or same object?",
        "== compares values (equal contents). is compares identity; a and b are two separate list objects.",
        topic="identity", level=2,
        analogy="Like Java: a.equals(b) vs a == b on object references."),
    out('nums = [4, 7, 10]\nprint(["even" if n % 2 == 0 else "odd" for n in nums])',
        ["['even', 'odd', 'even']", "['odd', 'even', 'odd']", "[4, 10]", "SyntaxError"], 0,
        "The ternary decides what each item becomes.",
        "For each n the expression picks 'even' or 'odd'. (A trailing `if` after the for would filter instead.)",
        topic="ternary", level=2),
    out('n = 1\nprint(f"{n} item{"s" if n != 1 else ""}")',
        ["1 item", "1 items", "SyntaxError", "1 item{}"], 0,
        "When n is 1, which string is chosen?",
        "n != 1 is False, so the empty string is added: '1 item'. Python 3.12+ allows the same quote type inside an f-string.",
        topic="ternary", level=2),
    out('def describe(code):\n    match code:\n        case 200:\n            return "OK"\n        case 404:\n            return "Not Found"\n        case _:\n            return "Other"\n\nprint(describe(404), describe(500))',
        ["Not Found Other", "Not Found Not Found", "OK Other", "Other Other"], 0,
        "_ is the catch-all case.",
        "match compares the value against each case top to bottom. 404 matches the second; 500 matches nothing specific, so `case _` runs.",
        topic="match-case", level=2,
        analogy="Like a JS switch, but no fall-through and no break needed: only the first matching case runs."),
    out('def kind(day):\n    match day:\n        case "sat" | "sun":\n            return "weekend"\n        case _:\n            return "weekday"\n\nprint(kind("sun"), kind("mon"))',
        ["weekend weekday", "weekday weekday", "weekend weekend", "SyntaxError"], 0,
        "| inside a case means 'or'.",
        "case 'sat' | 'sun' matches either string. 'mon' falls to the wildcard.",
        topic="match-case", level=2),
    out('print(not 1 == 2)',
        ["True", "False", "TypeError", "1"], 0,
        "Which runs first: == or not?",
        "== binds tighter than not, so this is not (1 == 2) -> not False -> True.",
        topic="precedence", level=2),
    out('print(True or False and False)',
        ["True", "False", "None", "SyntaxError"], 0,
        "`and` is evaluated before `or`, like * before +.",
        "It's True or (False and False) -> True or False -> True.",
        topic="precedence", level=2,
        diagram="""
 True or (False and False)
          '----+-----'
             False
 True or False -> True
"""),
    out('losses = [0.9, 0.5, 0.2]\nprint(any(l < 0.3 for l in losses), all(l < 1 for l in losses))',
        ["True True", "False True", "True False", "False False"], 0,
        "any: at least one; all: every one.",
        "0.2 < 0.3, so any() is True. All losses are below 1, so all() is True.",
        topic="any-all", level=2),
    out('files = ["a.csv", "b.csv", "c.txt"]\nprint(all(f.endswith(".csv") for f in files))',
        ["False", "True", "['a.csv', 'b.csv']", "TypeError"], 0,
        "One file breaks the rule.",
        "c.txt doesn't end with .csv, so all() is False.",
        topic="any-all", level=2),
    out('score = 95\nif score >= 50:\n    grade = "pass"\nelif score >= 90:\n    grade = "distinction"\nprint(grade)',
        ["pass", "distinction", "pass\ndistinction", "NameError"], 0,
        "The order of the branches matters.",
        "95 >= 50 is checked first and is True, so the 'distinction' branch can never run. Put the strictest condition first.",
        topic="if-structure", level=2,
        diagram="""
 95 >= 50 ? yes -> "pass"  (stop)
 95 >= 90 ?  never reached
 fix: test >= 90 first, then >= 50
"""),

    # ---------------------------------------------------------------- level 3
    out('print(0.1 + 0.2 == 0.3)\nimport math\nprint(math.isclose(0.1 + 0.2, 0.3))',
        ["False\nTrue", "True\nTrue", "False\nFalse", "True\nFalse"], 0,
        "Floats are stored in binary and can't represent 0.1 exactly.",
        "0.1 + 0.2 is 0.30000000000000004, so == fails. Compare floats with math.isclose (or a tolerance), e.g. when checking a loss value.",
        topic="comparisons", level=3,
        analogy="Like 1/3 written as 0.333 in decimal: binary can't write 0.1 exactly either, so tiny errors creep in.",
        diagram="""
 0.1 + 0.2  ->  0.30000000000000004
 0.3        ->  0.29999999999999998...
 ==  -> False      isclose -> True (tiny gap)
"""),
    out('print(3 < "4")',
        ["TypeError", "True", "False", "ValueError"], 0,
        "Python 3 won't order a number against a string.",
        "Ordering comparisons between unrelated types raise TypeError. (== between them is allowed and just returns False.)",
        topic="comparisons", level=3),
    out('print([1, 2, 3] < [1, 3], (1, 2) < (1, 2, 0))',
        ["True True", "False True", "True False", "TypeError"], 0,
        "Sequences compare item by item, left to right, like words in a dictionary.",
        "[1, 2, 3] vs [1, 3]: first items tie, then 2 < 3, so True. (1, 2) is a prefix of (1, 2, 0), and the shorter one is smaller.",
        topic="comparisons", level=3,
        diagram="""
 [1, 2, 3]
 [1, 3]
  =  2<3  -> decided: True (rest ignored)
"""),
    out('batch_size = 0\nbs = batch_size or 32\nprint(bs)',
        ["32", "0", "True", "None"], 0,
        "Is 0 truthy?",
        "`or` treats 0 as falsy and falls back to 32, even though 0 was a real value. If only None should fall back, write `32 if batch_size is None else batch_size`.",
        topic="truthiness", level=3,
        analogy="A form that treats 'number of children: 0' as 'field left blank' and fills in a default.",
        diagram="""
 batch_size = 0  -> falsy -> or picks 32   (wrong!)
 batch_size = None -> falsy -> or picks 32 (intended)
"""),
    out('import numpy as np\nmask = np.array([True, False])\nif mask:\n    print("yes")',
        ["ValueError", "yes", "Nothing is printed", "TypeError"], 0,
        "Is a two-element array True or False as a whole?",
        "NumPy refuses to guess: 'The truth value of an array with more than one element is ambiguous'. Use mask.any() or mask.all().",
        topic="truthiness", level=3,
        analogy="Asking 'is this class tall?': every student, any student, or the average? NumPy makes you say which.",
        diagram="""
 mask = [True, False]
 any()?  True     all()?  False
 if mask: ?  -> ambiguous -> ValueError
"""),
    out('def check():\n    print("called")\n    return True\n\nresult = False and check()\nprint(result)',
        ["False", "called\nFalse", "called\nTrue", "None"], 0,
        "If the left side of `and` is False, is the right side needed?",
        "and short-circuits: False and anything is False, so check() is never called.",
        topic="logic-ops", level=3,
        analogy='A security gate that stops at the first failed check and never runs the rest.'),
    out('user = None\nname = user and user["name"]\nprint(name)',
        ["None", "TypeError", "False", "KeyError"], 0,
        "`and` returns the first falsy operand.",
        "user is None (falsy), so `and` returns None without evaluating user['name']. That's why `x and x.attr` works as a guard.",
        topic="logic-ops", level=3,
        analogy='The same idea as JS user && user.name (or user?.name).'),
    out('print([] or {} or 0, 1 and "a" and [2])',
        ["0 [2]", "False True", "[] [2]", "0 a"], 0,
        "`or` with no truthy operand returns the last one.",
        "All of [], {}, 0 are falsy, so `or` returns the last: 0. All of 1, 'a', [2] are truthy, so `and` returns the last: [2].",
        topic="logic-ops", level=3),
    mcq("Why should you NOT write `if x is 1000:` or `if s is 'abc':`?",
        ["`is` checks object identity, which depends on caching and interning details; use == for values",
         "`is` is slower than ==",
         "`is` only works on lists",
         "It's fine; `is` and == are the same for numbers and strings"], 0,
        "Two equal values may or may not be the same object.",
        "Whether two equal ints/strings are the same object is an implementation detail. Python even emits a SyntaxWarning for `is` with a literal.",
        topic="identity", level=3),
    tf("`x is None` and `x == None` always give the same result.", False,
       "Who decides what == means for an object?",
       "== calls the object's __eq__, which a class can define to return anything. `is` can't be overridden, which is why PEP 8 says use `is None`.",
       topic="identity", level=3),
    out('x = 5\nprint("big" if x > 3 else "small" + "!")',
        ["big", "big!", "small!", "SyntaxError"], 0,
        "The conditional expression has the lowest precedence; where does the + attach?",
        "It parses as 'big' if x > 3 else ('small' + '!'). x > 3, so just 'big'. Wrap in brackets if you want ! on both.",
        topic="ternary", level=3,
        diagram="""
 "big" if x > 3 else ("small" + "!")
                     '------ else part only'
"""),
    out('print(1 + 1 if False else 0)',
        ["0", "1", "2", "SyntaxError"], 0,
        "Does the if/else apply to 1 + 1 or just to the second 1?",
        "Arithmetic binds tighter, so it's (1 + 1) if False else 0 -> 0.",
        topic="ternary", level=3),
    out('def where(p):\n    match p:\n        case (0, 0):\n            return "origin"\n        case (0, y):\n            return f"on y-axis at {y}"\n        case (x, y):\n            return f"at {x},{y}"\n\nprint(where((0, 7)))',
        ["on y-axis at 7", "origin", "at 0,7", "SyntaxError"], 0,
        "Literals must match; names capture whatever is there.",
        "(0, 0) fails since 7 != 0. (0, y) matches: 0 is a literal and y captures 7.",
        topic="match-case", level=3,
        diagram="""
 subject:  ( 0 , 7 )
 case:     ( 0 , y )
             |   |
          must  binds
          equal y = 7
"""),
    out('def route(event):\n    match event:\n        case {"type": "click", "x": x}:\n            return f"click at {x}"\n        case {"type": "key"}:\n            return "key"\n        case _:\n            return "unknown"\n\nprint(route({"type": "click", "x": 5, "y": 9}))',
        ["click at 5", "unknown", "key", "KeyError"], 0,
        "Does a mapping pattern need ALL keys to be listed?",
        "Mapping patterns only require the listed keys; extra keys like 'y' are ignored. Great for routing JSON events or tool calls.",
        topic="match-case", level=3,
        diagram="""
 subject: {"type": "click", "x": 5, "y": 9}
 pattern: {"type": "click", "x": x}
           match      bind x=5   "y" ignored
"""),
    out('def sign(n):\n    match n:\n        case 0:\n            return "zero"\n        case x if x > 0:\n            return "positive"\n        case _:\n            return "negative"\n\nprint(sign(-3), sign(8))',
        ["negative positive", "positive positive", "zero positive", "negative negative"], 0,
        "A guard is an extra `if` the case must pass.",
        "-3 isn't 0, then `x if x > 0` captures -3 but the guard fails, so it falls to _. 8 passes the guard.",
        topic="match-case", level=3),
    out('def cmd(parts):\n    match parts:\n        case ["go", direction]:\n            return f"going {direction}"\n        case ["quit"]:\n            return "bye"\n        case [first, *rest]:\n            return f"unknown {first} +{len(rest)}"\n\nprint(cmd(["go", "north"]), "|", cmd(["jump", "a", "b"]))',
        ["going north | unknown jump +2", "going north | unknown jump +3", "going north | bye", "SyntaxError"], 0,
        "Sequence patterns match by length and position; *rest takes the leftovers.",
        "['go', 'north'] matches the first case. ['jump', 'a', 'b'] has 3 items so it skips to [first, *rest] with rest = ['a', 'b'].",
        topic="match-case", level=3),
    out('x = 5\nif x == 1 or 2:\n    print("matched")\nelse:\n    print("no")',
        ["matched", "no", "SyntaxError", "TypeError"], 0,
        "How does Python group `x == 1 or 2`?",
        "It's (x == 1) or 2. x == 1 is False, so the result is 2, which is truthy. Write `x == 1 or x == 2`, or better `x in (1, 2)`.",
        topic="precedence", level=3,
        analogy="Asking 'is it red or blue?' and the computer hears 'is it red?' OR 'blue', and 'blue' on its own counts as yes.",
        diagram="""
 x == 1 or 2
   = (x == 1) or 2
   =  False   or 2  -> 2 (truthy) -> branch runs
"""),
    out('print(not True and False, not (True and False))',
        ["False True", "True True", "False False", "True False"], 0,
        "not binds tighter than and.",
        "(not True) and False -> False and False -> False. With brackets, not (False) -> True.",
        topic="precedence", level=3),
    out('print(all([]), any([]))',
        ["True False", "False False", "True True", "False True"], 0,
        "all asks 'is there any item that fails?'; any asks 'is there any item that passes?'",
        "With no items, nothing fails (all is True) and nothing passes (any is False). An empty batch silently passes an all() validation check.",
        topic="any-all", level=3,
        analogy="'Every student in an empty class passed' is technically true: nobody failed.",
        diagram="""
 all(items): stop at first falsy  -> none found -> True
 any(items): stop at first truthy -> none found -> False
"""),
    out('print(all([[], [1]]), any([0, "", None, [0]]))',
        ["False True", "True True", "False False", "True False"], 0,
        "Each item's own truthiness is what counts.",
        "[] is falsy, so all() is False. [0] is a non-empty list (truthy), so any() is True.",
        topic="any-all", level=3),
    out('def price(cart):\n    if not cart:\n        return 0\n    if len(cart) > 100:\n        return -1\n    return sum(cart)\n\nprint(price([]), price([10, 20]))',
        ["0 30", "None 30", "0 0", "-1 30"], 0,
        "The edge cases return early.",
        "This is the guard-clause style: handle empty and too-big carts first, then the main logic sits un-nested at the end.",
        topic="if-structure", level=3,
        diagram="""
 price(cart)
  |-- empty?    -> return 0
  |-- too big?  -> return -1
  '-- main path:   return sum(cart)
""",
        analogy="Like validating a request at the top of an API handler and returning 400 early, before the real work."),

    # ---------------------------------------------------------------- level 4
    out('print(False == False in [False])\nprint((False == False) in [False])',
        ["True\nFalse", "False\nFalse", "True\nTrue", "False\nTrue"], 0,
        "`in` is a comparison operator too, so it chains with ==.",
        "Chained: (False == False) and (False in [False]) -> True and True -> True. With brackets: True in [False] -> False.",
        topic="comparisons", level=4,
        diagram="""
 False == False in [False]
   = (False == False) and (False in [False])
   =      True        and      True       -> True
"""),
    out('def mid():\n    print("mid")\n    return 3\n\nprint(1 < mid() < 5)',
        ["mid\nTrue", "mid\nmid\nTrue", "True", "mid\nFalse"], 0,
        "How many times is the middle operand evaluated in a chain?",
        "a < b < c evaluates b only once, unlike the hand-written (1 < mid()) and (mid() < 5), which would call it twice.",
        topic="comparisons", level=4,
        diagram="""
 1 < mid() < 5
 tmp = mid()          (called once)
 (1 < tmp) and (tmp < 5)
"""),
    out('class Batch:\n    def __init__(self, items):\n        self.items = items\n    def __len__(self):\n        return len(self.items)\n\nprint(bool(Batch([])), bool(Batch([1])), bool(object()))',
        ["False True True", "True True True", "False True False", "TypeError"], 0,
        "With no __bool__, Python falls back to something else.",
        "Truth testing calls __bool__ if defined, else __len__ (0 means falsy). Objects with neither are always truthy.",
        topic="truthiness", level=4,
        diagram="""
 bool(obj):  has __bool__? -> use it
             else __len__? -> len != 0
             else          -> True
"""),
    out('class AlwaysEqual:\n    def __eq__(self, other):\n        return True\n\nobj = AlwaysEqual()\nprint(obj == None, obj is None)',
        ["True False", "False False", "True True", "TypeError"], 0,
        "One of these operators can be overridden by the class.",
        "obj == None calls obj.__eq__ and gets True. `is` checks identity and can't be faked, which is why `is None` is the safe check.",
        topic="identity", level=4,
        analogy="Someone who says 'yes' to every 'are you X?' question; `is` checks their ID card instead of asking."),
    out('x = float("nan")\nprint(x == x, x in [x], float("nan") in [x])',
        ["False True False", "False False False", "True True True", "False True True"], 0,
        "Containers check identity before equality.",
        "NaN is never equal to anything, even itself. But `in` (and list.count, dict lookup) tries `is` first, so the same object is found; a different NaN isn't.",
        topic="identity", level=4),
    out('def a():\n    print("a")\n    return 0\n\ndef b():\n    print("b")\n    return 1\n\nprint(a() if b() else b())',
        ["b\na\n0", "a\n0", "b\nb\n1", "a\nb\n0"], 0,
        "The condition is evaluated first, then only ONE branch.",
        "b() runs first as the condition (prints b, returns 1, truthy), then only a() runs. The else branch is never evaluated.",
        topic="ternary", level=4),
    out('n = 0\nprint("neg" if n < 0 else "zero" if n == 0 else "pos")',
        ["zero", "neg", "pos", "SyntaxError"], 0,
        "Nested conditional expressions group to the right.",
        "It's 'neg' if n < 0 else ('zero' if n == 0 else 'pos'). Readable for two levels; beyond that use if/elif.",
        topic="ternary", level=4),
    out('code = """\nmatch color:\n    case RED:\n        print("red")\n    case _:\n        print("other")\n"""\ncompile(code, "<demo>", "exec")',
        ["SyntaxError", "Nothing is printed", "NameError", "red"], 0,
        "A bare name in a case is not a constant lookup.",
        "`case RED:` is a capture pattern that matches anything and binds it to RED, so the next case is unreachable: SyntaxError 'name capture makes remaining patterns unreachable'. Use a dotted name like Color.RED.",
        topic="match-case", level=4,
        analogy='Like a route /:color in a web router: a bare name is a placeholder that captures anything, not a fixed value.'),
    out('def f(x):\n    match x:\n        case [a, b]:\n            return f"pair {a}{b}"\n        case str():\n            return "string"\n\nprint(f("hi"), f(("h", "i")))',
        ["string pair hi", "pair hi pair hi", "string string", "pair hi string"], 0,
        "Is a two-character string a sequence pattern match?",
        "Sequence patterns deliberately do NOT match str/bytes, so 'hi' goes to the class pattern str(). The tuple ('h', 'i') is a sequence of length 2.",
        topic="match-case", level=4),
    out('from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\ndef where(p):\n    match p:\n        case Point(x=0, y=0):\n            return "origin"\n        case Point(x=0):\n            return "y-axis"\n        case Point(x=x, y=y) if x == y:\n            return "diagonal"\n        case _:\n            return "elsewhere"\n\nprint(where(Point(0, 4)), where(Point(3, 3)))',
        ["y-axis diagonal", "origin diagonal", "y-axis elsewhere", "TypeError"], 0,
        "Class patterns check type, then the named attributes you list.",
        "Point(0, 4) fails origin but matches Point(x=0). Point(3, 3) binds x and y, and the guard x == y passes.",
        topic="match-case", level=4),
    out('import pandas as pd\ndf = pd.DataFrame({"a": [1, 5, 9], "b": [2, 1, 0]})\ntry:\n    df[(df.a > 1) and (df.b < 2)]\nexcept ValueError:\n    print("ValueError")\nprint(len(df[(df.a > 1) & (df.b < 2)]))',
        ["ValueError\n2", "2", "ValueError\n1", "TypeError\n2"], 0,
        "`and` needs ONE truth value; a Series has many.",
        "`and` calls bool() on the Series, which is ambiguous -> ValueError. Element-wise masks need & (and brackets, because & binds tighter than >).",
        topic="precedence", level=4),
    out('print(not 1 in [2], not None is None)',
        ["True False", "False True", "True True", "SyntaxError"], 0,
        "`in` and `is` are comparisons, so they bind tighter than not.",
        "not (1 in [2]) -> not False -> True. not (None is None) -> not True -> False. PEP 8 prefers `not in` / `is not` for clarity.",
        topic="precedence", level=4),
    out('def gen():\n    for x in [1, 2, 3, 4]:\n        print("check", x)\n        yield x > 1\n\nprint(any(gen()))',
        ["check 1\ncheck 2\nTrue", "check 1\ncheck 2\ncheck 3\ncheck 4\nTrue", "True", "check 1\nTrue"], 0,
        "any() can stop as soon as it knows the answer.",
        "any() short-circuits on the first truthy item, so the generator is only advanced twice. Passing a list comprehension instead would compute all 4 first.",
        topic="any-all", level=4,
        analogy='Interviewing candidates one at a time and stopping at the first good one, instead of interviewing everyone first.',
        diagram="""
 item:    1      2      3   4
 value:  False  True
 any:    keep   STOP -> True  (3, 4 never made)
"""),
    out('print(any(["", 0, "x"]), any([0, 5]) == 5)',
        ["True False", "x True", "True True", "x False"], 0,
        "Unlike `or`, any() doesn't hand back an operand.",
        "any() and all() always return a bool (True/False), not the first truthy item. To get the item, use next((v for v in items if v), None).",
        topic="any-all", level=4),
    out('data = [3, 8, 1, 9]\nif (n := len(data)) > 3:\n    print(f"too long: {n}")',
        ["too long: 4", "too long: True", "SyntaxError", "Nothing is printed"], 0,
        "The walrus := assigns and returns the value in one step.",
        "(n := len(data)) stores 4 in n and evaluates to 4, so 4 > 3 is True and n is usable in the body. The brackets matter: without them n would get the bool.",
        topic="if-structure", level=4),
    out('if True:\n    pass\nelse:\n    print("never")\nprint("done")',
        ["done", "never\ndone", "IndentationError", "Nothing"], 0,
        "pass is a statement that does nothing.",
        "A block can't be empty, so `pass` is the placeholder. The if-branch runs (doing nothing), else is skipped, then 'done'.",
        topic="if-structure", level=4),
    mcq("A reviewer flags `if flag == True:` and `if len(items) > 0:` in your PR. What's the idiomatic replacement and why?",
        ["`if flag:` and `if items:`; truthiness already covers it and works for any container",
         "`if flag is True:` and `if items != []:`; it's more explicit",
         "`if bool(flag) == True:` and `if len(items):`; it avoids errors",
         "Nothing; the originals are the PEP 8 style"], 0,
        "PEP 8 has an opinion on comparing to True.",
        "PEP 8: don't compare booleans to True with ==, and use the fact that empty sequences are falsy. Exception: when None and 0/'' mean different things, check `is None` explicitly.",
        topic="truthiness", level=4),

    # ================================================================ second set
    # ---------------------------------------------------------------- level 1
    out('password = "abc123"\nprint(len(password) >= 8)',
        ["False", "True", "6", "abc123"], 0,
        "How many characters are there?",
        "len('abc123') is 6, and 6 >= 8 is False. A comparison can use any expression on either side, such as a function call.",
        topic="comparisons", level=1),
    mcq("Python reports a SyntaxError on the line `if x > 5`. What's missing?",
        ["A colon at the end: if x > 5:", "Brackets: if (x > 5)", "Curly braces around the block", "The word then"], 0,
        "Every line that opens a block ends with the same character.",
        "if, elif, else, for, while, def and class lines all end with a colon. Brackets around the condition are optional in Python.",
        topic="if-structure", level=1,
        analogy="The colon plays the role of the opening { in JS or Java; the indentation replaces the closing }."),
    tf("`if items:` runs its block only when the list `items` has at least one item.", True,
       "What is the truth value of an empty list?",
       "An empty list is falsy and a non-empty one is truthy, so `if items:` means 'if the list is not empty'. No len() needed.",
       topic="truthiness", level=1),
    out('val_loss = 0.42\nbest = 0.40\nif val_loss < best:\n    print("save model")\nelse:\n    print("no improvement")',
        ["no improvement", "save model", "save model\nno improvement", "Nothing is printed"], 0,
        "Lower loss is better. Is 0.42 lower than 0.40?",
        "0.42 < 0.40 is False, so the else branch runs. Training loops use exactly this check to decide whether to save a new best checkpoint.",
        topic="ml-patterns", level=1),
    out('print(isinstance(5, int), isinstance("5", int))',
        ["True False", "True True", "False False", "int str"], 0,
        "Quotes make a string, whatever is inside them.",
        "isinstance(value, type) asks 'is this value of that type?'. 5 is an int; '5' is a str that happens to contain a digit.",
        topic="type-checks", level=1),
    fill("The comparison operator that means 'not equal to' is ____.", "!=",
         "An exclamation mark is involved.",
         "!= gives True when the two sides differ: 3 != 4 is True. Python has no !== or <> (that one was removed in Python 3).",
         topic="comparisons", level=1),

    # ---------------------------------------------------------------- level 2
    out('print(isinstance(3.0, (int, float)), type(3.0) == int)',
        ["True False", "False False", "True True", "TypeError"], 0,
        "isinstance accepts a tuple of types.",
        "isinstance(x, (int, float)) is True if x is either type: a handy 'is it a number?' check. 3.0 is a float, so type(3.0) == int is False.",
        topic="type-checks", level=2),
    out('value = "42"\nif value.isdigit():\n    value = int(value)\nprint(value + 1)',
        ["43", "421", "TypeError", "42"], 0,
        "The string is converted before the maths.",
        "isdigit() is True for '42', so value becomes the int 42 and 42 + 1 is 43. Without the conversion, '42' + 1 would raise TypeError.",
        topic="type-checks", level=2),
    out('print(not [], not [0])',
        ["True False", "False True", "True True", "False False"], 0,
        "An empty list is falsy; a list holding a zero is not empty.",
        "not [] is True. [0] has one item, so it's truthy and not [0] is False.",
        topic="logic-ops", level=2),
    out('print("10" < "9", 10 < 9)',
        ["True False", "False False", "True True", "TypeError"], 0,
        "Strings compare character by character, not by numeric value.",
        "'1' comes before '9', so '10' < '9' is True. That's why files named epoch_10, epoch_9 sort in the wrong order; compare numbers as ints, or zero-pad the names.",
        topic="comparisons", level=2,
        analogy="Like a phone book: 'Ab...' comes before 'B' no matter how long the name is."),
    mcq("Which checks that `x` is between 0 and 1 inclusive, in idiomatic Python?",
        ["0 <= x <= 1", "0 <= x and <= 1", "x in range(0, 1)", "x >= 0 or x <= 1"], 0,
        "Python lets you chain comparisons like maths.",
        "0 <= x <= 1 means 0 <= x and x <= 1. range(0, 1) only contains the int 0, and `or` would accept every number.",
        topic="comparisons", level=2),
    out('x = -4\nprint(x if x >= 0 else -x)',
        ["4", "-4", "True", "SyntaxError"], 0,
        "Which branch runs for a negative x?",
        "x >= 0 is False, so the expression gives -x, which is 4. That's absolute value written as a conditional expression (abs(x) does the same).",
        topic="ternary", level=2),
    out('def run(cmd):\n    match cmd:\n        case "start":\n            return "go"\n        case "stop":\n            return "halt"\n\nprint(run("stop"), run("pause"))',
        ["halt None", "halt halt", "halt MatchError", "go None"], 0,
        "What happens when no case matches?",
        "If no case matches, match does nothing (no error), so the function falls off the end and returns None. Add `case _:` when you need a default.",
        topic="match-case", level=2),
    tf("In match/case, if two cases both match, both of their blocks run, top to bottom.", False,
       "Think switch without fall-through.",
       "Only the first matching case runs; there is no fall-through and no break. Put the most specific cases first.",
       topic="match-case", level=2),
    out('scores = [55, 72, 40]\nprint(any(s < 50 for s in scores), sum(s >= 50 for s in scores))',
        ["True 2", "False 2", "True 1", "True [55, 72]"], 0,
        "Booleans add up as 1s and 0s.",
        "40 < 50, so any() is True. Summing the boolean generator counts the True values: 55 and 72 pass, giving 2.",
        topic="any-all", level=2),
    out('rows = [{"id": 1}, {"id": 2, "label": "x"}]\nprint(all("label" in r for r in rows))',
        ["False", "True", "KeyError", "[False, True]"], 0,
        "Does every row have the key?",
        "The first row has no 'label', so all() is False. A one-line check before training that every example is labelled.",
        topic="any-all", level=2),
    out('age, has_id = 20, False\nif age >= 18:\n    if has_id:\n        print("enter")\n    else:\n        print("show id")\nelse:\n    print("too young")',
        ["show id", "enter", "too young", "show id\ntoo young"], 0,
        "Follow the outer if first, then the inner one.",
        "age >= 18 is True, so we go inside; has_id is False, so the inner else runs. Each else belongs to the if at the same indentation.",
        topic="if-structure", level=2),
    tf("`x is not None` and `not x is None` give the same result, but `is not` is the preferred style.", True,
       "`is` binds tighter than `not`.",
       "not x is None parses as not (x is None), so both agree. PEP 8 recommends `is not` because it reads as one operator and can't be misread.",
       topic="identity", level=2),
    out('labels = [1, 0, 1]\npreds = [1, 1, 1]\nacc = sum(p == y for p, y in zip(preds, labels)) / len(labels)\nprint(round(acc, 2))',
        ["0.67", "0.33", "2", "1.0"], 0,
        "Each comparison is True (1) or False (0).",
        "Two of the three predictions match, so the sum is 2 and accuracy is 2/3, about 0.67. Comparisons that sum to counts are behind most metric code.",
        topic="ml-patterns", level=2),

    # ---------------------------------------------------------------- level 3
    out('accs = [0.70, 0.75, 0.74, 0.73]\npatience, bad = 2, 0\nbest = accs[0]\nfor a in accs[1:]:\n    if a > best:\n        best, bad = a, 0\n    else:\n        bad += 1\n    if bad >= patience:\n        print("stop at", a)\n        break',
        ["stop at 0.73", "stop at 0.74", "Nothing is printed", "stop at 0.75"], 0,
        "Count epochs without improvement; reset on improvement.",
        "0.75 improves (bad = 0); 0.74 and 0.73 don't (bad = 1, then 2), so the loop stops at 0.73. This is early stopping with patience = 2.",
        topic="ml-patterns", level=3,
        diagram="""
 acc:   0.70  0.75  0.74  0.73
 best:  0.70  0.75  0.75  0.75
 bad:    -     0     1     2   -> 2 >= patience: stop
"""),
    out('x = 5\nprint(x > 3 == True)',
        ["False", "True", "TypeError", "SyntaxError"], 0,
        "== is a comparison too, so this is a chain.",
        "It means (x > 3) and (3 == True). 3 == True is False, so the result is False. Another reason never to write `== True`.",
        topic="comparisons", level=3,
        diagram="""
 x > 3 == True
   =  (x > 3) and (3 == True)
   =   True   and  False
   =  False
"""),
    out('print(round(2.675, 2) == 2.68, round(2.675, 2))',
        ["False 2.67", "True 2.68", "False 2.68", "True 2.67"], 0,
        "2.675 can't be stored exactly in binary.",
        "The float is really 2.67499999..., so it rounds down to 2.67. Rounding doesn't fix float comparisons; use math.isclose with a tolerance.",
        topic="comparisons", level=3),
    out('print(None == 0)\nprint(None < 1)',
        ["False\nTypeError", "True\nFalse", "False\nTrue", "False\nFalse"], 0,
        "== works between any types; < doesn't.",
        "None equals nothing but itself, so == is False. Ordering None against an int raises TypeError, e.g. when a metric is missing and you sort or compare it.",
        topic="comparisons", level=3),
    out('print([1, 2] == (1, 2), [1, 2] == list((1, 2)))',
        ["False True", "True True", "False False", "TypeError"], 0,
        "== between a list and a tuple...",
        "A list never equals a tuple, even with the same items. Convert one side first. A common surprise after JSON round trips turn tuples into lists.",
        topic="comparisons", level=3),
    out('import numpy as np\na = np.array([0.5])\nif a:\n    print("ok")',
        ["ok", "ValueError", "Nothing is printed", "TypeError"], 0,
        "The ambiguity error is about arrays with MORE than one element.",
        "A one-element array has a single clear truth value, so this works. That's what makes the bug sneaky: the same code crashes later when the array has 2 elements.",
        topic="truthiness", level=3),
    out('import pandas as pd\ndf = pd.DataFrame({"a": []})\nprint(df.empty, len(df) == 0)',
        ["True True", "False True", "ValueError", "True False"], 0,
        "A DataFrame can't be used in `if df:`, so Pandas gives you an attribute.",
        "`if df:` raises ValueError (ambiguous). Use df.empty or len(df) == 0 to check for an empty table, e.g. after a filter removes every row.",
        topic="ml-patterns", level=3),
    out('print(bool(" "), bool(" ".strip()))',
        ["True False", "False False", "True True", "False True"], 0,
        "A space is still a character.",
        "' ' is a non-empty string, so it's truthy and `if name:` lets it through. Strip user input first, then test it.",
        topic="truthiness", level=3),
    out('x = []\nprint(x and x[0])',
        ["[]", "None", "IndexError", "False"], 0,
        "`and` returns its first falsy operand as it is.",
        "x is falsy, so `and` returns x itself ([]) and never evaluates x[0]. The guard avoids the IndexError but hands back [] rather than None.",
        topic="logic-ops", level=3),
    out('x = 0\nprint(x == 0 or 1 / x > 1)',
        ["True", "ZeroDivisionError", "False", "1"], 0,
        "Does `or` need its right side when the left side is True?",
        "x == 0 is True, so `or` stops and 1 / x never runs. Put the cheap or protective check on the left.",
        topic="logic-ops", level=3),
    mcq("Python has no `??` operator. Which expression uses `timeout` unless it is None, keeping a real value of 0?",
        ["30 if timeout is None else timeout", "timeout or 30", "timeout and 30", "timeout if timeout else 30"], 0,
        "Only None should trigger the fallback.",
        "`or` and `if timeout` both treat 0 as missing. The explicit `is None` test is Python's version of JS/C# `timeout ?? 30`.",
        topic="logic-ops", level=3),
    tf("`True is 1` is False, even though `True == 1` is True.", True,
       "Equal values can still be different objects.",
       "True and 1 are equal (bool is a subclass of int), but they are distinct objects, so `is` says False. Python also warns about `is` with a literal.",
       topic="identity", level=3),
    out('x = 0\nresult = 10 / x if x else 0\nprint(result)',
        ["0", "ZeroDivisionError", "10", "None"], 0,
        "Only one branch of a conditional expression is evaluated.",
        "x is 0 (falsy), so the else branch gives 0 and 10 / x never runs. A safe-division one-liner.",
        topic="ternary", level=3),
    out('print([n for n in range(5) if n % 2 else 0])',
        ["SyntaxError", "[0, 1, 0, 3, 0]", "[1, 3]", "[0, 0, 0]"], 0,
        "In a comprehension, the filter `if` can't have an else.",
        "A trailing `if` filters and takes no else. To map values write the conditional expression first: [n if n % 2 else 0 for n in range(5)] -> [0, 1, 0, 3, 0].",
        topic="ternary", level=3),
    out('def kind(v):\n    match v:\n        case bool():\n            return "bool"\n        case int() | float():\n            return "number"\n        case str():\n            return "text"\n        case _:\n            return "other"\n\nprint(kind(True), kind(3.5), kind(None))',
        ["bool number other", "number number other", "bool number text", "bool float other"], 0,
        "Class patterns use isinstance, and order matters.",
        "bool() is checked first, so True is 'bool' (otherwise it would match int()). 3.5 matches float(); None matches nothing until _.",
        topic="match-case", level=3),
    out('match [1, 2]:\n    case [1, *_] as whole:\n        print(whole)',
        ["[1, 2]", "1", "[2]", "SyntaxError"], 0,
        "`as` binds the whole matched value.",
        "[1, *_] matches any sequence starting with 1, and `as whole` captures the entire subject, so you can check the shape and still use the full value.",
        topic="match-case", level=3),
    out('match {"type": "msg", "text": "hi", "id": 7}:\n    case {"type": "msg", **rest}:\n        print(rest)',
        ["{'text': 'hi', 'id': 7}", "{'type': 'msg', 'text': 'hi', 'id': 7}", "{}", "SyntaxError"], 0,
        "**rest in a mapping pattern collects the keys you didn't list.",
        "'type' is matched and the remaining pairs go into rest. Useful for routing a message by type and passing the payload on.",
        topic="match-case", level=3),
    out('print(-2 ** 2, (-2) ** 2)',
        ["-4 4", "4 4", "-4 -4", "4 -4"], 0,
        "Which binds tighter: the minus sign or **?",
        "** binds tighter than unary minus, so -2 ** 2 is -(2 ** 2) = -4. Brackets make the minus part of the base.",
        topic="precedence", level=3),
    out('import numpy as np\na = np.array([0.1, 0.9])\nprint((a > 0.5).any(), (a > 0.5).all(), np.all([]))',
        ["True False True", "True True False", "False False True", "ValueError"], 0,
        "Array methods replace any() and all() on masks; an empty all is still True.",
        "a > 0.5 gives [False, True]: some (any) but not all. np.all([]) is True, the same vacuous truth as Python's all([]).",
        topic="any-all", level=3),
    out('print(all("abc"), all(["a", ""]), any(""))',
        ["True False False", "False False False", "True True True", "True False True"], 0,
        "A string is iterated character by character.",
        "Every character in 'abc' is a non-empty (truthy) string. [\"a\", \"\"] contains an empty string. The empty string has no characters, so any() is False.",
        topic="any-all", level=3),
    out('def grade(s):\n    if s >= 50:\n        return "pass"\n\nprint(grade(30))',
        ["None", "fail", "pass", "SyntaxError"], 0,
        "What does a function return if no return statement runs?",
        "For 30 the if is False and the function ends without a return, so it returns None. Make sure every branch returns something, or add a final return.",
        topic="if-structure", level=3),
    mcq("You have a 12-branch `if/elif` chain that maps status codes to messages. What's usually cleaner?",
        ["A dict lookup: MESSAGES.get(code, 'Unknown')", "Nesting the ifs deeper", "A while loop over the codes", "Twelve separate try/except blocks"], 0,
        "It's pure data: one key, one value.",
        "When each branch only returns a value, a dict is a lookup table: one line, O(1), and easy to extend. Keep if/elif (or match) for real logic.",
        topic="if-structure", level=3,
        analogy="Like a routing table in a web framework instead of a giant switch statement."),
    out('print(isinstance(True, int), type(True) == int)',
        ["True False", "False False", "True True", "False True"], 0,
        "bool is a subclass of int.",
        "isinstance accepts subclasses, so True counts as an int. type(True) is exactly bool, so the == check says no. A validator using isinstance(x, int) lets True through.",
        topic="type-checks", level=3),
    mcq("Why is `isinstance(cfg, dict)` usually preferred over `type(cfg) == dict`?",
        ["isinstance also accepts subclasses such as OrderedDict and defaultdict",
         "type() is deprecated",
         "isinstance is the only one that works on None",
         "type() == dict raises an error for subclasses"], 0,
        "What does type(x) == dict say about a defaultdict?",
        "type(x) == dict is an exact match, so a defaultdict fails it even though it is a dict. Use type() only when you really need the exact class.",
        topic="type-checks", level=3),
    fill("In Python 3.10+, `isinstance(x, list ____ tuple)` checks for either type in one expression.", "|",
         "The same symbol as a type-hint union.",
         "list | tuple builds a union type that isinstance understands, equal to passing (list, tuple).",
         topic="type-checks", level=3),
    out('import numpy as np\nprobs = np.array([0.2, 0.7, 0.5])\nprint(np.where(probs >= 0.5, 1, 0).tolist())',
        ["[0, 1, 1]", "[0, 1, 0]", "[1]", "ValueError"], 0,
        "np.where(condition, if_true, if_false) works item by item.",
        "Each probability is compared with 0.5 separately: 0.5 >= 0.5 is True. This is how you turn classifier probabilities into labels without a Python loop.",
        topic="ml-patterns", level=3,
        diagram="""
 probs:     0.2    0.7    0.5
 >= 0.5:    F      T      T
 where:     0      1      1
"""),
    out('import torch\nt = torch.tensor([1.0, 2.0])\nif t > 1:\n    print("big")',
        ["RuntimeError", "big", "ValueError", "Nothing is printed"], 0,
        "Same problem as NumPy, but PyTorch raises its own error type.",
        "t > 1 is a 2-element bool tensor, and 'Boolean value of Tensor with more than one value is ambiguous' is a RuntimeError. Use (t > 1).any() or .all().",
        topic="ml-patterns", level=3),
    mcq("Why do early-stopping checks often use `if val_loss < best - min_delta:` instead of `if val_loss < best:`?",
        ["So tiny, noise-level improvements don't count and training stops when progress is really flat",
         "Because floats can't be compared with <",
         "To make training run longer",
         "Because best is always negative"], 0,
        "A loss going from 0.40000 to 0.39999 isn't real progress.",
        "Without a minimum improvement, random noise keeps resetting patience and training never stops. min_delta sets how much better counts as better.",
        topic="ml-patterns", level=3),
    mcq('A config sets `"lr": 0.0` on purpose. Which check correctly reports a MISSING lr without flagging the 0.0?',
        ['if "lr" not in cfg:', 'if not cfg.get("lr"):', 'if cfg["lr"] is None:', 'if cfg.get("lr") == False:'], 0,
        "Ask about the key, not the value's truthiness.",
        "not cfg.get('lr') and == False are both triggered by 0.0. cfg['lr'] raises KeyError when it's truly missing. `in` checks only whether the key exists.",
        topic="ml-patterns", level=3),
    out('import torch\nt = torch.tensor(0.0)\nprint("truthy" if t else "falsy", bool(torch.tensor([2.0])))',
        ["falsy True", "truthy True", "RuntimeError", "falsy RuntimeError"], 0,
        "One-element tensors have a single truth value.",
        "A tensor with exactly one value can be used in `if` (it works like that number). That's why `if loss < best:` works on a scalar loss but fails on a batch of losses.",
        topic="ml-patterns", level=3),

    # ---------------------------------------------------------------- level 4
    out('def add(item, bucket=None):\n    bucket = bucket or []\n    bucket.append(item)\n    return bucket\n\nmine = []\nadd(1, mine)\nprint(mine)',
        ["[]", "[1]", "None", "TypeError"], 0,
        "Is the empty list the caller passed truthy?",
        "mine is [] (falsy), so `bucket or []` swaps in a NEW list and the caller's list never gets the item. Write `if bucket is None: bucket = []` instead.",
        topic="logic-ops", level=4,
        diagram="""
 caller:   mine ---> []          (falsy!)
 inside:   bucket = mine or []
           bucket ---> [] (new) -> append(1) -> [1]
 result:   mine is still []
"""),
    out('_MISSING = object()\n\ndef get(d, k, default=_MISSING):\n    if k in d:\n        return d[k]\n    if default is _MISSING:\n        raise KeyError(k)\n    return default\n\nprint(get({}, "a", None))',
        ["None", "KeyError", "_MISSING", "<object object>"], 0,
        "The caller explicitly passed None as the default.",
        "A private sentinel object lets the function tell 'no default given' apart from 'default is None'. `is` is the right test because only that one object is _MISSING.",
        topic="identity", level=4,
        analogy="Like JS telling undefined (argument not passed) apart from null (passed, but empty)."),
    out('import pandas as pd\ndf = pd.DataFrame({"a": [1, 5], "b": [0, 1]})\ndf[df.a > 1 & df.b < 2]',
        ["ValueError", "TypeError", "Nothing is printed; it selects one row", "KeyError"], 0,
        "& binds tighter than > and <.",
        "It parses as df.a > (1 & df.b) < 2, a chained comparison of Series, which needs bool() of a Series: ValueError. Always bracket each condition: (df.a > 1) & (df.b < 2).",
        topic="precedence", level=4),
    out('import numpy as np\nx = np.int64(5)\nprint(isinstance(x, int), isinstance(x, (int, np.integer)))',
        ["False True", "True True", "False False", "True False"], 0,
        "NumPy has its own integer types.",
        "np.int64 is not a subclass of Python int (unlike np.float64, which subclasses float). Validators that check isinstance(x, int) reject values read from arrays; also accept np.integer, or convert with int(x).",
        topic="type-checks", level=4),
    out('import numpy as np\na = np.array([1, 2])\nb = np.array([1, 2])\nprint(np.array_equal(a, b))\nif a == b:\n    print("same")',
        ["True\nValueError", "True\nsame", "False\nValueError", "ValueError"], 0,
        "a == b compares element by element.",
        "a == b gives array([True, True]), and `if` on a 2-element array is ambiguous. np.array_equal (or (a == b).all()) gives one answer.",
        topic="ml-patterns", level=4),
    out('import math\nloss = float("nan")\nprint(bool(loss), loss > 10, loss < 10, math.isnan(loss))',
        ["True False False True", "False False False True", "True True False True", "False False True True"], 0,
        "NaN is a non-zero float, and every comparison with it is False.",
        "NaN is truthy, and both loss > 10 and loss < 10 are False, so `if loss > 10: stop()` never catches a diverged run. Test math.isnan(loss) (or torch.isnan) explicitly.",
        topic="ml-patterns", level=4),
    out('print([1, "a"] < [2, "b"])\nprint([1, "a"] < [1, 2])',
        ["True\nTypeError", "TypeError", "True\nFalse", "False\nTypeError"], 0,
        "Sequence comparison stops at the first position that differs.",
        "First: 1 < 2 decides it and 'a' is never compared. Second: the 1s tie, so Python compares 'a' with 2 and raises TypeError. Mixed-type lists fail only on some inputs.",
        topic="comparisons", level=4,
        diagram="""
 [1, "a"] vs [2, "b"]:  1 < 2 -> decided (True)
 [1, "a"] vs [1, 2]:    1 == 1 -> next: "a" vs 2 -> TypeError
"""),
    out('class X:\n    def __bool__(self):\n        return 1\n\nbool(X())',
        ["TypeError", "Nothing is printed; it's True", "ValueError", "Nothing is printed; it's False"], 0,
        "__bool__ has a strict return-type rule.",
        "__bool__ must return an actual bool; returning 1 raises TypeError ('__bool__ should return bool, returned int'). __len__, in contrast, must return a non-negative int.",
        topic="truthiness", level=4),
    out('class Y:\n    def __len__(self):\n        return 0\n    def __bool__(self):\n        return True\n\nprint(bool(Y()), len(Y()))',
        ["True 0", "False 0", "TypeError", "True True"], 0,
        "When both are defined, which one does truth testing use?",
        "__bool__ wins; __len__ is only the fallback. So an object can have length 0 and still be truthy, which is why `if obj:` and `if len(obj):` can disagree.",
        topic="truthiness", level=4),
    out('x = None\nprint(x is None is True)',
        ["False", "True", "SyntaxError", "TypeError"], 0,
        "`is` is a comparison operator, so it chains like <.",
        "It means (x is None) and (None is True). The second part is False. Chaining with `is` or `==` almost never does what the author meant.",
        topic="identity", level=4),
    out('def a():\n    print("A")\n    return "a"\n\ndef b():\n    print("B")\n    return "b"\n\nprint((b(), a())[True])',
        ["B\nA\na", "A\na", "B\nA\nb", "B\nb"], 0,
        "Building a tuple evaluates every item.",
        "The old (if_false, if_true)[cond] trick runs BOTH functions before indexing; True is 1, so it picks 'a'. A real conditional expression runs only the chosen branch.",
        topic="ternary", level=4,
        analogy="Cooking both meals and then throwing one away, instead of asking first which one the guest wants."),
    out('from enum import Enum\n\nclass Color(Enum):\n    RED = 1\n    BLUE = 2\n\ndef f(c):\n    match c:\n        case Color.RED:\n            return "r"\n        case _:\n            return "other"\n\nprint(f(Color.RED), f(1))',
        ["r other", "r r", "other other", "SyntaxError"], 0,
        "A dotted name is a value pattern, compared with ==.",
        "Color.RED is looked up and compared with ==. Color.RED == 1 is False for a plain Enum, so f(1) falls to _. (An IntEnum would compare equal to 1.)",
        topic="match-case", level=4),
    out('match True:\n    case 1:\n        print("one")\n    case True:\n        print("true")',
        ["one", "true", "one\ntrue", "SyntaxError"], 0,
        "The literal 1 is compared with ==. What is True == 1?",
        "Number literals match by ==, and True == 1, so the first case wins. (The literals True, False and None themselves match by `is`.) Put case True: first if you need to tell them apart.",
        topic="match-case", level=4),
    out('code = "match p:\\n    case [x, x]:\\n        pass\\n"\ncompile(code, "<demo>", "exec")',
        ["SyntaxError", "Nothing is printed; it compiles", "NameError", "ValueError"], 0,
        "Can one pattern bind the same name twice?",
        "A pattern may bind each name only once ('multiple assignments to name x in pattern'). To check two items are equal, bind different names and add a guard: case [x, y] if x == y.",
        topic="match-case", level=4),
    out('def handle(call):\n    match call:\n        case {"name": "search", "args": {"q": str(q)}}:\n            return f"search {q}"\n        case {"name": name}:\n            return f"unknown tool {name}"\n\nprint(handle({"name": "search", "args": {"q": 42}}))',
        ["unknown tool search", "search 42", "TypeError", "None"], 0,
        "str(q) inside a pattern is a type check, not a conversion.",
        "q is 42, not a str, so the first case fails and the general case catches it. One pattern validates the shape AND the types of a tool-call payload from an LLM.",
        topic="match-case", level=4,
        diagram="""
 {"name": "search", "args": {"q": 42}}
 case {"name": "search", "args": {"q": str(q)}}
            ok                     42 is not str -> fail
 case {"name": name}  -> name = "search"
"""),
    out('x = 2\nprint(x & 1 == 0)',
        ["True", "False", "0", "TypeError"], 0,
        "In Python, & binds tighter than ==. (In C and JS it's the other way round.)",
        "Python reads it as (x & 1) == 0 -> 0 == 0 -> True: an even-number test. The same expression in JavaScript means x & (1 == 0) and gives 0.",
        topic="precedence", level=4,
        diagram="""
 higher  **
         * / // %
         + -
         &  ^  |          <- bitwise
         == != < > in is  <- comparisons
         not, and, or
 lower   x if c else y
"""),
    out('g = (x for x in [0, 3, 0, 5])\nprint(any(g), list(g))',
        ["True [0, 5]", "True [0, 3, 0, 5]", "True []", "False [0, 5]"], 0,
        "any() stops at the first truthy item, and a generator remembers where it stopped.",
        "any() pulls 0 and 3, then stops. The generator now continues from the item after 3, so list(g) gives [0, 5]. Don't reuse a generator after any()/all().",
        topic="any-all", level=4),
    out('data = [3, 8, 1]\nprint([y for x in data if (y := x * 2) > 5])',
        ["[6, 16]", "[16]", "[3, 8]", "SyntaxError"], 0,
        "The walrus computes once in the filter, and the result is reused.",
        "y := x * 2 stores 6, 16, 2; only 6 and 16 pass > 5. Without the walrus you'd compute x * 2 twice, once to filter and once to keep.",
        topic="if-structure", level=4),
    out('for x in [1, 3, 5]:\n    if x % 2 == 0:\n        print("found even")\n        break\nelse:\n    print("no even")',
        ["no even", "found even", "Nothing is printed", "no even\nno even\nno even"], 0,
        "A loop's else runs only if the loop was NOT ended by break.",
        "No even number is found, so break never runs and the loop's else block runs once. It's the built-in 'searched everything, found nothing' branch.",
        topic="if-structure", level=4),
    out('from collections.abc import Mapping\nfrom collections import OrderedDict\nprint(isinstance({}, Mapping), isinstance(OrderedDict(), dict), isinstance([], Mapping))',
        ["True True False", "False True False", "True False False", "TypeError"], 0,
        "Abstract base classes describe behaviour, not one concrete class.",
        "dict and every dict-like class count as a Mapping; OrderedDict subclasses dict; a list is not a mapping. Checking against Mapping accepts any dict-like config object.",
        topic="type-checks", level=4),
    mcq("A config validator checks `isinstance(v, int)` for `epochs`. A user passes `epochs=True`. What happens, and what's the fix?",
        ["It passes as 1 epoch, because bool subclasses int; also reject bools: isinstance(v, int) and not isinstance(v, bool)",
         "It raises TypeError automatically",
         "It passes as 0 epochs; use type(v) == float",
         "Nothing; True is converted to 'True' and rejected"], 0,
        "Where does bool sit in the type hierarchy?",
        "isinstance(True, int) is True, so the validator silently accepts a boolean. Libraries like pydantic have strict modes for exactly this.",
        topic="type-checks", level=4),

    # ---------------------------------------------------------------- concept checks
    mcq("Which condition is True only when a user is logged in AND is an admin?",
        ["logged_in and is_admin", "logged_in or is_admin", "not logged_in and is_admin", "logged_in = is_admin"], 0,
        "Both things must be true at once.",
        "`and` is True only if both sides are True. `or` would let in any logged-in user, and = is assignment (a SyntaxError inside a condition).",
        topic="logic-ops", level=1,
        analogy="A door with two locks: you need both keys to get in. `or` is a door with two separate doors."),
    tf("An `if` statement doesn't need an `else`.", True,
       "Sometimes there's nothing to do when the condition is False.",
       "else (and elif) are optional. Without else, a False condition just skips the block and the program carries on.",
       topic="if-structure", level=1),
    mcq("Which values should you compare with `is` rather than `==`?",
        ["None, True/False and your own sentinel objects", "Any two numbers", "Strings from user input", "Lists with the same items"], 0,
        "`is` asks 'the very same object?'",
        "Use `is` for singletons, where there's only ever one object. For values (numbers, strings, lists) use ==, because equal values can be different objects.",
        topic="identity", level=2),
    mcq("Which one-liner is equivalent to:\n`if ok:` `msg = 'yes'` / `else:` `msg = 'no'`?",
        ['msg = "yes" if ok else "no"', 'msg = ok ? "yes" : "no"', 'msg = if ok "yes" else "no"', 'msg = "yes" else "no" if ok'], 0,
        "Python puts the condition in the middle.",
        "The conditional expression reads 'value if condition else other'. The ?: form is JS/Java/C syntax and is a SyntaxError in Python.",
        topic="ternary", level=2),
    mcq("When is `match/case` clearly better than an `if/elif` chain?",
        ["When you dispatch on the SHAPE of data (parsed JSON, commands, tool calls) and want to unpack it in the same step",
         "Whenever there are more than two branches",
         "When comparing two numbers",
         "Never; match is just slower if/elif"], 0,
        "Think about what patterns can do that == can't.",
        "Patterns check structure, types and values and bind variables at once. For a couple of plain value checks, if/elif is simpler.",
        topic="match-case", level=3,
        analogy="Like route matching in a web framework (/users/:id): the pattern both selects the handler and pulls out the parameters."),
    tf("`any([expensive(x) for x in data])` short-circuits, so `expensive` stops being called after the first True result.", False,
       "Look at the brackets.",
       "The square brackets build the whole list first, calling expensive on every item; only then does any() look at it. Drop the brackets to pass a lazy generator.",
       topic="any-all", level=3),
    fill("To compare two floats safely with a tolerance, use `math.____(a, b)`.", "isclose",
         "It asks 'are these close enough?'",
         "math.isclose uses a relative tolerance (1e-9 by default); pass abs_tol for values near zero. NumPy's version for arrays is np.isclose / np.allclose.",
         topic="comparisons", level=3),
    mcq("Why does NumPy refuse `if arr:` when a Python list happily allows `if lst:`?",
        ["For an array it's unclear whether you mean 'any element true', 'all true' or 'not empty', so NumPy makes you say which",
         "NumPy arrays have no __bool__ at all",
         "Arrays are always truthy, so the check would be pointless",
         "It's a bug kept for backwards compatibility"], 0,
        "A list's truthiness is about its length. What might an array's be about?",
        "For element-wise data, length-based truthiness would be a trap (np.array([0]) is 'non-empty' but all zeros). So NumPy raises and you choose .any(), .all() or .size > 0.",
        topic="truthiness", level=4),
    mcq("Before Python had `x if c else y`, people wrote `c and x or y`. Why was that unreliable?",
        ["If x is falsy (0, '', None), the expression returns y even when c is True",
         "It raised SyntaxError on some platforms",
         "It always evaluated both x and y",
         "and/or didn't short-circuit back then"], 0,
        "Work through c = True, x = 0.",
        "True and 0 gives 0, and 0 or y gives y: the wrong branch. You may still see it in old code; the conditional expression has no such hole.",
        topic="logic-ops", level=4),
    tf("For a NumPy array `arr`, `arr == None` gives an element-wise boolean array, so `if arr == None:` is a bug; `arr is None` is correct.", True,
       "== on arrays compares each element.",
       "arr == None compares every element with None and returns an array, which `if` then refuses. `is None` checks whether the variable holds no array at all.",
       topic="identity", level=4),

    # ---- round 3: conceptual mcq/tf/fill
    # ---------------------------------------------------------------- level 1
    mcq("A function receives `config`. Which value makes `if config:` skip its block?",
        ["{}", '{"lr": 0}', "[None]", '"{}"'], 0,
        "Empty containers are falsy.",
        "An empty dict is falsy, so the block is skipped. {'lr': 0} has one key, [None] has one item and '{}' is a two-character string: all truthy. "
        "Truthiness asks whether the container is empty, not what's inside it. In an API handler, `if not payload:` is the quick 'empty body' check.",
        topic="truthiness", level=1),
    tf("`x = 5` stores 5 in x, while `x == 5` asks whether x is equal to 5.", True,
       "One equals sign or two?",
       "= is assignment, == is a comparison that gives True or False. Writing `if x = 5:` is a SyntaxError in Python, "
       "which protects you from the classic C/JS bug of assigning by accident inside a condition.",
       topic="comparisons", level=1),
    mcq("In one `if / elif / elif / else` chain, how many of the branches run?",
        ["Exactly one", "Every branch whose condition is True", "Always the if and the else", "As many as there are elifs"], 0,
        "Python stops looking once something matches.",
        "Python checks the conditions top to bottom, runs the first True branch and skips the rest; if none is True, else runs. "
        "With an else exactly one branch runs (without else, at most one). If several checks should all fire, use separate ifs.",
        topic="if-structure", level=1,
        diagram="""
 if c1:    --True--> run A ---+
   | False                    |
 elif c2:  --True--> run B ---+--> carry on
   | False                    |
 else:     --------> run C ---+
"""),
    mcq("A spam model outputs a probability `p` between 0 and 1. Which line flags an email as spam using a 0.5 threshold?",
        ["if p >= 0.5:", "if p = 0.5:", "if p => 0.5:", "if 0.5:"], 0,
        "'Greater than or equal' is written with the > first.",
        "p >= 0.5 is True for 0.5 and above. `=` assigns (a SyntaxError in an if), `=>` isn't a Python operator, and `if 0.5:` is always True because 0.5 is non-zero. "
        "Choosing the threshold is a product decision: a higher one means fewer false alarms but more missed spam.",
        topic="ml-patterns", level=1),
    fill("The keyword that turns True into False (and False into True) is ____.", "not",
         "JS and Java write it as !.",
         "`not x` gives the opposite truth value, always as a real bool: not 0 is True, not 'hi' is False. "
         "Python spells all three logic operators as words: and, or, not.",
         topic="logic-ops", level=1),
    tf("`if not x:` runs its block both when `x` is None and when `x` is 0.", True,
       "Both values are falsy.",
       "None, 0, '' and [] are all falsy, so `not x` is True for each of them. That's handy when you mean 'missing or empty', "
       "and a bug when 0 is a real value (a 0% discount, a dropout of 0). Then write `if x is None:`.",
       topic="truthiness", level=1),

    # ---------------------------------------------------------------- level 2
    mcq("`user` may be None. Which condition can never raise AttributeError?",
        ["user is not None and user.is_active",
         "user.is_active and user is not None",
         "user.is_active or user is None",
         "(user is not None) & user.is_active"], 0,
        "`and` stops as soon as its left side is falsy.",
        "With the None check on the left, `and` short-circuits and never reads user.is_active when user is None. Swapping the order reads the attribute first and crashes. "
        "`&` is a bitwise operator, so both sides are always evaluated. Put the protective check first.",
        topic="logic-ops", level=2,
        analogy="The same guard as JS `user && user.isActive`, or `user?.isActive`.",
        diagram="""
 user = None
 user is not None  -> False -> stop: result False
 user.is_active    -> never evaluated
"""),
    mcq("A reviewer flags the second line. What's the best change?",
        ["Rewrite it as an if/elif/else block (or a small function) with one threshold per line",
         "Add brackets around every comparison; that's the only problem",
         "Replace it with `p > 0.7 and 'pos' or 'neg'`",
         "Nothing; chained conditional expressions are what PEP 8 recommends"], 0,
        "Code is read far more often than it's written.",
        "It works (nested conditional expressions group to the right), but three outcomes squeezed into one line are hard to scan and easy to break when a fourth band is added. "
        "One condition per line is clearer. The and/or trick is the old idiom that breaks when the middle value is falsy.",
        topic="ternary", level=2,
        code='p = 0.42\nlabel = "pos" if p > 0.7 else "neg" if p < 0.3 else "unsure"\nprint(label)'),
    fill("Structural pattern matching (`match` / `case`) was added in Python 3.____.", "10",
         "It was released in October 2021.",
         "Python 3.10 (PEP 634). On older interpreters a match statement is a SyntaxError, so check the Python version of your servers or notebook image. "
         "`match` and `case` are soft keywords, so old code that uses them as variable names still runs.",
         topic="match-case", level=2),
    mcq("`if is_admin or is_owner and not is_locked:` is valid Python. Why do reviewers still ask for brackets?",
        ["Readers must remember that `and` binds tighter than `or`; brackets make the intended grouping obvious",
         "Without brackets Python evaluates strictly left to right, so the result is wrong",
         "Brackets make the condition run faster",
         "`not` can't be combined with `and` without brackets"], 0,
        "Is it (admin or owner) and not locked, or admin or (owner and not locked)?",
        "Python reads it as is_admin or (is_owner and not is_locked), so a locked admin still gets in. If the author meant the other grouping, "
        "that's a permissions bug that looks correct in review. Brackets cost nothing and document the intent.",
        topic="precedence", level=2),
    tf("`any()` stops as soon as it finds a truthy item, without looking at the rest.", True,
       "Once one item passes, is the answer still in doubt?",
       "any() short-circuits on the first truthy item and all() on the first falsy one. With a generator, the remaining items aren't even computed, "
       "so `any(is_spam(m) for m in inbox)` can skip most of the work. A list comprehension inside the call would build everything first.",
       topic="any-all", level=2),
    mcq("An order gets a discount if the user is a member, AND free shipping if the total is over 500. Why should these be two separate `if`s rather than `if / elif`?",
        ["The rules are independent; with elif the second check is skipped whenever the first one is True",
         "elif is slower than if",
         "elif can only compare numbers",
         "Two ifs are required whenever there is no else"], 0,
        "Can both perks apply to the same order?",
        "elif means 'only if every earlier check failed'. A member with a 600 total should get both perks, but `if member: ... elif total > 500: ...` gives only the discount. "
        "Use elif for mutually exclusive cases (grade bands, status codes) and separate ifs for independent rules.",
        topic="if-structure", level=2,
        analogy="elif is a menu where you pick one dish; separate ifs are a checklist where every ticked box applies."),
    tf("After `b = a` where `a` is a list, `a is b` is True, and `a.append(1)` also shows up in `b`.", True,
       "Assignment copies the reference, not the list.",
       "b = a gives the same object a second name, so `is` says True and a change through either name is visible through both. "
       "For an independent list use a.copy() or list(a): then a == b is True but a is b is False.",
       topic="identity", level=2),
    mcq("A JSON field `qty` may arrive as `\"42\"`, `42` or `\"-3\"`. Which approach accepts all three as ints and rejects `\"abc\"`?",
        ["Try int(v) and catch TypeError/ValueError, as in the snippet",
         "`if v.isdigit(): v = int(v)`",
         "`if isinstance(v, int):`",
         "`if type(v) == str and v.isnumeric():`"], 0,
        "What does '-3'.isdigit() return?",
        "isdigit() is False for '-3' (the minus isn't a digit) and raises AttributeError on the int 42. isinstance(v, int) rejects '42'. "
        "Trying the conversion and catching the failure handles every case, and it's what validation libraries such as pydantic do for you. Note int(4.9) gives 4, so reject floats separately if that matters.",
        topic="type-checks", level=2,
        code='def parse_qty(v):\n    try:\n        return int(v)\n    except (TypeError, ValueError):\n        return None\n\nprint(parse_qty("-3"), parse_qty(42), parse_qty("abc"))',
        analogy="Like server-side form validation: try to parse the field, and return a 400 if it doesn't parse."),
    fill('For `if val_loss < best_loss:` to count the very first epoch as an improvement, start with `best_loss = float("____")`.', "inf",
         "Every real loss must be smaller than it.",
         "float('inf') is bigger than any finite loss, so the first comparison is always True. Starting at 0 means nothing ever improves; "
         "starting at None makes < raise TypeError. For a metric you maximise, such as accuracy, start at float('-inf').",
         topic="ml-patterns", level=2),
    tf("For built-in types such as int and str, `a != b` always gives the same result as `not (a == b)`.", True,
       "!= asks the opposite question.",
       "For built-ins, != is exactly the negation of ==; even NaN agrees (nan != nan is True, nan == nan is False). "
       "A custom class can define __ne__ separately (by default it inverts __eq__), one more reason to keep __eq__ simple.",
       topic="comparisons", level=2),

    # ---------------------------------------------------------------- level 3
    mcq("`search(q)` returns `[]` when it ran and found nothing, and `None` when the search service failed. Which check alerts only on failure?",
        ["if results is None:", "if not results:", "if results == []:", "if len(results) == 0:"], 0,
        "Two empty-looking values mean two different things.",
        "`not results` is True for both [] and None, so every empty search would page someone. `is None` separates 'failed' from 'found nothing'. "
        "== [] and len() miss the failure (len(None) even raises TypeError). When a function's empty result and its error result are both falsy, test for the one you mean.",
        topic="truthiness", level=3,
        diagram="""
 value   not value   value is None
 []      True        False   <- ran, found nothing
 None    True        True    <- service failed
"""),
    mcq("This 'boolean' helper feeds a JSON API response. What's wrong with it?",
        ["It returns None or '' instead of False for bad input, so the API sends null or \"\" where clients expect false",
         "It raises KeyError when 'name' is missing",
         "It always returns True",
         "`and` can't be used in a return statement"], 0,
        "What does `and` return when its left side is falsy?",
        "`and` returns the first falsy operand itself, so the function hands back None (missing key) or '' (empty name), not False. "
        "json.dumps writes those as null and \"\", and a typed client breaks. Wrap the first part in bool(...) or write an explicit if. There's no KeyError: len() is never reached when the name is missing.",
        topic="logic-ops", level=3,
        code='def has_name(cfg):\n    return cfg.get("name") and len(cfg["name"]) > 2\n\nprint(repr(has_name({})), repr(has_name({"name": ""})))'),
    fill('`sorted(runs)` on a list of result dicts raises TypeError (\'<\' not supported). Fix it with `sorted(runs, ____=lambda r: r["acc"])`.', "key",
         "The keyword argument that tells sorted what to compare.",
         "Dicts have no ordering, so sorting them directly fails. key= turns each dict into something comparable, here its accuracy. "
         "Add reverse=True for best-first, or use max(runs, key=...) if you only need the winner.",
         topic="comparisons", level=3),
    tf("`float('inf') > 10**400` is True, even though 10**400 is too big to convert to a float.", True,
       "Python compares an int with a float exactly, without converting the int first.",
       "Mixed int/float comparisons are exact: the int isn't squeezed into a float (float(10**400) would raise OverflowError). Infinity is bigger than every finite number. "
       "That's why float('inf') is a safe 'nothing seen yet' starting value when you search for a minimum.",
       topic="comparisons", level=3),
    tf("`x is not None` uses the single two-word operator `is not`; it does not mean `x is (not None)`.", True,
       "What would `not None` on its own evaluate to?",
       "`is not` and `not in` are operators in their own right. If it meant x is (not None), it would compare x with True, a completely different test. "
       "That's why `x is not None` is both correct and the PEP 8 style.",
       topic="identity", level=3),
    mcq("Which of these is valid Python?",
        ['key = lambda r: r["acc"] if r["acc"] is not None else 0.0',
         'key = lambda r: if r["acc"]: r["acc"] else: 0.0',
         'key = lambda r: return r["acc"] or 0.0',
         'key = lambda r: {if r["acc"] r["acc"] else 0.0}'], 0,
        "A lambda body must be a single expression.",
        "if blocks and return are statements, which a lambda can't contain. `a if c else b` IS an expression, so it fits in lambdas, comprehensions, default arguments and f-strings. "
        "That's the main reason the conditional expression exists.",
        topic="ternary", level=3),
    mcq("Tool calls that include a query never reach the second case. Why, and what's the fix?",
        ["Mapping patterns match a subset of keys, so the first case also matches messages that have a query; put the more specific case first",
         "The second case needs `**rest` before it can match",
         "Mapping patterns compare the whole dict with ==, so the second case is broken",
         "match only ever tries the first case that mentions a given key"], 0,
        "Does {'tool': 'search'} require the dict to have ONLY that key?",
        "A mapping pattern succeeds when the listed keys are present; extra keys are ignored. So the general pattern swallows the specific one, and Python gives no warning "
        "(it only rejects an unreachable case after a bare-name capture). Order cases from most specific to most general.",
        topic="match-case", level=3,
        code='def route(msg):\n    match msg:\n        case {"tool": "search"}:\n            return "generic search"\n        case {"tool": "search", "query": q}:\n            return f"search {q}"\n    return "unknown"\n\nprint(route({"tool": "search", "query": "gpu"}))',
        analogy="Like registering a catch-all /users/* route before /users/:id/settings in a web router: the catch-all wins first.",
        diagram="""
 msg: {"tool": "search", "query": "gpu"}
 case {"tool": "search"}              -> match (extra key ok)
 case {"tool": "search", "query": q}  -> never tried
"""),
    mcq("A payment webhook does `match event[\"type\"]:` with cases for 'paid' and 'refunded' and no `case _:`. A new type 'disputed' starts arriving. What happens?",
        ["No case matches, no error is raised, and the event is silently ignored; add a final `case _:` that logs or raises",
         "Python raises a MatchError",
         "The last case runs as a fallback",
         "SyntaxError, because every match must end with case _"], 0,
        "Python's match has no built-in 'nothing matched' error.",
        "Unlike exhaustive matches in Rust or Scala, a Python match with no matching case simply does nothing. In a payment webhook that's silent data loss. "
        "A final `case _: raise ValueError(f'unknown event {t}')` (or a logged warning) turns the surprise into a visible error.",
        topic="match-case", level=3,
        analogy="Like an API router with no 404 handler that quietly returns an empty 200 for unknown paths."),
    fill("Of `not`, `and` and `or`, the one that binds most tightly (is applied first) is ____.", "not",
         "It's the one that takes a single operand.",
         "The order is not, then and, then or (like unary minus, then *, then +). So `not a and b or c` means ((not a) and b) or c. "
         "All three bind looser than comparisons, which is why `not x == y` means not (x == y).",
         topic="precedence", level=3),
    mcq("You want to reject a batch of losses if it contains any NaN. Which check is right?",
        ["any(math.isnan(x) for x in batch)",
         "not all(batch)",
         'float("nan") in batch',
         'any(x == float("nan") for x in batch)'], 0,
        "NaN is truthy, 0.0 is falsy, and NaN is equal to nothing.",
        "all(batch) is False here only because of the 0.0; NaN itself is truthy, so that check flags valid zero losses and misses NaN. "
        "`float('nan') in batch` builds a new NaN object, and NaN == NaN is False, so it's never found; == float('nan') fails the same way. "
        "math.isnan (or torch.isnan(t).any() for tensors) is the reliable test.",
        topic="any-all", level=3,
        code='import math\nbatch = [0.4, float("nan"), 0.0]\nprint(any(math.isnan(x) for x in batch), all(batch))'),
    mcq("How would most reviewers restructure this handler?",
        ["Invert each check and return early (guard clauses), leaving the happy path un-nested at the end",
         "Wrap the whole body in try/except",
         "Turn every else into an elif",
         "Squeeze everything into one long conditional expression"], 0,
        "Deal with the failure cases first.",
        "With guard clauses it becomes: if req is None: return 'no request'; if not req.get('user'): return 'no user'; ... then return 'process'. "
        "Each rule sits next to its error result, and adding a new check doesn't push the main logic further right. It's the same early-return validation you'd write in an Express or FastAPI handler.",
        topic="if-structure", level=3,
        code='def handle(req):\n    if req is not None:\n        if req.get("user"):\n            if req.get("items"):\n                return "process"\n            else:\n                return "no items"\n        else:\n            return "no user"\n    else:\n        return "no request"\n\nprint(handle({"user": "a", "items": [1]}))',
        diagram="""
 nested ("arrow code"):     guard clauses:
 if a:                      if not a: return E1
     if b:                  if not b: return E2
         if c:              if not c: return E3
             work()         work()
"""),
    mcq("`add_tags(tags)` should accept one tag string or a list of tags. Why can't `isinstance(tags, Iterable)` tell the two apart?",
        ["A str is itself an iterable of characters; check isinstance(tags, str) first and wrap it in a list",
         "Iterable only recognises lists",
         "isinstance doesn't work with abstract base classes",
         "Strings were iterable only in Python 2"], 0,
        "What does looping over 'gpu' give you?",
        "Strings are iterable, so 'gpu' passes the Iterable check and would be stored as three tags: 'g', 'p', 'u'. "
        "The standard pattern is `if isinstance(tags, str): tags = [tags]` before treating it as a collection. Pattern matching builds the same rule in: sequence patterns refuse str.",
        topic="type-checks", level=3,
        code='from collections.abc import Iterable\nprint(isinstance("gpu", Iterable), list("gpu"))'),
    mcq("Epochs are numbered from 0. You want to validate after every 5th epoch (the 5th, 10th, 15th...). Which condition is right?",
        ["(epoch + 1) % 5 == 0", "epoch % 5 == 0", "epoch % 5 == 1", "epoch // 5 == 0"], 0,
        "In a 0-based loop, what is the number of the 5th epoch?",
        "The 5th epoch is epoch 4, so add 1 before the modulo. epoch % 5 == 0 also fires at epoch 0, validating an untrained model, and then always one epoch early. "
        "The same off-by-one shifts when checkpoints get saved.",
        topic="ml-patterns", level=3,
        diagram="""
 epoch:           0  1  2  3  4  5  6  7  8  9
 (epoch+1)%5==0:              Y              Y
 epoch%5==0:      Y              Y
"""),
    mcq("Early-stopping code written for loss (`if metric < best: best = metric; save()`) is reused to monitor validation accuracy. What happens?",
        ["Every drop in accuracy counts as an improvement, so it keeps the worst checkpoint; flip the comparison (or use mode='max')",
         "It raises TypeError because accuracy is a float",
         "It works the same, because both are just numbers",
         "Training always stops after the first epoch"], 0,
        "Is a smaller accuracy better?",
        "The comparison direction encodes what 'better' means. For loss lower is better; for accuracy, F1 or AUC higher is better. "
        "Keras and PyTorch Lightning callbacks take mode='min' / 'max' for exactly this reason, and best must then start at float('-inf') instead of float('inf').",
        topic="ml-patterns", level=3),

    # ---------------------------------------------------------------- level 4
    mcq("Why is this 'sorted' list not sorted at all, with no error raised?",
        ["Every comparison with NaN is False, which breaks the total order the sort relies on, so it silently returns a garbled order",
         "sorted() skips NaN and sorts the remaining numbers around it",
         "NaN is treated as 0, so it is placed among the smallest values",
         "sorted() only checks ordering for strings, never for floats"], 0,
        "Is nan < 1? Is 1 < nan?",
        "Sorting assumes that for any a and b, either a < b, b < a, or they're equivalent. NaN looks 'equivalent' to everything, yet 1 < 3, so the algorithm makes inconsistent decisions: "
        "here the output is [3, nan, 1, 2]. A NaN metric can scramble a leaderboard without a crash. Filter with math.isnan first, or sort with key=lambda x: (math.isnan(x), x) to push NaNs to the end.",
        topic="comparisons", level=4,
        code='vals = [3, float("nan"), 1, 2]\nprint(sorted(vals))',
        diagram="""
 3 < nan? False   nan < 3? False   -> "equivalent"
 1 < nan? False   nan < 1? False   -> "equivalent"
 but 1 < 3 is True -> no consistent order exists
"""),
    tf("If a class defines only `__lt__`, then `b > a` still works for two instances, because Python falls back to the reflected `a.__lt__(b)`.", True,
       "> and < are each other's mirror image.",
       "For b > a Python first tries b.__gt__(a); the inherited default returns NotImplemented, so it tries the reflection a.__lt__(b). That's why __lt__ alone is enough for sorted() and max(). "
       "It does NOT give you <= or >= (those raise TypeError): use functools.total_ordering to fill in the rest.",
       topic="comparisons", level=4),
    mcq("Why does this print True even though `b.__bool__` returns False?",
        ["Special methods are looked up on the class, not the instance, so the instance attribute is ignored",
         "A lambda can't return False",
         "bool() caches the result of its first call",
         "__bool__ only takes effect if __len__ is also defined"], 0,
        "Where does bool() look for __bool__: on b, or on type(b)?",
        "Implicit calls such as bool(x), len(x), x + y and hash(x) look the dunder up on type(x) and skip the instance dict. That's faster and keeps every instance of a class consistent. "
        "To change truthiness, define __bool__ (or __len__) in the class body. The same rule is why monkey-patching obj.__len__ on one object does nothing.",
        topic="truthiness", level=4,
        code='class Batch:\n    pass\n\nb = Batch()\nb.__bool__ = lambda: False\nprint(bool(b))',
        diagram="""
 bool(b)
   -> type(b).__bool__ ?   not on Batch
   -> type(b).__len__  ?   not on Batch
   -> True (default)
 b.__dict__["__bool__"]    never consulted
"""),
    mcq("A helper checks `if ok is True:` and silently skips every result computed with NumPy. Why?",
        ["`scores[0] > 0.5` is a NumPy bool scalar, a different object from Python's True; use `if ok:` or bool(ok)",
         "NumPy comparisons return the strings 'True' and 'False'",
         "`is True` always returns False on Windows",
         "NumPy scalars are always falsy"], 0,
        "`is` checks for the exact same object.",
        "np.True_ prints as True (and in NumPy 2 its class is even named 'bool'), but it isn't the Python singleton True, so `is True` is False. "
        "Plain truthiness and == True both work. The same goes for values from pandas and PyTorch: `is` is only safe for None and your own sentinels.",
        topic="identity", level=4,
        code='import numpy as np\nscores = np.array([0.9, 0.4])\nok = scores[0] > 0.5\nprint(ok, type(ok).__name__, ok is True)',
        analogy="Like two passports with the same name and photo issued by different countries: equal for most purposes, but not the same document."),
    mcq("This works, but changing the case to `case Point(0, y):` raises TypeError when the match runs. What makes positional sub-patterns work?",
        ["A `__match_args__` tuple saying which attributes the positions map to; dataclasses and namedtuples generate it",
         "Defining __eq__ on Point",
         "Making Point a subclass of tuple",
         "Adding __slots__ = ('x', 'y')"], 0,
        "How would Python know that position 0 means .x?",
        "Keyword sub-patterns just read attributes. Positional ones need the class to declare an order: `__match_args__ = ('x', 'y')`. Without it you get "
        "'Point() accepts 0 positional sub-patterns (2 given)'. @dataclass and namedtuple set __match_args__ from their fields, which is why they work out of the box.",
        topic="match-case", level=4,
        code='class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\ndef where(p):\n    match p:\n        case Point(x=0, y=y):\n            return f"y-axis {y}"\n    return "other"\n\nprint(where(Point(0, 5)))'),
    tf("The pattern `case {}:` matches only an empty dict.", False,
       "A mapping pattern checks that the keys it lists are present.",
       "With no keys listed there's nothing to check, so `case {}:` matches every mapping, empty or not. To match only an empty dict add a guard, "
       "e.g. `case {} if len(event) == 0:`. Easy to miss when routing JSON payloads, because the 'empty' case quietly catches everything below it.",
       topic="match-case", level=4),
    mcq("How does Python group the last assignment?",
        ["(cached or compute()) if use_cache else None",
         "cached or (compute() if use_cache else None)",
         "(cached or compute() if use_cache) else None",
         "It's a SyntaxError without brackets"], 0,
        "The conditional expression binds more loosely than `or`.",
        "`a if c else b` is the loosest operator apart from lambda and :=, so the whole `or` on its left becomes the 'true' branch. "
        "use_cache is False, so value is None even though cached holds 'hit'; the second grouping would give 'hit'. Add brackets whenever a conditional expression meets and/or.",
        topic="precedence", level=4,
        code='cached, use_cache = "hit", False\n\ndef compute():\n    return 5\n\nvalue = cached or compute() if use_cache else None\nprint(value)',
        diagram="""
 cached or compute() if use_cache else None
 '-- true branch --'    '- test -'    '-else-'
 = (cached or compute()) if use_cache else None
"""),
    tf("For a 2-D NumPy array `m`, the built-in `any(m)` checks every element, just like `m.any()`.", False,
       "What does iterating over a 2-D array give you?",
       "Built-in any() iterates the first axis, so it receives whole rows and calls bool(row), which raises ValueError for rows with more than one element. "
       "m.any() (or np.any(m)) reduces over every element in C. On arrays, prefer the array method over Python's any/all: correct for any shape and much faster.",
       topic="any-all", level=4),
    mcq("A validator runs `isinstance(value, list[int])` to check a list of ids. What happens?",
        ["TypeError: isinstance doesn't accept parameterized generics; check isinstance(value, list), then each item",
         "It checks that every item in the list is an int",
         "It returns True for any list",
         "It returns False for any list"], 0,
        "Type hints and runtime checks live in different worlds.",
        "list[int] is a hint for static type checkers; at runtime isinstance raises 'argument 2 cannot be a parameterized generic'. "
        "Write isinstance(value, list) and all(isinstance(i, int) and not isinstance(i, bool) for i in value), or let pydantic validate against the annotation.",
        topic="type-checks", level=4,
        analogy="Like TypeScript types: they guide the compiler but vanish at runtime, so the server still has to validate the JSON it receives."),
    mcq("A model-serving endpoint must reject invalid probabilities. Which guard also rejects NaN?",
        ["if not 0 <= p <= 1: raise ValueError(...)",
         "if p < 0 or p > 1: raise ValueError(...)",
         "if p is None: raise ValueError(...)",
         "if not p: raise ValueError(...)"], 0,
        "One guard asks 'is it invalid?', the other asks 'is it valid?'. Which question does NaN answer 'no' to?",
        "Every comparison with NaN is False. 'p < 0 or p > 1' asks 'is it invalid?', NaN answers no, and it gets through. 'not (0 <= p <= 1)' asks 'is it valid?', NaN answers no, and it's rejected. "
        "Describe the valid range (an allow-list) and add math.isnan when you want a clearer error. `not p` misses NaN because NaN is truthy.",
        topic="ml-patterns", level=4,
        code='p = float("nan")\nprint(p < 0 or p > 1, not 0 <= p <= 1)',
        diagram="""
 p = nan
 p < 0 or p > 1     -> False or False -> passes  (bad)
 not (0 <= p <= 1)  -> not False      -> rejected (good)
"""),

    # ---- round 3 pass 2: conceptual mcq/tf/fill
    # ---------------------------------------------------------------- level 1
    mcq("What type of value does a comparison such as `3 > 2` produce?",
        ["bool (True or False)", "int (1 or 0)", "str ('True' or 'False')", "None, because it only checks"], 0,
        "It's the type of value an `if` is happiest with.",
        "Every comparison gives a bool: True or False. bool happens to be a subclass of int, which is why True + True is 2, "
        "but type(3 > 2) is bool, not int. Knowing this helps when you store a check in a variable, e.g. `is_better = val_loss < best`.",
        topic="comparisons", level=1),
    tf("An empty dict `{}` is falsy, so `if {}:` skips its block.", True,
       "Empty containers behave the same way, whatever kind of container they are.",
       "Empty dicts, lists, tuples, sets and strings are all falsy. That's why `if config:` is a quick way to check that a loaded config isn't empty. "
       "The catch: a dict like {'debug': False} is truthy, because it has one key, even though the value inside is False.",
       topic="truthiness", level=1,
       analogy="Like checking whether a box has anything in it, not whether the thing in it is worth anything."),
    mcq("Training should stop when the epoch count reaches `max_epochs` OR the loss drops below 0.01. Which line is right?",
        ["if epoch >= max_epochs or loss < 0.01:",
         "if epoch >= max_epochs and loss < 0.01:",
         "if epoch >= max_epochs || loss < 0.01:",
         "if (epoch >= max_epochs, loss < 0.01):"], 0,
        "Either reason is enough on its own.",
        "`or` is True when at least one side is True, so either condition stops training. `and` would wait for both, so a run that never "
        "reaches 0.01 keeps training past max_epochs. `||` is JS/Java syntax and a SyntaxError in Python; a tuple of two bools is always truthy.",
        topic="logic-ops", level=1),
    mcq("In an `if / elif / else` chain, when does the `else` block run?",
        ["Only when none of the conditions above it were True",
         "Always, after the if block has run",
         "When the last elif is False, even if an earlier one was True",
         "Only when the if condition raises an error"], 0,
        "It's the 'none of the above' branch.",
        "Python checks the if, then each elif, and runs the first True one. else runs only when every one of them was False. "
        "It is not a 'finally' that always runs, and it has nothing to do with errors (that's try/except).",
        topic="if-structure", level=1,
        diagram="""
 if A:    -> A true?            run, done
 elif B:  -> A false, B true?   run, done
 else:    -> A false, B false   run
"""),
    tf("You can put an `elif` after the `else` in the same if-chain.", False,
       "Think about what 'else' means: everything that's left.",
       "else must come last: it already catches every remaining case, so an elif after it could never run, and Python reports a SyntaxError. "
       "The order is always: one if, any number of elif, then at most one else.",
       topic="if-structure", level=1),
    fill("To run a block only when `x` holds a real value (not None), write `if x is ____ None:`.", "not",
         "Two words that work as one operator.",
         "`is not` is a single operator meaning 'is a different object from'. `x is not None` is the PEP 8 spelling; it reads better than `not x is None` "
         "and, unlike `if x:`, it still lets 0 and empty strings through.",
         topic="identity", level=1),
    tf("`if accuracy >= 0.9:` runs its block when accuracy is exactly 0.9.", True,
       "Read >= aloud.",
       ">= means 'greater than or equal to', so the exact threshold value passes. With > it would not. Whether the boundary passes is a real decision "
       "in ML code: a 'must beat 0.9' rule and an 'at least 0.9' rule treat a 0.9 run differently, so say which you mean.",
       topic="ml-patterns", level=1),
    mcq("Which line checks whether `x` is a string?",
        ["isinstance(x, str)", "x.isstr()", "type(x) = str", "str(x) == x"], 0,
        "The built-in takes the value and a type.",
        "isinstance(value, type) is the standard check. Strings have no isstr() method, `type(x) = str` is an assignment (SyntaxError), "
        "and str(x) == x is True for strings but is a slow, roundabout way to ask.",
        topic="type-checks", level=1,
        analogy="Like `typeof x === 'string'` in JavaScript, but it also accepts subclasses of str."),
    fill("`____(score > 0.9 for score in scores)` is True if at least one score is above 0.9.", "any",
         "'Is there at least one?' in three letters.",
         "any() returns True as soon as it sees one truthy item; all() needs every item to be truthy. "
         "So any(...) answers 'did any run beat 0.9?' and all(...) answers 'did every run beat 0.9?'.",
         topic="any-all", level=1),
    mcq("In a `match` statement, what does `case _:` do?",
        ["Catches any value that no earlier case matched",
         "Matches only the value None",
         "Matches only an empty string",
         "Skips the match statement entirely"], 0,
        "_ is a wildcard.",
        "`_` matches anything and binds nothing, so as the last case it works like `default:` in a JS or Java switch. "
        "Without it, a value that matches no case is silently ignored, with no error.",
        topic="match-case", level=1),

    # ---------------------------------------------------------------- level 2
    mcq("Which is the clearest way to write `x == 1 or x == 2 or x == 3`?",
        ["x in (1, 2, 3)", "x == (1 or 2 or 3)", "x == 1 or 2 or 3", "x in range(3)"], 0,
        "Ask 'is x one of these?'.",
        "`in` checks membership in one step. `1 or 2 or 3` evaluates to 1, so x == (1 or 2 or 3) only tests 1. `x == 1 or 2 or 3` is always truthy, "
        "because the bare 2 counts as True. range(3) is 0, 1, 2, so it misses 3 and accepts 0.",
        topic="comparisons", level=2,
        diagram="""
 x == (1 or 2 or 3)  ->  x == 1          (or returns 1)
 x == 1 or 2 or 3    ->  False or 2 -> 2 (always truthy)
 x in (1, 2, 3)      ->  checks each     (what you meant)
"""),
    mcq("`find_index(items, target)` returns the position of a match (which can be 0) or None if there is none. Which caller check is correct?",
        ["if idx is not None:", "if idx:", "if idx > 0:", "if idx != False:"], 0,
        "What happens when the match is the very first item?",
        "A match at position 0 gives idx = 0, which is falsy, so `if idx:` and `idx > 0` both treat a real match as 'not found'. "
        "`idx != False` is also wrong, because 0 == False. Only `is not None` separates 'found at 0' from 'not found'. str.find avoids this by returning -1 instead.",
        topic="truthiness", level=2),
    mcq("`name = user_input or 'anonymous'`. When does `name` become 'anonymous'?",
        ["Whenever user_input is falsy: None, '', 0, [] and so on",
         "Only when user_input is None",
         "Only when reading user_input raises an error",
         "Never; `or` always returns True or False"], 0,
        "`or` hands back one of its two operands.",
        "`a or b` returns a if a is truthy, otherwise b. So any falsy input, including an empty string, falls back to the default. "
        "That's fine for names, but wrong for values where 0 or '' are legitimate; use `x if x is not None else default` there.",
        topic="logic-ops", level=2,
        diagram="""
 user_input  -> truthy?  yes -> name = user_input
                         no  -> name = 'anonymous'
 falsy: None  ''  0  0.0  []  {}
"""),
    mcq("What is a conditional expression (`a if cond else b`) best used for?",
        ["Choosing between two values in one place, e.g. inside an assignment or argument",
         "Running one of two multi-line blocks of statements",
         "Replacing every if/elif chain to save lines",
         "Looping until a condition becomes False"], 0,
        "It's an expression: it produces a value.",
        "Use it when the only difference between the branches is the value, e.g. `device = 'cuda' if has_gpu else 'cpu'`. "
        "Statements (loops, multiple assignments, raising) belong in a normal if block, and nested one-liners for long chains are harder to read than elif.",
        topic="ternary", level=2,
        analogy="Like `cond ? a : b` in JS or Java: great inside an expression, painful when stretched to do real work."),
    tf("`match` can only compare a value against int and string literals, like a C `switch`.", False,
       "Remember the dict and list patterns you've seen.",
       "Structural pattern matching also destructures: sequence patterns like [x, *rest], mapping patterns like {'type': 'click'}, "
       "class patterns like Point(x=0), plus | alternatives and `if` guards. That's what makes it useful for routing JSON events, not just status codes.",
       topic="match-case", level=2),
    fill("`not a == b` works, but the clearer spelling of the same test is `a ____ b`.", "!=",
         "There's a dedicated 'not equal' operator.",
         "== binds tighter than not, so `not a == b` is `not (a == b)`. a != b says the same thing directly, and readers don't have to "
         "think about precedence. For None, the equivalent is `x is not None`.",
         topic="precedence", level=2),
    mcq("Before training, you want to check that every key in `REQUIRED = ['lr', 'epochs', 'batch_size']` is present in `cfg`. Which line does that?",
        ["all(k in cfg for k in REQUIRED)",
         "any(k in cfg for k in REQUIRED)",
         "REQUIRED in cfg",
         "all(cfg)"], 0,
        "Every required key, not just some of them.",
        "all() over a generator checks each key and stops at the first missing one. any() passes if just one key is there. `REQUIRED in cfg` asks whether the "
        "list itself is a key, which raises TypeError because lists are unhashable. all(cfg) checks the keys' truthiness. set(REQUIRED) <= cfg.keys() also works.",
        topic="any-all", level=2),
    mcq("What does `continue` do here?",
        ["Skips the rest of this loop iteration and moves on to the next batch",
         "Ends the whole loop",
         "Restarts the loop from the first batch",
         "Does nothing; it's a placeholder like pass"], 0,
        "It's the loop version of an early return.",
        "`continue` jumps straight to the next iteration, so bad batches are skipped and training goes on. `break` would end the loop and `pass` would do nothing, "
        "letting the None batch reach the training code. Guard + continue keeps the main path un-nested.",
        topic="if-structure", level=2,
        code='batches = [[1, 2], None, [3]]\nfor batch in batches:\n    if batch is None:\n        continue\n    print("train on", batch)',
        diagram="""
 batch [1, 2] -> guard no  -> train
 batch None   -> guard yes -> continue (skip)
 batch [3]    -> guard no  -> train
"""),
    mcq("A string from a CSV, such as '3.5', '-2' or 'n/a', should become a float when it can. Which check handles all of these?",
        ["try: float(s) / except ValueError: handle the bad value",
         "if s.isdigit(): float(s)",
         "if isinstance(s, float): float(s)",
         "if s.isnumeric(): float(s)"], 0,
        "Which characters do isdigit and isnumeric accept?",
        "isdigit() and isnumeric() are False for '3.5' and '-2' (the dot and minus aren't digits), and isinstance(s, float) is False because s is a str. "
        "Trying the conversion and catching ValueError is the reliable test, and it's the Python 'easier to ask forgiveness' style.",
        topic="type-checks", level=2,
        analogy="Like calling an API and handling a 400 response, instead of re-implementing all of the server's validation rules on the client."),
    tf("`probs > 0.5` on a NumPy array gives an array of True/False values, one per element.", True,
       "NumPy applies comparisons element by element.",
       "Comparisons on arrays are vectorised: np.array([0.2, 0.7]) > 0.5 gives array([False, True]). That mask can pick rows, be summed to count "
       "positives, or be turned into labels with .astype(int). What it can't do is sit directly in an `if`, which needs a single True/False.",
       topic="ml-patterns", level=2),

    # ---------------------------------------------------------------- level 3
    mcq("Rank experiment runs by highest accuracy, breaking ties by lowest loss. Which sort key does it?",
        ["sorted(runs, key=lambda r: (-r['acc'], r['loss']))",
         "sorted(runs, key=lambda r: (r['acc'], r['loss']), reverse=True)",
         "sorted(runs, key=lambda r: r['acc'] - r['loss'])",
         "sorted(runs, key=lambda r: (r['loss'], -r['acc']))"], 0,
        "Tuples compare element by element, and reverse=True flips every element.",
        "A tuple key compares acc first and only looks at loss on a tie. Negating acc gives 'highest first' while loss stays 'lowest first'. "
        "reverse=True flips both, so ties end up with the HIGHEST loss first. Subtracting mixes two scales into one number, and the last key ranks by loss first.",
        topic="comparisons", level=3,
        diagram="""
 key = (-acc, loss)
 run A: (-0.91, 0.30)
 run B: (-0.91, 0.25)   tie on -acc -> compare loss
 run C: (-0.88, 0.10)
 order: B, A, C
"""),
    tf("`1 == 1.0 == True` evaluates to True.", True,
       "Expand the chain into two comparisons joined by `and`.",
       "The chain means (1 == 1.0) and (1.0 == True). int, float and bool compare by numeric value, and True is 1, so both parts are True. "
       "It's also why 1, 1.0 and True collide as the same dict key or set member.",
       topic="comparisons", level=3),
    mcq("Which condition is equivalent to `not (is_valid and is_ready)`?",
        ["not is_valid or not is_ready",
         "not is_valid and not is_ready",
         "is_valid or is_ready",
         "not is_valid and is_ready"], 0,
        "De Morgan's law: pushing `not` inside flips the operator.",
        "'Not both' is True when at least one is missing: not (a and b) == (not a) or (not b). The tempting `not a and not b` means 'neither', "
        "which is stricter. Getting this wrong in a guard clause lets half-ready jobs run, or blocks jobs that are almost ready.",
        topic="logic-ops", level=3,
        diagram="""
 a  b  | not(a and b) | not a or not b | not a and not b
 T  T  |     F        |      F         |      F
 T  F  |     T        |      T         |      F   <- differs
 F  T  |     T        |      T         |      F   <- differs
 F  F  |     T        |      T         |      T
"""),
    fill("An `__eq__` that doesn't know how to compare with the other object's type should return ____, so Python can try the other operand instead.", "NotImplemented",
         "A built-in constant, not an exception.",
         "Returning NotImplemented (not raising NotImplementedError, and not returning False) tells Python to try other.__eq__(self). "
         "If both sides give up, == falls back to identity. Returning False directly blocks the other class from ever answering.",
         topic="comparisons", level=3),
    mcq("A reviewer flags `print('saved') if ok else print('skipped')`. Why?",
        ["It uses an expression only for its side effects; an if/else statement says that more clearly",
         "It's a SyntaxError: print can't appear inside a conditional expression",
         "Both print calls always run",
         "The result of the expression is printed a second time"], 0,
        "It works. The problem is what it's for.",
        "The code runs and only one print fires, but the expression builds a value (None) that's thrown away. A conditional expression is for choosing a value; "
        "when each branch does something, a two-line if/else is easier to read, debug and extend.",
        topic="ternary", level=3,
        analogy="Like using a JS ternary as a statement: `ok ? save() : skip();`. Linters flag it there too."),
    mcq("What is the difference between `case [x, y]:` and `case (x, y):`?",
        ["None: both are sequence patterns that match any length-2 sequence, list or tuple",
         "The first matches only lists, the second only tuples",
         "The second is a class pattern for tuple",
         "The first is a SyntaxError; sequence patterns must use round brackets"], 0,
        "In a pattern, brackets don't name a type.",
        "Square and round brackets mean the same in patterns: a sequence of that length (str and bytes excluded). To insist on a type, use a class pattern: "
        "`case list([x, y]):` or `case tuple((x, y)):`. Easy to trip on when JSON turns tuples into lists, which still match either way.",
        topic="match-case", level=3,
        code='for p in ([1, 2], (1, 2)):\n    match p:\n        case (x, y):\n            print("pair", type(p).__name__)'),
    tf("In `case 'a' | 'b' as letter:`, the name `letter` is bound to whichever alternative matched.", True,
       "`as` applies to the whole or-pattern on its left.",
       "The | alternatives are tried left to right, and `as` captures the subject value that matched, so letter is 'a' or 'b'. "
       "Handy when routing a few aliases to one branch and still needing to know which one came in.",
       topic="match-case", level=3,
       code='match "b":\n    case "a" | "b" as letter:\n        print(letter)'),
    mcq("`scores` may be an empty list. Which threshold check never raises?",
        ["any(s > 0.9 for s in scores)",
         "max(scores) > 0.9",
         "sorted(scores)[-1] > 0.9",
         "scores[0] > 0.9 or max(scores[1:]) > 0.9"], 0,
        "What does max() do with nothing to compare?",
        "max([]) raises ValueError and indexing an empty list raises IndexError. any() over an empty iterable just returns False. If you do want max, "
        "pass a default: max(scores, default=0.0) > 0.9. An evaluation step that crashes on an empty validation split is a common late-night bug.",
        topic="any-all", level=3),
    mcq("When can nested `if a:` / `    if b:` / `        do()` be safely merged into `if a and b:` / `    do()`?",
        ["When neither if has an elif or else, and nothing else runs between them",
         "Always; the two forms are identical",
         "Only when a and b are both booleans",
         "Never; `and` evaluates b even when a is False"], 0,
        "Picture where an else would attach in each version.",
        "With no else branches, both forms run do() only when a and b are true, and `and` short-circuits just like the nested if. "
        "An else on the inner if (a true, b false) or code between the two ifs has nowhere to go after the merge, so check for those first.",
        topic="if-structure", level=3,
        diagram="""
 if a:              if a and b:
     if b:              do()
         do()
     else:          <- 'a but not b' path
         log()         has nowhere to go
"""),
    tf("`isinstance(np.float64(1.0), float)` is True, but `isinstance(np.float32(1.0), float)` is False.", True,
       "Only one NumPy float type has the same width as a Python float.",
       "np.float64 subclasses Python's float (both are 64-bit doubles); np.float32 doesn't. A validator using isinstance(x, float) accepts one and rejects "
       "the other, which bites when a model switches to float32. Accept both with isinstance(x, (float, np.floating)), or convert with float(x) first.",
       topic="type-checks", level=3,
       code='import numpy as np\nprint(isinstance(np.float64(1.0), float), isinstance(np.float32(1.0), float))'),
    mcq("A training loop must stop when the loss is NaN or infinite. Which guard catches both?",
        ["if not math.isfinite(loss): stop()",
         "if math.isnan(loss): stop()",
         "if loss != loss: stop()",
         "if loss > 1e9: stop()"], 0,
        "inf is a number, just not a finite one.",
        "math.isfinite is False for nan, inf and -inf. isnan and the `loss != loss` trick only catch NaN, and `loss > 1e9` misses NaN (every comparison with "
        "NaN is False) and -inf. Exploding losses usually go inf first and NaN a step later, so isfinite stops the run earlier.",
        topic="ml-patterns", level=3,
        analogy="Like a health check that fails on both 'no response' and 'response time is infinite', not just one of them."),

    # ---------------------------------------------------------------- level 4
    mcq("Both classes' `__eq__` return NotImplemented. What do `a == b` and `a < b` do?",
        ["a == b is False (Python falls back to identity); a < b raises TypeError",
         "Both raise TypeError",
         "a == b returns the NotImplemented object itself; a < b is False",
         "Both are False"], 0,
        "Equality and ordering have different last resorts.",
        "For ==, Python tries a.__eq__(b), then the reflected b.__eq__(a); if both return NotImplemented it falls back to `a is b`. "
        "Ordering has no sensible default, so after __lt__ and the reflected __gt__ both give up you get TypeError. That's why `x == y` never fails "
        "between unrelated types but sorting a mixed list does.",
        topic="comparisons", level=4,
        code='class A:\n    def __eq__(self, other):\n        return NotImplemented\n\nclass B:\n    def __eq__(self, other):\n        return NotImplemented\n\na, b = A(), B()\nprint(a == b, a == a)',
        diagram="""
 a == b:  a.__eq__(b) -> NotImplemented
          b.__eq__(a) -> NotImplemented
          fallback: a is b -> False
 a < b:   a.__lt__(b) -> NotImplemented
          b.__gt__(a) -> NotImplemented
          fallback: none -> TypeError
"""),
    mcq("Both objects count their `__bool__` calls. After `if a and b: pass`, how many times was each called?",
        ["a once, b once",
         "a once, b twice: once by `and`, once by `if`",
         "a twice, b once",
         "a once, b never: `and` returns b without testing it"], 0,
        "CPython compiles `if a and b:` into two conditional jumps.",
        "In an if, CPython never builds the value of `a and b`: it tests a, jumps away if false, then tests b. So each __bool__ runs exactly once. "
        "The last option describes `x = a and b`, where b is returned untested; the later `if x:` then tests it once. "
        "This matters when __bool__ is costly, e.g. a lazy result that has to query a database or sync a GPU to answer.",
        topic="logic-ops", level=4,
        code='calls = {"a": 0, "b": 0}\n\nclass C:\n    def __init__(self, k):\n        self.k = k\n    def __bool__(self):\n        calls[self.k] += 1\n        return True\n\na, b = C("a"), C("b")\nif a and b:\n    pass\nprint(calls)'),
    tf("In CPython, `tuple() is tuple()` is True.", True,
       "Immutable empty objects are cheap to share.",
       "CPython keeps a single empty tuple and hands it out every time, so both calls return the same object. It's an implementation detail, like small-int "
       "caching: other interpreters may differ, and code should compare tuples with ==. Interviewers use it to check you know `is` tests identity, not value.",
       topic="identity", level=4),
    tf("Matching `case {'x': v}:` against a `defaultdict(int)` that has no key 'x' quietly inserts 'x' with the value 0.", False,
       "Mapping patterns look keys up without triggering __missing__.",
       "Mapping patterns use the mapping's get() method, which never calls defaultdict's default_factory, so the pattern simply fails and the dict stays "
       "empty. By contrast `if d['x'] == 0:` would insert the key. Good news for routing over defaultdict-based configs: matching has no side effects.",
       topic="match-case", level=4,
       code='from collections import defaultdict\n\nd = defaultdict(int)\nmatch d:\n    case {"x": v}:\n        print("matched", v)\n    case _:\n        print("no match", dict(d))'),
    mcq("Why is `if flag == not other:` a SyntaxError?",
        ["`not` binds more loosely than ==, so `not other` can't be the right operand of ==; write `flag == (not other)`",
         "`not` is a function and needs brackets: not(other)",
         "== can't compare two booleans",
         "It's valid and means `not (flag == other)`"], 0,
        "Where does `not` sit in the precedence table compared with comparisons?",
        "The grammar puts `not` below the comparison operators, so after == the parser expects an operand with higher precedence and finds `not`. "
        "Brackets fix it. For two real bools, `flag != other` is the cleaner form; with truthy non-bool values the two aren't the same, so be explicit.",
        topic="precedence", level=4),
    fill("any() and all() always return a bool. To get the first truthy item itself, write `____((v for v in items if v), None)`.", "next",
         "The built-in that pulls one item out of an iterator.",
         "next(generator, default) returns the first item the generator produces, or the default if it's empty, and stops there: the same short-circuit as any(). "
         "`or` chains also return the item, but only for a fixed number of operands.",
         topic="any-all", level=4),
    mcq("Inside a GPU training loop, `if loss < best_loss:` works but makes each step noticeably slower. Why?",
        ["Turning a CUDA tensor into a Python bool forces the CPU to wait for the GPU to finish all queued work",
         "Comparing tensors is O(n) in the number of model parameters",
         "The comparison copies the model weights to the CPU",
         "Python compares tensors with string formatting"], 0,
        "GPU work is launched asynchronously. When does Python need the actual number?",
        "CUDA kernels are queued and run in the background, and Python races ahead. An `if` needs a real True/False, so bool(tensor) blocks until the loss is "
        "computed and copied back: a sync point every step. Compare less often (e.g. once per epoch), or keep the bookkeeping on the GPU with torch.minimum and check it later.",
        topic="ml-patterns", level=4,
        analogy="Like awaiting every network call inside a loop instead of firing them all and awaiting once at the end.",
        diagram="""
 CPU: launch fwd | launch bwd | if loss < best: WAIT......| next
 GPU:   [ fwd ........ ][ bwd ........ ]   -> value ready
                                     sync point ^
"""),
    fill("`isinstance(model, Predictor)` raises TypeError for a plain typing.Protocol. Decorating the protocol with `@typing.____` makes the check work.", "runtime_checkable",
         "The decorator name says when the check can happen.",
         "Protocols are for static type checkers; @runtime_checkable adds an isinstance check. It only tests that the methods exist, not their signatures, "
         "so an object with predict(self) passes a protocol that declares predict(self, x). Treat it as a duck-typing hint, not full validation.",
         topic="type-checks", level=4),
    mcq("Why shouldn't an API handler validate user input with `assert payload['k'] > 0`?",
        ["Asserts are removed when Python runs with -O, so the check silently disappears in that deployment",
         "assert can only compare strings",
         "assert always raises, even when the condition is True",
         "assert returns False instead of raising, which the handler ignores"], 0,
        "What does the -O flag do?",
        "`python -O` sets __debug__ to False and strips every assert statement, so the guard never runs. Use an explicit `if not ...: raise ValueError(...)` "
        "(or HTTP 400) for input checks, and keep assert for internal invariants that should never fail, such as tensor shapes in your own code.",
        topic="if-structure", level=4,
        analogy="Like validation that only exists in the dev build: production traffic goes straight past it."),

    # ---- round 3 pass 5: conceptual mcq/tf/fill
    mcq("Which operator means 'less than or equal to'?",
        ["<=", "=<", "<==", "<>"], 0,
        "Say it out loud: 'less than, or equal'.",
        "Python writes the symbols in the order you say them: `<=` and `>=`. `=<` is a SyntaxError, and `<>` was Python 2's old spelling of `!=`, "
        "removed in Python 3. You'll meet `<=` in checks such as `if epoch <= warmup_epochs:`.",
        topic="comparisons", level=1),
    tf("An `if` condition doesn't have to be True or False: Python also accepts a number, a string or a list and decides by whether it is truthy.", True,
       "What does `if` do with the value you give it?",
       "`if` calls bool() on whatever it gets. 0, '', [], {} and None count as False; most other values count as True. "
       "That's why `if losses:` is the normal way to ask 'did we record any losses yet?'. No cast or `.length` check is needed.",
       topic="truthiness", level=1,
       analogy="Like JavaScript's `if (value)` habit, with one twist: in JS an empty array `[]` is truthy, in Python an empty list is falsy."),
    mcq("A pixel value `x` must be rejected if it is outside 0..255. Which condition is True for the bad values?",
        ["x < 0 or x > 255", "x < 0 and x > 255", "0 <= x <= 255", "not x < 0 or x > 255"], 0,
        "Can one number be below 0 and above 255 at the same time?",
        "A bad value is too small OR too big. With `and`, both would have to hold at once, which no number can do, so nothing is ever rejected. "
        "`0 <= x <= 255` is the opposite test: it is True for the good values. The last option reads as `(not x < 0) or x > 255`, which is True for every x from 0 up.",
        topic="logic-ops", level=1,
        diagram="""
   bad    |        good         |    bad
 <--------0=====================255-------->
  x < 0      0 <= x <= 255          x > 255
"""),
    fill("A block can't be empty. To leave an `if` block with nothing in it for now, write the keyword ____ inside it.", "pass",
         "It tells Python 'nothing to do here, move on'.",
         "`if debug:` followed by an indented `pass` is valid; a block with nothing in it is an IndentationError. A comment alone doesn't count, "
         "because comments aren't statements. Handy while sketching code, e.g. a TODO branch in a training loop.",
         topic="if-structure", level=1),
    fill("In a `match command:` statement, each pattern to try starts with the keyword ____.", "case",
         "It's the same word a C or JS switch uses for its branches.",
         "`match` names the value and each `case` gives a pattern. Python tries them top to bottom and runs only the first one that matches, "
         "so there is no `break` to forget like in a C or JS switch.",
         topic="match-case", level=1),
    tf("`a == b` asks whether two values are equal, while `a is b` asks whether both names refer to the very same object.", True,
       "Two separate lists can hold the same numbers.",
       "Two separate lists [1, 2] are equal (`==` is True) but are two objects (`is` is False). Use `==` for values and `is` mainly for None. "
       "Mixing them up gives bugs that appear only for some values, because CPython happens to share small ints and short strings.",
       topic="identity", level=1,
       diagram="""
 a --> [1, 2]        a == b  -> True   same contents
 b --> [1, 2]        a is b  -> False  two objects

 c --> [1, 2] <-- d  c is d  -> True   one object
"""),
    mcq("`all(acc > 0.7 for acc in fold_accs)` is True when...",
        ["every fold's accuracy is above 0.7",
         "at least one fold's accuracy is above 0.7",
         "the average accuracy is above 0.7",
         "the last fold's accuracy is above 0.7"], 0,
        "all = no exceptions allowed.",
        "all() is True only if every item passes; any() needs just one. Neither looks at the average: folds of 0.95 and 0.6 average 0.775 "
        "but fail this all() check. That's a stricter bar for a cross-validated model, which catches one fold that went badly.",
        topic="any-all", level=1),
    mcq("`a < b > c` is valid Python. What does it test?",
        ["a < b and b > c", "(a < b) > c", "a < c", "Nothing: it's a SyntaxError"], 0,
        "A chain always splits into neighbouring pairs.",
        "Any chain `a op1 b op2 c` means `a op1 b and b op2 c`, with b evaluated only once. So `a < b > c` says b is bigger than both, and says "
        "nothing about a versus c. `(a < b) > c` would compare a bool with c. It's legal but confusing; reviewers prefer `b > max(a, c)`.",
        topic="comparisons", level=2,
        diagram="""
  a  <  b  >  c
  \\____/ \\____/
  a < b  and  b > c      (b evaluated once)
"""),
    tf("`if x:` and `if x is not None:` behave the same for every value of `x`.", False,
       "Try x = 0 or x = ''.",
       "`if x:` also skips 0, 0.0, '', [] and {}. When 0 is a real answer (an index, a dropout of 0.0, a count of 0 errors), `if x:` treats it as missing. "
       "Use `is not None` when None means 'no value' and the falsy values are valid.",
       topic="truthiness", level=2),
    mcq("Which expression always gives exactly True or False, whatever kind of values `x` and `y` hold?",
        ["not x", "x or y", "x and y", "x or False"], 0,
        "Two of the operators hand back one of their operands.",
        "`not` always returns a bool. `and` / `or` return one of their operands: `'' or 'n/a'` is 'n/a', and `x or False` gives x itself when x is truthy, "
        "e.g. a list. When you need a real bool, such as a JSON flag or a metrics field, wrap it: bool(x or y).",
        topic="logic-ops", level=2),
    fill("To add an extra condition to a case, write `case [x, y] ____ x == y:`.", "if",
         "It's the same keyword you'd use in a comprehension filter.",
         "This is a guard: the pattern must match first (binding x and y), then the condition must be truthy, or Python moves on to the next case. "
         "Guards check things pattern syntax can't express, such as `case {'loss': l} if l > 10:`.",
         topic="match-case", level=2),
    tf("`if loss < best: best = loss` written on a single line is valid Python.", True,
       "Can one simple statement sit right after the colon?",
       "A block made of simple statements can follow the colon on the same line. It's legal, but PEP 8 discourages it because the branch is easy to miss "
       "when reading and in diffs. A nested compound statement can't go there: `if a: if b: pass` is a SyntaxError.",
       topic="if-structure", level=2),
    mcq("A helper should accept any real number, but `isinstance(x, float)` rejects `3`. Why, and what's a fix?",
        ["int is not a subclass of float; check isinstance(x, (int, float)) or numbers.Real",
         "3 is converted to the string '3' before the check",
         "isinstance only works with classes you wrote yourself",
         "float checks must use type(x) == float instead"], 0,
        "Is int a kind of float in Python's class tree?",
        "int and float are separate types, so isinstance(3, float) is False even though 3 == 3.0. Accept both with a tuple, or use numbers.Real, "
        "which NumPy's scalar types also pass. Watch out: bool is a subclass of int, so True passes both checks.",
        topic="type-checks", level=2),
    mcq("A 3-class model outputs probs = [0.40, 0.35, 0.25]. Why is checking `p > 0.5` for each class the wrong way to pick the label?",
        ["The probabilities share a total of 1, so no class may pass 0.5; pick the largest one (argmax)",
         "A 0.5 threshold only works on integer outputs",
         "The probabilities must be sorted first",
         "Python can't compare a float with 0.5 exactly"], 0,
        "What happens when the winner has only 40%?",
        "With softmax over 3+ classes, the top class can sit well under 0.5, and then no label gets chosen. For one label per sample use argmax "
        "(np.argmax(probs)). Per-class thresholds are right for multi-label problems, where each class has its own sigmoid score.",
        topic="ml-patterns", level=2,
        diagram="""
 class :   0      1      2
 prob  :  0.40   0.35   0.25    (sums to 1)
 > 0.5?    no     no     no     -> no label at all
 argmax :  ^ class 0
"""),
    mcq("Which is the same as `not any(x < 0 for x in xs)`?",
        ["all(x >= 0 for x in xs)", "all(x < 0 for x in xs)", "any(x >= 0 for x in xs)", "not all(x < 0 for x in xs)"], 0,
        "'Not one of them is negative' means...",
        "'Not any negative' is 'all non-negative': De Morgan's law for any/all. Both forms are True for an empty list too. "
        "`any(x >= 0 ...)` only needs one non-negative value, so [-1, 5] would wrongly pass it.",
        topic="any-all", level=2),
    mcq("Which of these raises TypeError?",
        ["{'a': 1} < {'a': 2}", "[1, 2] < [1, 3]", "(1, 'x') < (2, 'a')", "{1} < {1, 2}"], 0,
        "One built-in container has no ordering at all.",
        "Dicts support == but not <, so ordering them raises TypeError; sort a list of dicts with key=. Lists and tuples compare item by item and stop at the "
        "first difference, so 'x' vs 'a' is never reached. For sets, < means 'proper subset', so {1} < {1, 2} is True, a surprise of its own.",
        topic="comparisons", level=3),
    tf("An object of a class that defines neither `__bool__` nor `__len__` is always truthy.", True,
       "What can Python fall back on when neither method exists?",
       "With no __bool__ and no __len__, Python treats every instance as True. So a custom Result whose `.ok` is False still passes `if result:`, "
       "and an 'empty' dataset wrapper passes `if dataset:`. Define __len__ (or __bool__) if truthiness should mean something.",
       topic="truthiness", level=3),
    mcq("Python has no `xor` keyword. Which test is True when exactly one of the bool flags `use_gpu` and `use_tpu` is set?",
        ["use_gpu != use_tpu", "use_gpu or use_tpu", "use_gpu and not use_tpu", "not (use_gpu and use_tpu)"], 0,
        "When are two bools different?",
        "For two bools, != is exclusive or: True only when they differ (`^` also works on bools). `or` also accepts both set, and `not (a and b)` also accepts "
        "neither set. If the values may not be real bools, such as a device string or None, compare bool(a) != bool(b): 'cuda' != 'tpu' is True even with both set.",
        topic="logic-ops", level=3),
    tf("Two different objects can report the same `id()` value during one program run.", True,
       "What happens to an object's memory once it's freed?",
       "id() is unique only among objects alive at the same time. In CPython it's the memory address, so once an object is freed a new one can reuse the slot. "
       "A cache keyed on id(batch) can therefore return stale results for a brand-new batch. Keep a reference alive or use a real key.",
       topic="identity", level=3),
    mcq("Which value does `case [first, *rest]:` NOT match?",
        ['"ab" (a str)', "(1, 2) (a tuple)", "range(3)", "[1] (a one-item list)"], 0,
        "Sequence patterns make one deliberate exception.",
        "Sequence patterns match any Sequence (list, tuple, range...) except str, bytes and bytearray, which are left out on purpose so a string isn't "
        "split into characters. [1] matches with rest = []. Iterators and generators don't match either, since matching must not consume them.",
        topic="match-case", level=3),
    mcq("This prints True instead of 4. Why, and what's the fix?",
        ["`:=` binds more loosely than `>`, so n = (len(data) > 3); write `(n := len(data)) > 3`",
         "The walrus always stores a bool when used in an if",
         "len() returns True for a non-empty list",
         "print converts 4 to True inside an if block"], 0,
        "Which runs first: the comparison or the assignment?",
        "The walrus has almost the lowest precedence, so the comparison runs first and n gets its result. Bracket the assignment. "
        "The same trap hits reading loops: `while chunk := f.read(n) != b''` stores a bool in chunk, not the bytes.",
        code="data = [1, 2, 3, 4]\nif n := len(data) > 3:\n    print(n)",
        topic="precedence", level=3),
    mcq("A fraud model flags a payment when `p >= threshold`. Raising the threshold from 0.5 to 0.8 usually...",
        ["raises precision and lowers recall: fewer flags, but more of them are real fraud",
         "raises both precision and recall",
         "lowers precision and raises recall",
         "changes nothing, because the model's weights are the same"], 0,
        "A higher bar lets fewer payments through to the 'flagged' side.",
        "Only the payments the model is surest about stay above 0.8, so a flag is more often right (precision up), but more real fraud slips under the bar "
        "(recall down). Pick the threshold on a validation set from the cost of each kind of error, not 0.5 by habit.",
        topic="ml-patterns", level=3,
        diagram="""
 0.0 ------------ 0.5 --------- 0.8 -------- 1.0
                   |<---- flagged at 0.5 ---->|
                                 |<- at 0.8 ->|
 higher threshold: fewer flags, more precise, more misses
"""),
    tf("If a class's `__len__` returns -1, `bool(obj)` raises ValueError instead of returning True.", True,
       "bool() falls back to __len__, and CPython checks what it gets back.",
       "With no __bool__, bool() uses __len__ and validates the result: a negative value raises ValueError ('__len__() should return >= 0'), and a float "
       "raises TypeError. A lazy dataset that returns -1 for 'unknown length' breaks both `if ds:` and len(ds); leave __len__ out for streams of unknown size.",
       topic="truthiness", level=4),
    tf("In Python 3.13, `if NotImplemented:` emits a DeprecationWarning.", True,
       "NotImplemented is meant to be returned, not tested.",
       "NotImplemented is the value __eq__ or __add__ return so Python tries the other operand. Testing it for truth is almost always a bug, e.g. a wrapper "
       "doing `if self.__eq__(other):`, which treated NotImplemented as True and called unrelated objects equal. It has warned since 3.9, and Python 3.14 makes it a TypeError.",
       topic="truthiness", level=4),
    mcq("`(lo < x) & (x < hi)` works on a NumPy array `x`, but `lo < x < hi` raises ValueError. Why?",
        ["A chain means `lo < x and x < hi`, and `and` calls bool() on the element-wise array from `lo < x`",
         "NumPy doesn't support < between an array and a scalar",
         "Chained comparisons are only allowed between ints",
         "The two comparisons broadcast to different shapes"], 0,
        "Rewrite the chain the way Python does.",
        "A chained comparison is sugar for `and`, which needs one truth value, so it calls bool() on a boolean array: 'truth value of an array ... is ambiguous'. "
        "Element-wise logic uses `&` with brackets, or np.logical_and. In pandas the same fix applies: df[(df.a > 0) & (df.a < 5)], or df.a.between(0, 5).",
        topic="comparisons", level=4,
        diagram="""
 lo < x < hi
   == (lo < x) and (x < hi)
          |
          v   bool(array([True, False, ...]))  -> ValueError
 fix: (lo < x) & (x < hi)    element-wise, no bool()
"""),
    mcq("In CPython 3.13, how does a `match` with many literal cases (`case 1:`, `case 2:`, ... `case 200:`) find the right branch?",
        ["It tests the cases one by one, top to bottom, like an if/elif chain",
         "It compiles to a jump table, so every lookup is O(1)",
         "It hashes the value and looks it up in a dict built at compile time",
         "It sorts the cases and binary-searches them"], 0,
        "Disassemble it with dis and count the comparisons.",
        "The bytecode is one compare-and-jump per case, so a value that matches case 200 costs 200 comparisons. match is built for taking structure apart, "
        "not for speed. For a large value-to-handler table, a dict lookup is O(1) and keeps the mapping as data.",
        topic="match-case", level=4,
        analogy="A C or Java switch over dense ints often becomes a jump table; Python's match is closer to a long chain of `else if`."),
    mcq("An eval script checks `all(p == y for p, y in zip(preds, labels))` and reports a perfect score. What's the hidden bug?",
        ["zip stops at the shorter list, so missing predictions are never compared; use zip(..., strict=True) or check the lengths",
         "all() only returns True for lists of bools",
         "== between ints is unreliable inside a generator",
         "The generator is used up before all() starts"], 0,
        "What if preds has 900 items and labels has 1,000?",
        "zip silently drops the 100 labels with no prediction, and all() still says True. zip(..., strict=True) (3.10+) raises ValueError on a length mismatch, "
        "and for two lists `preds == labels` checks the length too. all() of an empty zip is also True, so a model that produced nothing would 'pass'.",
        topic="any-all", level=4,
        analogy="Like a test that loops over the items in an API response: an empty or truncated response passes every assertion."),
    fill("Define `__eq__` and `__lt__`, then decorate the class with `@functools.____` to get `<=`, `>` and `>=` for free.", "total_ordering",
         "The decorator's name promises a full ordering.",
         "total_ordering derives the missing rich comparisons from one of __lt__/__le__/__gt__/__ge__ plus __eq__. The derived methods are slower, "
         "since each adds extra Python calls, so for a hot sort define them all or sort with key=. @dataclass(order=True) is another route: it compares fields as a tuple.",
         topic="comparisons", level=4),
    mcq("Inside a model's forward(), why write 'zero out negative scores' as `torch.where(x > 0, x, 0)` instead of `if x > 0:`?",
        ["`if` needs one Python bool, so on a batch it raises (or forces a sync and a graph break), while torch.where applies the rule to every element in one op",
         "torch.where is only shorter; both behave the same",
         "`if` statements are not allowed inside an nn.Module",
         "torch.where runs the condition on the CPU, which is faster"], 0,
        "What is the truth value of a tensor with 64 elements?",
        "`if tensor:` on more than one element raises RuntimeError. On a one-element GPU tensor it forces the CPU to wait for the GPU, and under torch.compile "
        "a data-dependent `if` splits the graph. A mask keeps the whole batch on the device in one vectorised kernel and works for any batch size.",
        topic="ml-patterns", level=4),
    mcq("On Windows, a training script that builds a DataLoader with num_workers=4 at module level crashes with a RuntimeError about the bootstrapping phase. What's the fix?",
        ["Put the training code under `if __name__ == '__main__':`, because each spawned worker re-imports the main script",
         "Set num_workers to a negative number",
         "Wrap the DataLoader in try/except RuntimeError",
         "Move the imports below the DataLoader"], 0,
        "How does a spawned worker get your functions and classes?",
        "Windows (and macOS by default) starts workers with spawn: each one imports your script fresh, under the name '__mp_main__'. Without the guard that import "
        "runs the training code again and tries to start more workers, which multiprocessing stops with this error. The guard runs the block only in the real program.",
        topic="if-structure", level=4,
        analogy="Python's version of Node's `if (require.main === module)`: top-level code should not run just because the file was imported.",
        diagram="""
 python train.py      __name__ == '__main__'    -> train()
   |-- worker 1: import train   '__mp_main__'   -> skip
   |-- worker 2: import train   '__mp_main__'   -> skip
 no guard: every worker calls train() -> RuntimeError
"""),
]
