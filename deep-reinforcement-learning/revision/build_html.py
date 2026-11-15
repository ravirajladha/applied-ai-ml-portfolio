# Renders the .md study files -> dark self-contained .html, then -> .pdf via headless Chrome.
#
#   python build_html.py          # html only
#   python build_html.py --pdf    # html + pdf
#
# The .md files are the single source of truth. Never hand-edit the .html/.pdf.
import io, os, re, sys, html, shutil, subprocess, tempfile
import mistune

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    ("TONIGHT.md", "DRL Endsem — Tonight"),
]

CSS = """
:root{--bg:#0e1117;--panel:#161b26;--panel2:#1d2432;--line:#2b3446;--ink:#e6edf7;
      --dim:#93a1b8;--accent:#5aa9ff;--good:#3ddc97;--warn:#ffb454;--bad:#ff6b6b;--violet:#b78cff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:36px 22px 120px}
h1{font-size:31px;margin:38px 0 10px;letter-spacing:-.4px;padding-bottom:10px;
   border-bottom:2px solid var(--accent)}
h2{font-size:23px;margin:40px 0 12px;padding-top:16px;border-top:1px solid var(--line);color:#cfe3ff}
h3{font-size:17px;margin:24px 0 8px;color:var(--accent)}
p{margin:12px 0}
a{color:var(--accent)}
code{background:var(--panel2);padding:2px 6px;border-radius:4px;font-size:14px;
     font-family:ui-monospace,Consolas,monospace;color:#ffd9a0}
pre{background:#0a0e15;border:1px solid var(--line);border-radius:10px;padding:16px;
    overflow-x:auto;line-height:1.65}
pre code{background:none;padding:0;color:#c8d6e8;font-size:13.5px}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14.5px;
      display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:var(--panel2);color:#b9c8dd;font-weight:600}
tr:nth-child(even) td{background:#121724}
blockquote{border-left:3px solid var(--warn);background:#1b1a14;margin:16px 0;
           padding:12px 18px;border-radius:0 10px 10px 0}
blockquote p{margin:8px 0}
blockquote strong{color:var(--warn)}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}
ul,ol{padding-left:26px}
li{margin:5px 0}
details{background:var(--panel);border:1px solid var(--line);border-radius:10px;
        padding:12px 16px;margin:14px 0}
details[open]{border-color:var(--good);background:#111d19}
summary{cursor:pointer;font-weight:600;color:var(--good);outline:none}
summary:hover{color:#7ff0bd}
strong{color:#fff}
#toc{position:fixed;top:0;right:0;width:250px;height:100vh;overflow-y:auto;
     background:var(--panel);border-left:1px solid var(--line);padding:20px 16px;font-size:13px}
#toc b{display:block;color:var(--dim);text-transform:uppercase;letter-spacing:.6px;
       font-size:11px;margin-bottom:10px}
#toc a{display:block;padding:5px 8px;border-radius:6px;text-decoration:none;color:#a9bdd6}
#toc a:hover{background:var(--panel2);color:var(--accent)}
#toc a.h1{font-weight:700;color:var(--ink);margin-top:8px}
#toc a.h2{padding-left:18px;font-size:12.5px}
#bar{position:fixed;top:14px;left:14px;z-index:99;display:flex;gap:8px}
#bar button{background:var(--panel2);color:var(--ink);border:1px solid var(--line);
  border-radius:8px;padding:8px 14px;cursor:pointer;font:600 13px inherit}
#bar button:hover{border-color:var(--accent);color:var(--accent)}
@media(max-width:1400px){#toc{display:none}}

/* ---------- PRINT / PDF ---------- */
@media print{
  #toc,#bar{display:none!important}
  body{background:#fff;color:#111;font-size:10.5pt}
  .wrap{max-width:100%;padding:0}
  h1{font-size:19pt;color:#000;border-bottom:2px solid #333;page-break-after:avoid;
     page-break-before:always;margin-top:0}
  h1:first-of-type{page-break-before:avoid}
  h2{font-size:14pt;color:#000;border-top:1px solid #999;page-break-after:avoid}
  h3{font-size:11.5pt;color:#1a4d80;page-break-after:avoid}
  a{color:#1a4d80;text-decoration:none}
  code{background:#eef1f5;color:#7a3d00;border:1px solid #dde3ea}
  pre{background:#f6f8fa;border:1px solid #c9d1d9;color:#111;page-break-inside:avoid;
      font-size:9pt;line-height:1.45}
  pre code{color:#111;font-size:9pt}
  table{font-size:9pt;display:table;page-break-inside:avoid}
  th{background:#e8edf3!important;color:#000}
  td{background:#fff!important}
  tr:nth-child(even) td{background:#f7f9fb!important}
  th,td{border:1px solid #b6c0cc;padding:5px 7px}
  blockquote{background:#fffdf3;border-left:3px solid #d19a20;color:#111;
             page-break-inside:avoid}
  blockquote strong{color:#8a5a00}
  strong{color:#000}
  details{background:#f4faf7;border:1px solid #b9d9c9;page-break-inside:avoid}
  details[open]{background:#f4faf7}
  summary{color:#14663f}
  hr{border-top:1px solid #bbb}
  ul,ol{padding-left:20px}
}
@page{size:A4;margin:14mm 12mm}
"""

