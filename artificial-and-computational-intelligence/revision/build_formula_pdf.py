# Renders formula-sheet.md -> a COMPACT, print-first formula-sheet.pdf.
#
#   python build_formula_pdf.py
#
# Separate from build_html.py on purpose: the study files are laid out for
# reading on screen, this one is laid out to be printed, stapled and flipped
# through during an open-book exam. Denser type, tighter margins, and no
# section is ever split across a page break.
import io, os, re, sys, html
import mistune
import build_html as bh          # reuse find_chrome() / build_pdf()

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, TITLE = "formula-sheet.md", "ACI — Formula Sheet (print)"

CSS = """
:root{--bg:#0e1117;--panel2:#1d2432;--line:#2b3446;--ink:#e6edf7;--accent:#5aa9ff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:28px 20px 90px}
h1{font-size:27px;margin:0 0 8px;border-bottom:2px solid var(--accent);padding-bottom:8px}
h2{font-size:19px;margin:22px 0 8px;color:#cfe3ff;border-top:1px solid var(--line);padding-top:12px}
h3{font-size:15px;margin:14px 0 6px;color:var(--accent)}
p{margin:8px 0}
code{background:var(--panel2);padding:1px 5px;border-radius:4px;font-size:13px;
     font-family:ui-monospace,Consolas,monospace;color:#ffd9a0}
pre{background:#0a0e15;border:1px solid var(--line);border-radius:8px;padding:12px;
    overflow-x:auto;line-height:1.5}
pre code{background:none;padding:0;color:#c8d6e8;font-size:12.5px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13.5px}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--panel2);color:#b9c8dd}
blockquote{border-left:3px solid #ffb454;background:#1b1a14;margin:10px 0;padding:8px 14px;
           border-radius:0 8px 8px 0}
ul,ol{padding-left:22px;margin:8px 0}
li{margin:2px 0}
strong{color:#fff}
#bar{position:fixed;top:12px;left:12px;z-index:99}
#bar button{background:var(--panel2);color:var(--ink);border:1px solid var(--line);
  border-radius:8px;padding:8px 14px;cursor:pointer;font:600 13px inherit}

/* ---------- PRINT: dense, and never split a section ---------- */
@media print{
  #bar{display:none!important}
  body{background:#fff;color:#000;font:8.6pt/1.34 "Segoe UI",Arial,sans-serif}
  .wrap{max-width:100%;padding:0}
  .blk{page-break-inside:avoid;break-inside:avoid}
  h1{font-size:15pt;color:#000;border-bottom:1.5pt solid #000;margin:0 0 6pt;padding-bottom:4pt}
  h2{font-size:10.5pt;color:#fff;background:#333;margin:9pt 0 4pt;padding:2.5pt 6pt;
     border:0;border-radius:2pt;page-break-after:avoid}
  h3{font-size:9pt;color:#000;margin:6pt 0 3pt;padding:0;
     border-bottom:.5pt solid #999;page-break-after:avoid}
  p{margin:3pt 0}
  code{background:#eef1f5;color:#000;border:.5pt solid #ccc;font-size:8pt;padding:0 2pt}
  pre{background:#f7f8fa;border:.5pt solid #bbb;border-radius:0;padding:4pt 6pt;
      margin:4pt 0;page-break-inside:avoid;font-size:7.7pt;line-height:1.32}
  pre code{color:#000;font-size:7.7pt;border:0;background:none}
  table{font-size:7.7pt;margin:4pt 0;page-break-inside:avoid}
  th,td{border:.5pt solid #888;padding:1.8pt 3.5pt}
  th{background:#e4e9ef!important;color:#000}
  blockquote{background:#fffdf3;border-left:2pt solid #c8930f;color:#000;
             margin:4pt 0;padding:3pt 8pt;page-break-inside:avoid}
  ul,ol{padding-left:14pt;margin:3pt 0}
  li{margin:0}
  strong{color:#000}
  a{color:#000;text-decoration:none}
}
@page{size:A4;margin:9mm 8mm}
"""

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title><style>%s</style></head>
<body>
<div id="bar"><button onclick="window.print()">&#128424; Print / Save as PDF</button></div>
<div class="wrap">%s</div>
</body></html>"""


def wrap_sections(body):
    """Wrap each <h2>-led block in .blk so a section is never split across pages."""
    parts = re.split(r"(?=<h2[ >])", body)
    if len(parts) == 1:
        return body
    out = [parts[0]]
    out += ['<section class="blk">%s</section>' % p for p in parts[1:]]
    return "".join(out)


def main():
    md = io.open(os.path.join(HERE, SRC), encoding="utf-8").read()
    convert = mistune.create_markdown(
        renderer=mistune.HTMLRenderer(escape=False),
        plugins=["table", "strikethrough"],
    )
    body = convert(md)
    body = re.sub(
        r"<h([1-3])>(.*?)</h\1>",
        lambda m: '<h%s id="%s">%s</h%s>'
        % (m.group(1), bh.ghslug(m.group(2)), m.group(2), m.group(1)),
        body, flags=re.S,
    )
    body = wrap_sections(body)
    out = os.path.join(HERE, "formula-sheet.html")
    io.open(out, "w", encoding="utf-8").write(PAGE % (TITLE, CSS, body))
    print("  html  %-24s %6.0f KB" % (os.path.basename(out), os.path.getsize(out) / 1024))
    pdf = bh.build_pdf(out)
    if pdf:
        try:
            from pypdf import PdfReader
            print("  pages %d" % len(PdfReader(pdf).pages))
        except Exception:
            pass


if __name__ == "__main__":
    main()
