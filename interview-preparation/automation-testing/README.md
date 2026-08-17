# Automation testing interview preparation

**📱 Open it in a browser: https://ravirajladha.github.io/applied-ai-ml-portfolio/interview-preparation/automation-testing/**
— works on phone and desktop, no install, nothing to run.

250 interview questions with model answers, explanations, code and diagrams, for a **4–6 year
experience** SDET / Automation Engineer profile — written so each answer can be *spoken*, not just read.
It starts from the basics, so it also works if you are new to automation and building up.

## The stack it covers

Manual testing and QA process · Java · Selenium WebDriver · TestNG · Maven · Git · Jenkins · Docker ·
Cucumber · RestAssured · Playwright with TypeScript · Appium · JMeter · OWASP · SQL

## Read it by category

Each category is a standalone page with its own search and quiz mode. Start anywhere.

| # | Category | Questions | What's in it |
|---|----------|-----------|--------------|
| 1 | [Manual Testing & QA Fundamentals](categories/01-manual-testing-qa-fundamentals.html) | Q1–Q41 | Test design techniques, STLC, defect life cycle, severity vs priority, Agile, risk-based testing |
| 2 | [Java Essentials for Automation](categories/02-java-for-automation.html) | Q42–Q65 | OOP, collections, exceptions, Java 8 streams, generics, ThreadLocal, coding-round questions |
| 3 | [Selenium WebDriver with Java](categories/03-selenium-webdriver.html) | Q66–Q115 | Architecture, locators, waits, frames, windows, Actions, JS executor, Grid, CDP, flakiness |
| 4 | [TestNG, Framework, Maven, Git & CI/CD](categories/04-testng-framework-maven-cicd.html) | Q116–Q150 | Annotations, data providers, listeners, Page Object Model, design patterns, Jenkins, Docker, BDD |
| 5 | [Playwright with TypeScript / JS](categories/05-playwright-typescript.html) | Q151–Q190 | Auto-waiting, locators, fixtures, tracing, network mocking, parallelism, migration from Selenium |
| 6 | [API, Database, Scenario & Behavioural](categories/06-api-database-behavioural.html) | Q191–Q200 | HTTP methods and status codes, auth, SQL for testers, and the questions that decide offers |
| 7 | [Appium & Mobile Automation](categories/07-appium-mobile.html) | Q201–Q215 | Appium 2 architecture, mobile locators, gestures, context switching, ADB, device strategy |
| 8 | [Performance, Security & Non-Functional](categories/08-performance-security-nonfunctional.html) | Q216–Q230 | JMeter, load test design, bottleneck analysis, OWASP Top 10, accessibility, contract testing |
| 9 | [Practical Coding Exercises](categories/09-practical-coding-exercises.html) | Q231–Q250 | Twenty write-the-code tasks with full solutions, for the live-coding round |

Or read [index.html](index.html) for all 250 in one page, plus the cheat sheets and the
"questions you should ask the interviewer" section.

## Files

| File | What it is |
|------|------------|
| [index.html](index.html) | The full guide — all 250 questions, 14 diagrams, cheat sheets, study plan. Best opened via the link above |
| `categories/` | One standalone page per category, generated from `index.html` |
| `Automation-Interview-Prep.pdf` | The whole guide as a PDF, for offline reading and printing |
| `build-categories.js` | Regenerates `categories/` from `index.html` so the two can never drift apart |

## How to use it

- **Study mode** (default) — answers are open. Read a category end to end, out loud.
- **Quiz mode** — collapses every answer. Read the question, *say your answer aloud in 60–90 seconds*,
  then click to reveal. Speaking is the skill being tested; reading is not.
- **Search** — press <kbd>/</kbd> and type a keyword (`StaleElement`, `fixture`, `severity`) to filter instantly.
- **PDF** — the *Print / PDF* button expands every answer and prints cleanly, or use the PDF in this folder.
- Tags mark each question: **core** (know it cold), **advanced** (senior differentiator),
  **trap** (commonly answered wrong).

## Two things that matter more than the question list

- **Anchor every technical answer in a project.** Add one sentence of *"on my project we…"* to each one.
  Interviewers grade experience, not definitions — a textbook-perfect answer with no project story scores
  lower than an average answer anchored in real work.
- **Rehearse two answers until they need no thinking**: your 3-minute introduction (Q194) and your
  framework walkthrough (Q132). Most interviews are decided in those five minutes, and every later
  question is drawn from what you said there.

## Regenerating the category pages

The category pages are generated, not hand-written. Edit `index.html`, then:

```bash
node build-categories.js
```

It re-splits the master file, reuses its stylesheet and script verbatim, and fails the build if the
question count is not 250.