JS = r"""
var wasOpen = [];
function openAll(){
  wasOpen = [];
  document.querySelectorAll("details").forEach(function(d,i){
    wasOpen[i] = d.open; d.open = true;
  });
}
function restoreAll(){
  document.querySelectorAll("details").forEach(function(d,i){ d.open = wasOpen[i]; });
}
window.addEventListener("beforeprint", openAll);
window.addEventListener("afterprint", restoreAll);

function doPrint(){ openAll(); window.print(); }
function toggleAll(){
  var ds = document.querySelectorAll("details");
  var anyClosed = Array.prototype.some.call(ds, function(d){ return !d.open; });
  ds.forEach(function(d){ d.open = anyClosed; });
  document.getElementById("tgl").textContent = anyClosed ? "Hide all answers" : "Show all answers";
}

var out = "";
document.querySelectorAll(".wrap h1, .wrap h2").forEach(function(h){
  if(!h.id) return;
  out += '<a class="' + h.tagName.toLowerCase() + '" href="#' + h.id + '">' +
         h.textContent.replace(/^[0-9]+[.]\s*/, "") + "</a>";
});
document.getElementById("toclinks").innerHTML = out;
"""

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style></head>
<body>
<div id="bar">
  <button onclick="doPrint()">&#128424; Print / Save as PDF</button>
  <button id="tgl" onclick="toggleAll()">Show all answers</button>
</div>
<nav id="toc"><b>Jump to</b><div id="toclinks"></div></nav>
<div class="wrap">%s</div>
<script>%s</script>
</body></html>"""


def ghslug(h):
    # strip tags, then DECODE ENTITIES (&amp; -> &) so "&" doesn't slug as "amp"
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).lower()
    t = re.sub(r"[^\w\s\-]", "", t, flags=re.U)
    return t.replace(" ", "-")


def build_html(mdname, title):
    md = io.open(os.path.join(HERE, mdname), encoding="utf-8").read()
    convert = mistune.create_markdown(
        renderer=mistune.HTMLRenderer(escape=False),
        plugins=["table", "strikethrough", "footnotes"],
    )
    body = convert(md)
    body = re.sub(
        r"<h([1-3])>(.*?)</h\1>",
        lambda m: '<h%s id="%s">%s</h%s>' % (m.group(1), ghslug(m.group(2)), m.group(2), m.group(1)),
        body, flags=re.S,
    )
    out = os.path.join(HERE, mdname.replace(".md", ".html"))
    io.open(out, "w", encoding="utf-8").write(PAGE % (title, CSS, body, JS))
    print("  html  %-26s %6.0f KB" % (os.path.basename(out), os.path.getsize(out) / 1024))
    return out


def find_chrome():
    cands = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return shutil.which("chrome") or shutil.which("msedge")


def build_pdf(htmlpath):
    exe = find_chrome()
    if not exe:
        print("  !! no Chrome/Edge found — open the .html and press the Print button instead")
        return None
    pdf = htmlpath.replace(".html", ".pdf")
    prof = tempfile.mkdtemp(prefix="mdpdf_")
    url = "file:///" + htmlpath.replace("\\", "/")
    cmd = [exe, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=12000", "--user-data-dir=" + prof,
           "--print-to-pdf=" + pdf, url]
    try:
        subprocess.run(cmd, capture_output=True, timeout=180)
    except subprocess.TimeoutExpired:
        print("  !! PDF render timed out")
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    if os.path.exists(pdf) and os.path.getsize(pdf) > 20000:
        print("  pdf   %-26s %6.0f KB" % (os.path.basename(pdf), os.path.getsize(pdf) / 1024))
        return pdf
    print("  !! PDF not produced for", os.path.basename(htmlpath))
    return None


if __name__ == "__main__":
    want_pdf = "--pdf" in sys.argv
    for mdname, title in FILES:
        if not os.path.exists(os.path.join(HERE, mdname)):
            print("  skip (missing)", mdname); continue
        h = build_html(mdname, title)
        if want_pdf:
            build_pdf(h)
    print("done.")
