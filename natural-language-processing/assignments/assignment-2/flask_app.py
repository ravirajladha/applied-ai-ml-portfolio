"""Task 4 - Flask front end (alternative to the Streamlit app).

Owner: Member 4 (Application & DevOps Engineer).

The problem statement allows Streamlit *or* Flask. Both are provided:
Streamlit for the demo, Flask for environments where a plain WSGI server
is easier to deploy - such as the OSHA Virtual Lab.

Run:  python flask_app.py     then open http://localhost:5000

It also exposes a JSON endpoint:
    POST /api/summarize   {"reviews": ["...", "..."]}
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template_string, request

from config import FLASK_PORT, MAX_REVIEWS_DEFAULT, use_utf8_console
from data_prep import split_reviews
from summarizer_service import (analyse, load_sample_reviews,
                                reviews_from_file, to_plain_dict)

app = Flask(__name__)

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Customer Review Summarization</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;
      padding:0 1rem;line-height:1.5;color:#1a1a2e}
 h1{margin-bottom:.2rem} .sub{color:#555;margin-top:0}
 textarea{width:100%;height:180px;font:inherit;padding:.6rem;
          border:1px solid #ccc;border-radius:6px}
 button{background:#2e5e9e;color:#fff;border:0;padding:.6rem 1.2rem;
        border-radius:6px;font-size:1rem;cursor:pointer}
 .verdict{background:#e8f4ec;border-left:4px solid #2e9e5b;padding:.8rem 1rem;
          border-radius:4px;margin:1rem 0}
 .cols{display:flex;gap:2rem;flex-wrap:wrap}.col{flex:1;min-width:240px}
 .pos li::marker{color:#2e9e5b}.neg li::marker{color:#d1495b}
 table{border-collapse:collapse;width:100%;margin-top:.5rem}
 th,td{border:1px solid #ddd;padding:.4rem .6rem;text-align:left;
       font-size:.92rem;vertical-align:top}
 th{background:#f4f6f8} .tiles{display:flex;gap:1.5rem;margin:1rem 0}
 .tile b{display:block;font-size:1.6rem}
</style></head><body>
<h1>Customer Review Summarization</h1>
<p class="sub">Paste many reviews for one product, or upload a .txt / .csv file.</p>

<form method="post" enctype="multipart/form-data">
  <textarea name="reviews" placeholder="One review per line...">{{ text }}</textarea>
  <p><input type="file" name="file" accept=".txt,.csv">
     <label><input type="checkbox" name="use_sample" {{ sample_checked }}>
     use the sample product</label></p>
  <button type="submit">Summarize reviews</button>
</form>

{% if result %}
  {% if result.error %}<p style="color:#d1495b">{{ result.error }}</p>{% else %}
  <h2>Overall summary</h2>
  <div class="verdict">{{ result.overall_summary }}</div>
  <div class="tiles">
    <div class="tile"><b>{{ result.n_reviews }}</b>reviews</div>
    <div class="tile"><b>{{ result.sentiment.positive }}</b>positive</div>
    <div class="tile"><b>{{ result.sentiment.negative }}</b>negative</div>
    <div class="tile"><b>{{ (result.sentiment.positive_share*100)|round|int }}%</b>positive share</div>
  </div>
  <div class="cols">
    <div class="col"><h3>Praised</h3><ul class="pos">
      {% for a in result.praised_aspects %}<li>{{ a.aspect }} ({{ a.mentions }})</li>{% endfor %}
    </ul></div>
    <div class="col"><h3>Criticised</h3><ul class="neg">
      {% for a in result.criticised_aspects %}<li>{{ a.aspect }} ({{ a.mentions }})</li>{% endfor %}
    </ul></div>
  </div>
  <h2>Per-review summaries</h2>
  <table><tr><th>Review</th><th>Generated summary</th></tr>
  {% for row in result.summaries %}
    <tr><td>{{ row.review[:180] }}...</td><td>{{ row.summary }}</td></tr>
  {% endfor %}</table>
  {% endif %}
{% endif %}
</body></html>"""


def _collect_reviews(form, files) -> list[str]:
    """Work out which of the three inputs the user actually used."""
    if form.get("use_sample"):
        return load_sample_reviews()

    upload = files.get("file")
    if upload and upload.filename:
        return reviews_from_file(upload.filename, upload.read())

    return split_reviews(form.get("reviews", ""))


@app.route("/", methods=["GET", "POST"])
def index():
    result, text = None, ""
    if request.method == "POST":
        text = request.form.get("reviews", "")
        reviews = _collect_reviews(request.form, request.files)
        result = to_plain_dict(analyse(reviews))
    return render_template_string(
        PAGE, result=result, text=text,
        sample_checked="checked" if request.form.get("use_sample") else "")


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """JSON endpoint, for scripted use and testing."""
    payload = request.get_json(silent=True) or {}
    reviews = payload.get("reviews") or []
    if isinstance(reviews, str):
        reviews = split_reviews(reviews)
    if not reviews:
        return jsonify({"error": "send {'reviews': [...]}"}), 400

    max_reviews = int(payload.get("max_reviews", MAX_REVIEWS_DEFAULT))
    return jsonify(to_plain_dict(analyse(reviews, max_reviews=max_reviews)))


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    use_utf8_console()
    print(f"Flask app on http://localhost:{FLASK_PORT}")
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)
