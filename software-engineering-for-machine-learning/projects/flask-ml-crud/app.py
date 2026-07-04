"""flask-ml-crud

A small Flask application for learning ML/AI workflows. It provides full
CRUD (Create, Read, Update, Delete) over a table of "experiments" -- the kind
of records you keep when tracking machine-learning model runs: the model name,
the algorithm used, the accuracy achieved, and free-form notes.

Run it with:

    python app.py

then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request, redirect, url_for, flash

import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"

# Make sure the database and table exist before the first request.
db.init_db()


@app.route("/")
def index():
    """List every experiment (the "Read all" part of CRUD)."""
    experiments = db.list_experiments()
    return render_template("index.html", experiments=experiments)


@app.route("/experiments/new", methods=["GET", "POST"])
def create():
    """Create a new experiment."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        algorithm = request.form.get("algorithm", "").strip()
        accuracy = request.form.get("accuracy", "").strip()
        notes = request.form.get("notes", "").strip()

        error = _validate(name, accuracy)
        if error:
            flash(error, "error")
            return render_template(
                "form.html",
                action="Create",
                experiment=request.form,
            )

        db.create_experiment(name, algorithm, _to_float(accuracy), notes)
        flash("Experiment created.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", action="Create", experiment={})


@app.route("/experiments/<int:experiment_id>/edit", methods=["GET", "POST"])
def update(experiment_id):
    """Update an existing experiment."""
    experiment = db.get_experiment(experiment_id)
    if experiment is None:
        flash("Experiment not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        algorithm = request.form.get("algorithm", "").strip()
        accuracy = request.form.get("accuracy", "").strip()
        notes = request.form.get("notes", "").strip()

        error = _validate(name, accuracy)
        if error:
            flash(error, "error")
            return render_template(
                "form.html",
                action="Update",
                experiment=request.form,
            )

        db.update_experiment(
            experiment_id, name, algorithm, _to_float(accuracy), notes
        )
        flash("Experiment updated.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", action="Update", experiment=experiment)


@app.route("/experiments/<int:experiment_id>/delete", methods=["POST"])
def delete(experiment_id):
    """Delete an experiment."""
    db.delete_experiment(experiment_id)
    flash("Experiment deleted.", "success")
    return redirect(url_for("index"))


def _validate(name, accuracy):
    """Return an error message if the form input is invalid, else None."""
    if not name:
        return "Name is required."
    if accuracy:
        value = _to_float(accuracy)
        if value is None:
            return "Accuracy must be a number."
        if not 0 <= value <= 1:
            return "Accuracy must be between 0 and 1."
    return None


def _to_float(value):
    """Best-effort float conversion; returns None on failure or empty input."""
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    app.run(debug=True)
