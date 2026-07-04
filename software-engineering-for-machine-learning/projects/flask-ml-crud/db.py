"""Database layer for flask-ml-crud.

Uses Python's built-in ``sqlite3`` module so there are no extra dependencies to
install. The whole database lives in a single file, ``experiments.db``, created
automatically next to this script.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "experiments.db")


def get_connection():
    """Open a connection with rows accessible by column name."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the experiments table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                algorithm  TEXT,
                accuracy   REAL,
                notes      TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def list_experiments():
    """Return all experiments, newest first."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM experiments ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return rows


def get_experiment(experiment_id):
    """Return a single experiment by id, or None if it does not exist."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM experiments WHERE id = ?", (experiment_id,)
        ).fetchone()
    return row


def create_experiment(name, algorithm, accuracy, notes):
    """Insert a new experiment and return its id."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO experiments (name, algorithm, accuracy, notes)
            VALUES (?, ?, ?, ?)
            """,
            (name, algorithm, accuracy, notes),
        )
        return cursor.lastrowid


def update_experiment(experiment_id, name, algorithm, accuracy, notes):
    """Update an existing experiment in place."""
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE experiments
            SET name = ?, algorithm = ?, accuracy = ?, notes = ?
            WHERE id = ?
            """,
            (name, algorithm, accuracy, notes, experiment_id),
        )


def delete_experiment(experiment_id):
    """Remove an experiment by id."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM experiments WHERE id = ?", (experiment_id,)
        )
