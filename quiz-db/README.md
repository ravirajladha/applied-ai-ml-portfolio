# AI/ML Ladder Quiz: database

A quiz question bank that climbs from basic Python up to shipping LLM apps, with tracking for each student. Only the database exists so far; the app comes later.

Every question has a **level**: 1 Amateur, 2 Intermediate, 3 Advanced, 4 Expert. Every deep subject has a **spec** (`specs/<subject>.md`) that lists its topics and what each level must know; the questions are tagged with those topics. See `STANDARD.md` for how specs and questions are written.

**Database:** `aiml_quiz` on local XAMPP MariaDB (open it in phpMyAdmin).

## Structure

```
categories (ladder rung L0..L5)
  └─ sections
       └─ subjects   (status: ready | planned)
            └─ topics     (from specs/<subject>.md)
            └─ questions  (level 1-4, topic, hint, explanation, diagram, analogy, code snippet)
                 └─ question_options (A-D, one is_correct)

students ─ quiz_attempts ─ attempt_answers
                 │  (trigger on each answer)
                 └─> question_mastery  (Leitner box 1-5, next_due_at)
```

Views: `v_ladder` (tree and question counts), `v_coverage` (questions per subject x level), `v_student_subject_progress`, `v_student_level_progress`, `v_due_for_review`.

### Example: a filtered quiz

```sql
-- 10 random intermediate-to-advanced NumPy questions
SELECT q.* FROM questions q JOIN subjects s ON s.id = q.subject_id
WHERE s.slug = 'np-operations' AND q.level BETWEEN 2 AND 3
ORDER BY RAND() LIMIT 10;
```

## Rebuild / add questions

1. Edit `content/subjects/<subject>.py` (one `mcq(...)`, `tf(...)`, `out(...)` or `fill(...)` call per question, with `topic=` and `level=`). The first starter questions live in `content/q_python.py` / `content/q_ml.py`. New subjects go in `content/structure.py` plus a spec in `specs/`.
2. `C:/ProgramData/anaconda3/python.exe check_subject.py <subject>` checks the structure and the level minimums, and runs every code snippet to confirm its answer.
3. `C:/ProgramData/anaconda3/python.exe build_seed.py` validates everything and writes `seed.sql`.
4. Reload everything (this **wipes** tracking data):
   ```
   mysql -u root < schema.sql
   mysql -u root --default-character-set=utf8mb4 aiml_quiz < seed.sql
   ```
   Or import `schema.sql` and then `seed.sql` in phpMyAdmin.

## Adding your own course material

Put the notes for a subject under its spec's **Source material** section (or send them over). New questions from them go into the same subject file, tagged with an existing topic or a new one added to both the spec and `TOPICS`.
