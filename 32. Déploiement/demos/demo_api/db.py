import sqlite3
# import supabase

DB_PATH = "predictions.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS predictions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 inputs TEXT,
                 result TEXT,
                 create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )
                 """)
    conn.commit()
    conn.close()

def save_prediction(inputs, result):
    conn = get_conn()
    conn.execute("INSERT INTO predictions (inputs, result) VALUES (?,?)",
                 (str(inputs), str(result)))
    conn.commit()
    conn.close()