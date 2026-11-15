"""Small builders (level=1..4: amateur, intermediate, advanced, expert; topic=<topic slug>) so each question is one readable call.

mcq(question, options, correct_index, hint, explanation, ...)
tf(statement, is_true, hint, explanation, ...)
out(code, options, correct_index, hint, explanation, ...)   # "What does this print?"
fill(question, answer, hint, explanation, ...)
"""


LEVELS = {1: "amateur", 2: "intermediate", 3: "advanced", 4: "expert"}


def _q(qtype, question, answer, hint, explanation, options=None, correct=None,
       code=None, lang=None, diagram=None, analogy=None, d=1, level=None, topic=None):
    return {
        "qtype": qtype, "question": question.strip(), "answer": answer,
        "hint": hint, "explanation": explanation, "options": options or [],
        "correct": correct, "code": code.strip("\n") if code else None,
        "lang": lang or ("python" if code else None),
        "diagram": diagram.strip("\n") if diagram else None,
        "analogy": analogy, "level": level or d, "topic": topic,
    }


def mcq(question, options, correct, hint, explanation, **kw):
    return _q("mcq", question, options[correct], hint, explanation, options, correct, **kw)


def tf(statement, is_true, hint, explanation, **kw):
    return _q("true_false", statement, "True" if is_true else "False", hint, explanation,
              ["True", "False"], 0 if is_true else 1, **kw)


def out(code, options, correct, hint, explanation, question="What does this print?", **kw):
    return _q("code_output", question, options[correct], hint, explanation, options, correct,
              code=code, **kw)


def fill(question, answer, hint, explanation, **kw):
    return _q("fill_blank", question, answer, hint, explanation, **kw)
