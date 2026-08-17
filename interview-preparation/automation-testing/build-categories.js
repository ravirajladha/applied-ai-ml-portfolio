/**
 * Splits the master interview guide into one self-contained page per category.
 *
 * Every generated page reuses the master's stylesheet and script verbatim, so the
 * category pages can never drift from the full guide — regenerate with:
 *     node build-categories.js
 */
const fs = require("fs");
const path = require("path");

const SRC = path.join(__dirname, "index.html");
const OUT_DIR = path.join(__dirname, "categories");

const html = fs.readFileSync(SRC, "utf8");

const STYLE = html.match(/<style>([\s\S]*?)<\/style>/)[1];
const SCRIPT = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];

// Pull every <section class="sec" id="..."> ... </section> block out of the master.
const sections = {};
const re = /<section class="sec" id="([a-z0-9]+)">([\s\S]*?)<\/section>/g;
let m;
while ((m = re.exec(html))) sections[m[1]] = m[0];

const CATEGORIES = [
  { id: "s1", file: "01-manual-testing-qa-fundamentals.html", title: "Manual Testing & QA Fundamentals", range: "Q1–Q41",    count: 41,
    blurb: "Test design techniques, STLC, defect life cycle, severity vs priority, Agile and risk-based testing." },
  { id: "s2", file: "02-java-for-automation.html",            title: "Java Essentials for Automation",   range: "Q42–Q65",   count: 24,
    blurb: "OOP, collections, exceptions, Java 8 streams, generics, ThreadLocal and coding-round questions." },
  { id: "s3", file: "03-selenium-webdriver.html",             title: "Selenium WebDriver with Java",      range: "Q66–Q115",  count: 50,
    blurb: "Architecture, locators, waits, frames, windows, Actions, JS executor, Grid, CDP and flakiness." },
  { id: "s4", file: "04-testng-framework-maven-cicd.html",    title: "TestNG, Framework, Maven, Git & CI/CD", range: "Q116–Q150", count: 35,
    blurb: "Annotations, data providers, listeners, Page Object Model, design patterns, Jenkins, Docker and BDD." },
  { id: "s5", file: "05-playwright-typescript.html",          title: "Playwright with TypeScript / JS",   range: "Q151–Q190", count: 40,
    blurb: "Architecture, auto-waiting, locators, fixtures, tracing, network mocking, parallelism and migration." },
  { id: "s6", file: "06-api-database-behavioural.html",       title: "API, Database, Scenario & Behavioural", range: "Q191–Q200", count: 10,
    blurb: "HTTP methods and status codes, auth, SQL for testers, and the behavioural questions that decide offers." },
  { id: "s7", file: "07-appium-mobile.html",                  title: "Appium & Mobile Automation",        range: "Q201–Q215", count: 15,
    blurb: "Appium 2 architecture, mobile locators, gestures, context switching, ADB and device strategy." },
  { id: "s8", file: "08-performance-security-nonfunctional.html", title: "Performance, Security & Non-Functional", range: "Q216–Q230", count: 15,
    blurb: "JMeter, load test design, bottleneck analysis, OWASP Top 10, accessibility, contract testing." },
  { id: "s9", file: "09-practical-coding-exercises.html",     title: "Practical Coding Exercises",        range: "Q231–Q250", count: 20,
    blurb: "Twenty write-the-code tasks with full solutions, for the live-coding round." },
];

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function page(cat, prev, next) {
  const nav = [
    prev ? `<a class="pn" href="${prev.file}">&#8592; ${esc(prev.title)}</a>` : `<span></span>`,
    next ? `<a class="pn" href="${next.file}">${esc(next.title)} &#8594;</a>` : `<span></span>`,
  ].join("\n      ");

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(cat.title)} — Automation Interview Prep (${cat.range})</title>
<meta name="description" content="${esc(cat.blurb)}">
<style>${STYLE}
.crumb{max-width:1400px;margin:0 auto;padding:14px 18px 0;font-size:13.5px;color:var(--muted)}
.crumb a{font-weight:600}
.pager{display:flex;justify-content:space-between;gap:12px;margin:34px 0 0;flex-wrap:wrap}
.pn{display:inline-block;padding:12px 16px;border:1px solid var(--line);border-radius:12px;
    background:var(--panel);font-weight:600;font-size:14px;box-shadow:var(--shadow)}
.pn:hover{border-color:var(--accent);text-decoration:none}
@media print{.crumb,.pager{display:none}}
</style>
</head>
<body>

<header class="top">
  <div class="top-in">
    <div class="brand"><span class="dot">QA</span><span>${esc(cat.title)}</span></div>
    <div class="tools">
      <input id="search" type="search" placeholder="Search this section…  (press /)" autocomplete="off">
      <span class="count" id="count"></span>
      <button class="btn" id="quiz" title="Hide all answers and test yourself">Quiz mode</button>
      <button class="btn" id="expand">Expand all</button>
      <button class="btn" id="theme" title="Toggle dark mode">Dark</button>
      <button class="btn" onclick="window.print()" title="Save as PDF">Print / PDF</button>
    </div>
  </div>
</header>

<div class="crumb"><a href="../index.html">&#8592; All 250 questions</a> &nbsp;·&nbsp; ${esc(cat.title)} &nbsp;·&nbsp; ${cat.range} (${cat.count} questions)</div>

<div class="wrap" style="grid-template-columns:1fr">
<main>
${sections[cat.id]}

  <nav class="pager">
      ${nav}
  </nav>
</main>
</div>

<button class="btn toTop noprint" onclick="scrollTo({top:0,behavior:'smooth'})" title="Back to top">&#8593; Top</button>

<script>${SCRIPT}</script>
</body>
</html>
`;
}

fs.mkdirSync(OUT_DIR, { recursive: true });
CATEGORIES.forEach((cat, i) => {
  const out = page(cat, CATEGORIES[i - 1], CATEGORIES[i + 1]);
  fs.writeFileSync(path.join(OUT_DIR, cat.file), out);
  const questions = (sections[cat.id].match(/class="num">Q\d+</g) || []).length;
  console.log(`${cat.file.padEnd(46)} ${questions} questions  ${(out.length / 1024).toFixed(0)} KB`);
});

const total = CATEGORIES.reduce((n, c) => n + (sections[c.id].match(/class="num">Q\d+</g) || []).length, 0);
console.log(`\n${CATEGORIES.length} category pages, ${total} questions total.`);
if (total !== 250) { console.error("!! expected 250 questions"); process.exit(1); }
