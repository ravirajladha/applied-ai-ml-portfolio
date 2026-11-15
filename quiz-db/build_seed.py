"""Validate the quiz content and write seed.sql.

Content sources:
  content/structure.py          categories, sections, subjects
  content/q_python.py, q_ml.py  first starter questions (no topics)
  content/subjects/<slug>.py    deep question banks: SUBJECT, TOPICS, QUESTIONS

Usage:
    python build_seed.py            # validates, writes seed.sql
    mysql -u root < schema.sql && mysql -u root --default-character-set=utf8mb4 aiml_quiz < seed.sql
"""
import hashlib
import importlib.util
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "content"))

from structure import CATEGORIES, SECTIONS, SUBJECTS  # noqa: E402
import q_python  # noqa: E402
import q_ml  # noqa: E402

SUBJECT_DIR = HERE / "content" / "subjects"
SPEC_DIR = HERE / "specs"


def sql(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace("'", "''").replace("\n", "\\n")
    return f"'{s}'"


def load_subject_file(path):
    spec = importlib.util.spec_from_file_location(f"subj_{path.stem.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_all():
    """Return (questions_by_subject, topics_by_subject)."""
    questions, topics = {}, {}
    for qs in (q_python.QUESTIONS, q_ml.QUESTIONS):
        for slug, items in qs.items():
            questions.setdefault(slug, []).extend(items)
    for path in sorted(SUBJECT_DIR.glob("*.py")):
        mod = load_subject_file(path)
        if mod.SUBJECT != path.stem:
            raise SystemExit(f"{path.name}: SUBJECT = {mod.SUBJECT!r} must match the file name")
        topics[mod.SUBJECT] = list(mod.TOPICS)
        questions.setdefault(mod.SUBJECT, []).extend(mod.QUESTIONS)
    return questions, topics


def validate_questions(slug, qs, topic_slugs):
    errors = []
    seen = set()
    for q in qs:
        tag = f"{slug}: {q['question'][:50]!r}"
        key = (q["question"], q["code"])
        if key in seen:
            errors.append(f"{tag}: duplicate question")
        seen.add(key)
        if q["level"] not in (1, 2, 3, 4):
            errors.append(f"{tag}: level must be 1-4")
        if topic_slugs is not None and q["topic"] not in topic_slugs:
            errors.append(f"{tag}: unknown topic {q['topic']!r}")
        if q["qtype"] in ("mcq", "code_output", "true_false"):
            opts = q["options"]
            if len(opts) < 2 or len(set(opts)) != len(opts):
                errors.append(f"{tag}: options missing or duplicated")
            if q["qtype"] != "true_false" and len(opts) != 4:
                errors.append(f"{tag}: expected 4 options")
            if any(len(o) > 500 for o in opts):
                errors.append(f"{tag}: option longer than 500 chars")
        if q["qtype"] == "code_output" and not q["code"]:
            errors.append(f"{tag}: code_output without code")
        if len(q["answer"]) > 500:
            errors.append(f"{tag}: answer longer than 500 chars")
        if not q["hint"] or not q["explanation"]:
            errors.append(f"{tag}: missing hint/explanation")
    return errors


def validate(questions, topics):
    errors = []
    cat_slugs = {c[0] for c in CATEGORIES}
    sec_slugs = {s[0] for s in SECTIONS}
    sub_slugs = {s[0] for s in SUBJECTS}
    for s in SECTIONS:
        if s[1] not in cat_slugs:
            errors.append(f"section {s[0]}: unknown category {s[1]}")
    for s in SUBJECTS:
        if s[1] not in sec_slugs:
            errors.append(f"subject {s[0]}: unknown section {s[1]}")
        if s[4] == "ready" and not questions.get(s[0]):
            errors.append(f"subject {s[0]} is 'ready' but has no questions")
        if s[4] == "planned" and questions.get(s[0]):
            errors.append(f"subject {s[0]} is 'planned' but has questions")
    for slug, qs in questions.items():
        if slug not in sub_slugs:
            errors.append(f"questions for unknown subject {slug}")
        tslugs = {t[0] for t in topics[slug]} if slug in topics else None
        # starter questions (q_python / q_ml) have topic=None, allow that
        if tslugs is not None:
            tslugs = tslugs | {None}
        errors += validate_questions(slug, qs, tslugs)
    for slug, ts in topics.items():
        if len({t[0] for t in ts}) != len(ts):
            errors.append(f"{slug}: duplicate topic slugs")
    return errors


def shuffled(q):
    """Shuffle options deterministically so the right answer isn't always A."""
    opts = list(enumerate(q["options"]))
    if q["qtype"] != "true_false":
        seed = int(hashlib.md5(q["question"].encode() + (q["code"] or "").encode()).hexdigest(), 16)
        random.Random(seed).shuffle(opts)
    return [(chr(65 + i), text, orig == q["correct"]) for i, (orig, text) in enumerate(opts)]


def main():
    questions, topics = load_all()
    errors = validate(questions, topics)
    if errors:
        print("Content errors:\n  " + "\n  ".join(errors[:200]))
        sys.exit(1)

    lines = ["-- Generated by build_seed.py. Edit content/*.py, not this file.",
             "USE aiml_quiz;", "SET NAMES utf8mb4;", "START TRANSACTION;", ""]

    for i, (slug, name, level, desc) in enumerate(CATEGORIES):
        lines.append(f"INSERT INTO categories (slug, name, ladder_level, description, sort_order) "
                     f"VALUES ({sql(slug)}, {sql(name)}, {level}, {sql(desc)}, {i + 1});")
    lines.append("")
    for i, (slug, cat, name, desc) in enumerate(SECTIONS):
        lines.append(f"INSERT INTO sections (category_id, slug, name, description, sort_order) "
                     f"SELECT id, {sql(slug)}, {sql(name)}, {sql(desc)}, {i + 1} FROM categories WHERE slug = {sql(cat)};")
    lines.append("")
    for i, (slug, sec, name, desc, status) in enumerate(SUBJECTS):
        lines.append(f"INSERT INTO subjects (section_id, slug, name, description, status, sort_order) "
                     f"SELECT id, {sql(slug)}, {sql(name)}, {sql(desc)}, {sql(status)}, {i + 1} FROM sections WHERE slug = {sql(sec)};")
    lines.append("")
    for slug, ts in topics.items():
        for i, (tslug, tname) in enumerate(ts, 1):
            lines.append(f"INSERT INTO topics (subject_id, slug, name, sort_order) "
                         f"SELECT id, {sql(tslug)}, {sql(tname)}, {i} FROM subjects WHERE slug = {sql(slug)};")

    total = 0
    for slug, qs in questions.items():
        lines += ["", f"-- {slug}", f"SET @s = (SELECT id FROM subjects WHERE slug = {sql(slug)});"]
        for order, q in enumerate(qs, 1):
            total += 1
            topic = (f"(SELECT id FROM topics WHERE subject_id = @s AND slug = {sql(q['topic'])})"
                     if q["topic"] else "NULL")
            lines.append(
                "INSERT INTO questions (subject_id, topic_id, level, qtype, question, code_snippet, code_language, "
                "answer, hint, explanation, diagram, analogy, sort_order) VALUES "
                f"(@s, {topic}, {q['level']}, {sql(q['qtype'])}, {sql(q['question'])}, {sql(q['code'])}, "
                f"{sql(q['lang'])}, {sql(q['answer'])}, {sql(q['hint'])}, {sql(q['explanation'])}, "
                f"{sql(q['diagram'])}, {sql(q['analogy'])}, {order});")
            if q["options"]:
                lines.append("SET @q = LAST_INSERT_ID();")
                vals = ", ".join(f"(@q, '{lab}', {sql(t)}, {1 if ok else 0})" for lab, t, ok in shuffled(q))
                lines.append(f"INSERT INTO question_options (question_id, label, option_text, is_correct) VALUES {vals};")

    lines += ["", "INSERT INTO students (name) VALUES ('Ravi');", "", "COMMIT;", ""]
    (HERE / "seed.sql").write_text("\n".join(lines), encoding="utf-8")
    print(f"seed.sql written: {len(CATEGORIES)} categories, {len(SECTIONS)} sections, "
          f"{len(SUBJECTS)} subjects, {sum(len(t) for t in topics.values())} topics, {total} questions")


if __name__ == "__main__":
    main()
