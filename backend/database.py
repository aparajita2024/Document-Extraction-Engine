# backend/database.py
import sqlite3, json
from datetime import datetime

DB_PATH = "extractions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS extractions (
            id TEXT PRIMARY KEY,
            filename TEXT,
            document_type TEXT,
            timestamp TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_extraction(id, filename, doc_type, result: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO extractions VALUES (?, ?, ?, ?, ?)",
        (id, filename, doc_type, datetime.utcnow().isoformat(), json.dumps(result))
    )
    conn.commit()
    conn.close()

def update_extraction(id: str, result: dict):        # ✅ this was missing
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE extractions SET result=? WHERE id=?",
        (json.dumps(result), id)
    )
    conn.commit()
    conn.close()

def list_extractions():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, filename, document_type, timestamp FROM extractions ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [{"id": r[0], "filename": r[1], "document_type": r[2], "timestamp": r[3]} for r in rows]

def get_extraction(id: str):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT * FROM extractions WHERE id=?", (id,)).fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "filename": row[1], "document_type": row[2],
            "timestamp": row[3], "result": json.loads(row[4])}