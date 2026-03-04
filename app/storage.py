import os
import sqlite3
from datetime import datetime


class ScanStorage:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "scan_history.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                fraud_probability INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                fraud_type TEXT NOT NULL,
                explanation TEXT NOT NULL,
                scanned_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def save_scan(self, message, result):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO scans (
                message, fraud_probability, risk_level, fraud_type, explanation, scanned_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                message,
                int(result["fraud_probability"]),
                result["risk_level"],
                result["fraud_type"],
                result["explanation"],
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def recent_scans(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, message, fraud_probability, risk_level, fraud_type, scanned_at
            FROM scans
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()
        return rows
