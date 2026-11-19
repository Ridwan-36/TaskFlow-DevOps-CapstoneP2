import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "taskflow_db"),
        user=os.getenv("DB_USER", "taskflow_user"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )


@app.route("/")
def home():
    return jsonify({
        "application": "TaskFlow",
        "message": "TaskFlow Backend is running!",
        "status": "success"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY id")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(task) for task in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (title, data.get("description", ""), data.get("status", "Pending"))
    )

    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(dict(task)), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        UPDATE tasks
        SET title = COALESCE(%s, title),
            description = COALESCE(%s, description),
            status = COALESCE(%s, status)
        WHERE id = %s
        RETURNING *
        """,
        (
            data.get("title"),
            data.get("description"),
            data.get("status"),
            task_id
        )
    )

    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(task))


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = %s RETURNING id",
        (task_id,)
    )

    deleted_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted successfully",
        "id": task_id
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
