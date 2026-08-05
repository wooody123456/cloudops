import os

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://cloudops:cloudops_password@localhost:5432/cloudops",
)


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
    conn.close()


@app.get("/healthz")
def healthz():
    try:
        with get_db().cursor() as cur:
            cur.execute("SELECT 1")
        return jsonify(status="ok", database="ok")
    except Exception:
        return jsonify(status="degraded", database="down"), 503


@app.get("/todos")
def list_todos():
    conn = get_db()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM todos ORDER BY id")
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.post("/todos")
def create_todo():
    data = request.get_json(force=True)
    title = data.get("title")
    if not title:
        return jsonify(error="title is required"), 400
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id, title, done", (title,))
        row = cur.fetchone()
    conn.close()
    return jsonify(id=row[0], title=row[1], done=row[2]), 201


@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    conn = get_db()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        row = cur.fetchone()
    conn.close()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(row)


@app.patch("/todos/<int:todo_id>")
def update_todo(todo_id):
    data = request.get_json(force=True)
    conn = get_db()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        row = cur.fetchone()
        if row is None:
            conn.close()
            return jsonify(error="not found"), 404
        title = data.get("title", row["title"])
        done = data.get("done", row["done"])
        cur.execute(
            "UPDATE todos SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
            (title, done, todo_id),
        )
        row = cur.fetchone()
    conn.close()
    return jsonify(id=row[0], title=row[1], done=row[2])


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM todos WHERE id = %s RETURNING id", (todo_id,))
        row = cur.fetchone()
    conn.close()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(deleted=row[0])


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
