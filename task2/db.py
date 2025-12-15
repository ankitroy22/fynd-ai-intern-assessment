import sqlite3
from datetime import datetime

DB_PATH = "feedback.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            rating INTEGER,
            review TEXT,
            ai_response TEXT,
            ai_summary TEXT,
            ai_actions TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_feedback(rating, review, ai_response, ai_summary, ai_actions):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (timestamp, rating, review, ai_response, ai_summary, ai_actions)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        rating,
        review,
        ai_response,
        ai_summary,
        ai_actions
    ))

    conn.commit()
    conn.close()

def fetch_all_feedback():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, rating, review, ai_response, ai_summary, ai_actions
        FROM feedback
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows
