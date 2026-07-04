# flask-ml-crud

A small **Flask** web app built for learning ML/AI workflows. It's an
**ML Experiment Tracker**: a full CRUD (Create, Read, Update, Delete) interface
over the kind of records you keep when experimenting with machine-learning
models — model name, algorithm, accuracy, and notes.

The goal is to give you a clean, minimal codebase you can extend as you learn:
plug in scikit-learn to log real runs, add charts, expose a JSON API, etc.

## Features

- **Create** new experiment records
- **Read** / list all experiments (newest first)
- **Update** an existing experiment
- **Delete** experiments
- Server-side validation (name required, accuracy between 0 and 1)
- Zero external database — data is stored in a local SQLite file
- Clean, dependency-light code using only Flask + the Python standard library

## Tech stack

| Layer     | Choice                              |
|-----------|-------------------------------------|
| Web       | Flask (Jinja2 templates)            |
| Database  | SQLite via the stdlib `sqlite3`     |
| Styling   | Plain CSS                           |

## Project layout

```
flask-ml-crud/
├── app.py              # Flask routes (the CRUD endpoints)
├── db.py               # SQLite data-access layer
├── requirements.txt
├── templates/
│   ├── base.html       # Shared layout
│   ├── index.html      # List view (Read)
│   └── form.html       # Create / Update form
└── static/
    └── style.css
```

## Getting started

```bash
# 1. (optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. run the app
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

The SQLite database (`experiments.db`) is created automatically on first run.

## Ideas for extending it (great ML/AI practice)

- Train a scikit-learn model and auto-fill the accuracy field
- Add a chart comparing accuracy across experiments
- Expose the CRUD operations as a JSON REST API
- Add search / filtering by algorithm
- Store hyperparameters as structured JSON

## License

MIT
