import os
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'readings.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ettan TEXT,
                spansk_timjan TEXT,
                nummer_3 TEXT
            )
        ''')
        conn.commit()

def save_reading(timestamp, ettan, spansk_timjan, nummer_3):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO readings (timestamp, ettan, spansk_timjan, nummer_3)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, ettan, spansk_timjan, nummer_3))
        
        # Radera gamla mätningar
        cutoff_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        cursor.execute('''
            DELETE FROM readings
            WHERE timestamp < ?
        ''', (cutoff_date,))
        
        conn.commit()

def get_latest():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM readings
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        
        if row:
            return {
                'timestamp': row['timestamp'],
                'ettan': row['ettan'],
                'spansk_timjan': row['spansk_timjan'],
                'nummer_3': row['nummer_3']
            }
        return None
