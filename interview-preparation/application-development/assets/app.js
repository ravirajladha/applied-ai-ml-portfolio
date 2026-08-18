/**
 * Shared behaviour for every page: offline syntax highlighting, search,
 * quiz mode, expand-all and the dark-mode toggle.
 *
 * No build step and no dependencies — open any page straight from disk.
 */
(function () {
  /* ---- tiny offline syntax highlighter (Python / TS / JS / C# / Java / SQL / YAML) ---- */
  var KW = {};
  ([
    // shared control flow
    "if else elif for while do switch case default break continue return yield try catch except finally raise throw throws with using match when goto pass",
    // declarations
    "class interface struct record enum def function func var let const final static public private protected internal abstract virtual override sealed readonly partial namespace package module import from export require extends implements inherits new delete this self base super lambda global nonlocal",
    // types
    "int long short byte float double decimal bool boolean char string str list dict set tuple array object any unknown never void null none nil true false True False None undefined var dynamic Task Promise Optional List Dict Map Set ArrayList HashMap IEnumerable IActionResult DateTime Guid",
    // async
    "async await asyncio Thread lock synchronized volatile Parallel goroutine",
    // python / fastapi / pandas
    "self def print len range enumerate zip map filter sorted open yield assert del is not and or in isinstance super property staticmethod classmethod dataclass pytest fixture FastAPI APIRouter Depends BaseModel pydantic pd np df Series DataFrame",
    // web / api
    "app router get post put patch delete route middleware request response req res next express fetch axios useState useEffect useMemo useCallback props component render return",
    // sql
    "SELECT FROM WHERE JOIN INNER LEFT RIGHT FULL OUTER ON GROUP BY ORDER HAVING LIMIT OFFSET INSERT INTO VALUES UPDATE SET DELETE CREATE TABLE ALTER DROP INDEX VIEW PRIMARY KEY FOREIGN REFERENCES UNIQUE NOT NULL DISTINCT COUNT SUM AVG MIN MAX CASE WHEN THEN END AS WITH UNION ALL EXISTS BEGIN COMMIT ROLLBACK TRANSACTION",
    // infra / azure
    "resource module output param targetScope apiVersion kind spec metadata containers image replicas kubectl az docker terraform"
  ].join(" ")).split(/\s+/).forEach(function (w) { if (w) KW[w] = 1; });

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function plain(txt) {
    return esc(txt).replace(/\b([A-Za-z_$][\w$]*)\b|\b(\d+(?:\.\d+)?)\b|(@[A-Za-z]\w*)/g,
      function (m, word, num, ann) {
        if (ann) return '<span class="f">' + ann + "</span>";
        if (num) return '<span class="n">' + num + "</span>";
        if (word && KW[word]) return '<span class="k">' + word + "</span>";
        return m;
      });
  }

  [].forEach.call(document.querySelectorAll("pre > code"), function (el) {
    var src = el.textContent, out = "", last = 0, m;
    // Comments or string literals. Both comment markers require trailing whitespace so
    // that code which merely starts with the same characters is left alone:
    //   "# note"  is a comment, "#4338ca" (a CSS colour) is not
    //   "-- note" is a comment, "--color-ink" and "--no-cache-dir" are not
    var re = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|--[ \t][^\n]*|^[ \t]*#[^\n]*|#[ \t][^\n]*)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)/gm;
    while ((m = re.exec(src))) {
      out += plain(src.slice(last, m.index));
      out += m[1] ? '<span class="c">' + esc(m[1]) + "</span>" : '<span class="s">' + esc(m[2]) + "</span>";
      last = re.lastIndex;
    }
    out += plain(src.slice(last));
    el.innerHTML = out;
  });

  var cards = [].slice.call(document.querySelectorAll(".qa"));
  var countEl = document.getElementById("count");

  cards.forEach(function (c, i) {
    var n = c.querySelector(".num");
    if (n && !n.textContent.trim()) n.textContent = "Q" + (i + 1);
    c.dataset.txt = c.textContent.toLowerCase();
    c.dataset.isq = (n && /^Q\d+$/.test(n.textContent.trim())) ? "1" : "0";
  });

  var total = cards.filter(function (c) {
    var n = c.querySelector(".num");
    return n && /^Q\d+$/.test(n.textContent.trim());
  }).length;

  function updateCount(v) {
    if (countEl) countEl.textContent = (v === undefined ? total : v) + " / " + total + " questions";
  }
  updateCount();

  /* toggle a single card */
  document.addEventListener("click", function (e) {
    var q = e.target.closest(".q");
    if (q && q.parentElement.classList.contains("qa")) q.parentElement.classList.toggle("closed");
  });

  /* quiz mode — collapse every answer so you have to say it out loud first */
  var quizOn = false, quizBtn = document.getElementById("quiz");
  if (quizBtn) quizBtn.addEventListener("click", function () {
    quizOn = !quizOn;
    quizBtn.classList.toggle("on", quizOn);
    quizBtn.textContent = quizOn ? "Study mode" : "Quiz mode";
    cards.forEach(function (c) { c.classList.toggle("closed", quizOn); });
  });

  var expandBtn = document.getElementById("expand");
  if (expandBtn) expandBtn.addEventListener("click", function () {
    cards.forEach(function (c) { c.classList.remove("closed"); });
    quizOn = false;
    if (quizBtn) { quizBtn.classList.remove("on"); quizBtn.textContent = "Quiz mode"; }
  });

  /* theme */
  var root = document.documentElement, themeBtn = document.getElementById("theme");
  function paintTheme() {
    if (themeBtn) themeBtn.textContent = root.getAttribute("data-theme") === "dark" ? "Light" : "Dark";
  }
  var saved = localStorage.getItem("prep-theme");
  if (saved) root.setAttribute("data-theme", saved);
  paintTheme();
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("prep-theme", next);
    paintTheme();
  });

  /* search */
  var box = document.getElementById("search"), t;
  if (box) {
    box.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        var q = box.value.trim().toLowerCase(), shown = 0;
        cards.forEach(function (c) {
          var hit = !q || c.dataset.txt.indexOf(q) > -1;
          c.classList.toggle("hidden", !hit);
          if (hit && c.dataset.isq === "1") shown++;
        });
        // primers and diagrams are reference material, not results — hide them while filtering
        document.querySelectorAll("main figure, main .primer").forEach(function (f) {
          f.classList.toggle("hidden", !!q);
        });
        document.querySelectorAll("section.sec").forEach(function (s) {
          var any = s.querySelector(".qa:not(.hidden)");
          s.classList.toggle("hidden", !!q && !any);
        });
        updateCount(shown);
      }, 120);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== box) { e.preventDefault(); box.focus(); }
      if (e.key === "Escape" && document.activeElement === box) {
        box.value = ""; box.dispatchEvent(new Event("input")); box.blur();
      }
    });
  }
})();
