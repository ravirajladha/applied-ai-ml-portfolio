-- AI/ML Ladder Quiz: database schema
-- Hierarchy: category (ladder rung) -> section -> subject -> question -> options
-- Tracking:  student -> quiz_attempt -> attempt_answer, plus per-question mastery stats

DROP DATABASE IF EXISTS aiml_quiz;
CREATE DATABASE aiml_quiz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aiml_quiz;

-- ---------- Content ----------

CREATE TABLE levels (
  id          TINYINT PRIMARY KEY,
  slug        VARCHAR(20) NOT NULL UNIQUE,
  name        VARCHAR(40) NOT NULL,
  description VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

INSERT INTO levels VALUES
 (1, 'amateur',      'Amateur',      'First contact: what it is, read and run simple code'),
 (2, 'intermediate', 'Intermediate', 'Uses it day to day: combines ideas, predicts output, avoids common traps'),
 (3, 'advanced',     'Advanced',     'Knows the edge cases, performance and the why behind the behaviour'),
 (4, 'expert',       'Expert',       'Internals, design trade-offs, debugging subtle bugs, interview-grade depth');

CREATE TABLE categories (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  slug         VARCHAR(60)  NOT NULL UNIQUE,
  name         VARCHAR(120) NOT NULL,
  ladder_level TINYINT      NOT NULL COMMENT '0 = prerequisites, 1..5 = ladder rungs',
  description  TEXT,
  sort_order   INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE sections (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  category_id INT NOT NULL,
  slug        VARCHAR(60)  NOT NULL UNIQUE,
  name        VARCHAR(120) NOT NULL,
  description TEXT,
  sort_order  INT NOT NULL DEFAULT 0,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE subjects (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  section_id  INT NOT NULL,
  slug        VARCHAR(60)  NOT NULL UNIQUE,
  name        VARCHAR(120) NOT NULL,
  description TEXT,
  status      ENUM('ready','planned') NOT NULL DEFAULT 'ready' COMMENT 'planned = no questions yet',
  sort_order  INT NOT NULL DEFAULT 0,
  FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Topics inside a subject (from the subject's spec in specs/<subject>.md)
CREATE TABLE topics (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  subject_id INT NOT NULL,
  slug       VARCHAR(60)  NOT NULL,
  name       VARCHAR(150) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
  UNIQUE KEY uq_subject_topic (subject_id, slug)
) ENGINE=InnoDB;

CREATE TABLE questions (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  subject_id    INT NOT NULL,
  topic_id      INT NULL,
  level         TINYINT NOT NULL DEFAULT 1 COMMENT '1 amateur, 2 intermediate, 3 advanced, 4 expert',
  qtype         ENUM('mcq','true_false','code_output','fill_blank') NOT NULL,
  question      TEXT NOT NULL,
  code_snippet  TEXT NULL,
  code_language VARCHAR(20) NULL,
  answer        VARCHAR(500) NOT NULL COMMENT 'short correct answer (for fill_blank, the accepted text)',
  hint          TEXT NOT NULL,
  explanation   TEXT NOT NULL COMMENT 'quick answer: why it is right, 1-3 lines',
  diagram       TEXT NULL COMMENT 'ASCII diagram, render in <pre>',
  analogy       TEXT NULL COMMENT 'real-world / SDE analogy',
  sort_order    INT NOT NULL DEFAULT 0,
  is_active     TINYINT(1) NOT NULL DEFAULT 1,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
  FOREIGN KEY (topic_id)   REFERENCES topics(id)   ON DELETE SET NULL,
  FOREIGN KEY (level)      REFERENCES levels(id),
  INDEX idx_subject_level (subject_id, level, sort_order)
) ENGINE=InnoDB;

CREATE TABLE question_options (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  question_id INT NOT NULL,
  label       CHAR(1) NOT NULL COMMENT 'A, B, C, D',
  option_text VARCHAR(500) NOT NULL,
  is_correct  TINYINT(1) NOT NULL DEFAULT 0,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
  UNIQUE KEY uq_q_label (question_id, label)
) ENGINE=InnoDB;

-- ---------- Tracking ----------

CREATE TABLE students (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(120) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE quiz_attempts (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  student_id  INT NOT NULL,
  subject_id  INT NULL COMMENT 'NULL = mixed / review quiz',
  mode        ENUM('practice','review','test') NOT NULL DEFAULT 'practice',
  level_min   TINYINT NULL COMMENT 'level filter used for this quiz',
  level_max   TINYINT NULL,
  started_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at DATETIME NULL,
  total       INT NOT NULL DEFAULT 0,
  correct     INT NOT NULL DEFAULT 0,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE attempt_answers (
  id                 INT AUTO_INCREMENT PRIMARY KEY,
  attempt_id         INT NOT NULL,
  question_id        INT NOT NULL,
  selected_option_id INT NULL,
  answer_text        VARCHAR(255) NULL COMMENT 'for fill_blank',
  is_correct         TINYINT(1) NOT NULL,
  used_hint          TINYINT(1) NOT NULL DEFAULT 0,
  time_taken_ms      INT NULL,
  answered_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (attempt_id)  REFERENCES quiz_attempts(id) ON DELETE CASCADE,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
  FOREIGN KEY (selected_option_id) REFERENCES question_options(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Leitner box spaced repetition: box 1 = see again soon ... box 5 = mastered
CREATE TABLE question_mastery (
  student_id    INT NOT NULL,
  question_id   INT NOT NULL,
  times_seen    INT NOT NULL DEFAULT 0,
  times_correct INT NOT NULL DEFAULT 0,
  streak        INT NOT NULL DEFAULT 0,
  box           TINYINT NOT NULL DEFAULT 1,
  last_seen_at  DATETIME NULL,
  next_due_at   DATETIME NULL,
  PRIMARY KEY (student_id, question_id),
  FOREIGN KEY (student_id)  REFERENCES students(id)  ON DELETE CASCADE,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Update mastery automatically whenever an answer is recorded
DELIMITER //
CREATE TRIGGER trg_answer_mastery AFTER INSERT ON attempt_answers
FOR EACH ROW
BEGIN
  DECLARE sid INT;
  SELECT student_id INTO sid FROM quiz_attempts WHERE id = NEW.attempt_id;

  INSERT INTO question_mastery (student_id, question_id, times_seen, times_correct, streak, box, last_seen_at, next_due_at)
  VALUES (sid, NEW.question_id, 1, NEW.is_correct, NEW.is_correct, IF(NEW.is_correct, 2, 1),
          NOW(), IF(NEW.is_correct, NOW() + INTERVAL 1 DAY, NOW()))
  ON DUPLICATE KEY UPDATE
    times_seen    = times_seen + 1,
    times_correct = times_correct + NEW.is_correct,
    streak        = IF(NEW.is_correct, streak + 1, 0),
    box           = IF(NEW.is_correct, LEAST(box + 1, 5), 1),
    last_seen_at  = NOW(),
    next_due_at   = IF(NEW.is_correct,
                       NOW() + INTERVAL ELT(LEAST(box, 5), 1, 3, 7, 14, 30) DAY,
                       NOW());

  UPDATE quiz_attempts
     SET total = total + 1, correct = correct + NEW.is_correct
   WHERE id = NEW.attempt_id;
END//
DELIMITER ;

-- ---------- Reporting views ----------

CREATE VIEW v_ladder AS
SELECT c.ladder_level, c.name AS category, s.name AS section, sub.name AS subject,
       sub.status, COUNT(q.id) AS questions
FROM categories c
JOIN sections s   ON s.category_id = c.id
JOIN subjects sub ON sub.section_id = s.id
LEFT JOIN questions q ON q.subject_id = sub.id AND q.is_active = 1
GROUP BY c.id, s.id, sub.id
ORDER BY c.sort_order, s.sort_order, sub.sort_order;

CREATE VIEW v_student_subject_progress AS
SELECT st.id AS student_id, st.name AS student, sub.id AS subject_id, sub.name AS subject,
       COUNT(DISTINCT q.id)                                  AS total_questions,
       COUNT(DISTINCT m.question_id)                         AS seen,
       SUM(CASE WHEN m.box >= 4 THEN 1 ELSE 0 END)           AS mastered,
       ROUND(100 * SUM(m.times_correct) / NULLIF(SUM(m.times_seen), 0), 1) AS accuracy_pct
FROM students st
CROSS JOIN subjects sub
JOIN questions q ON q.subject_id = sub.id AND q.is_active = 1
LEFT JOIN question_mastery m ON m.question_id = q.id AND m.student_id = st.id
GROUP BY st.id, sub.id;

CREATE VIEW v_due_for_review AS
SELECT m.student_id, q.id AS question_id, sub.name AS subject, q.question, m.box, m.next_due_at
FROM question_mastery m
JOIN questions q  ON q.id = m.question_id
JOIN subjects sub ON sub.id = q.subject_id
WHERE m.next_due_at <= NOW()
ORDER BY m.box, m.next_due_at;

-- Questions per subject x level (is the subject deep enough at every level?)
CREATE VIEW v_coverage AS
SELECT c.ladder_level, sub.slug AS subject, sub.name,
       SUM(q.level = 1) AS amateur, SUM(q.level = 2) AS intermediate,
       SUM(q.level = 3) AS advanced, SUM(q.level = 4) AS expert,
       COUNT(q.id) AS total
FROM subjects sub
JOIN sections s   ON s.id = sub.section_id
JOIN categories c ON c.id = s.category_id
LEFT JOIN questions q ON q.subject_id = sub.id AND q.is_active = 1
GROUP BY sub.id
ORDER BY c.sort_order, s.sort_order, sub.sort_order;

-- Per-student accuracy by subject and level (for "you're solid at intermediate, weak at advanced")
CREATE VIEW v_student_level_progress AS
SELECT st.id AS student_id, sub.name AS subject, l.name AS level,
       COUNT(DISTINCT q.id) AS questions, COUNT(DISTINCT m.question_id) AS seen,
       ROUND(100 * SUM(m.times_correct) / NULLIF(SUM(m.times_seen), 0), 1) AS accuracy_pct
FROM students st
CROSS JOIN questions q
JOIN subjects sub ON sub.id = q.subject_id
JOIN levels l     ON l.id = q.level
LEFT JOIN question_mastery m ON m.question_id = q.id AND m.student_id = st.id
WHERE q.is_active = 1
GROUP BY st.id, sub.id, l.id;
