"""
User authentication and audit logging database models using SQLite.
Stores user accounts (with role/group details) and logs every single compilation action:
Who ran what engine, at what timestamp, the input code snippet, and the result status.
"""

import sqlite3
import hashlib
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "compiler_logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        roll_number TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'Evaluator',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Audit Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        action TEXT NOT NULL,          -- e.g. 'LEXICAL_SCAN', 'SYNTAX_PARSE', 'SEMANTIC_CHECK', 'ICG_GEN', 'FULL_PIPELINE'
        status TEXT NOT NULL,          -- 'SUCCESS' or 'ERROR'
        details TEXT,                  -- error message or summary (e.g. '24 tokens generated')
        code_snippet TEXT,             -- first 150 chars or full code
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    
    # Pre-populate group members & evaluator accounts if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("ahsan", hash_password("ahsan123"), "Syed Ahsan Hassan Rizvi", "EB-24210006096", "Group Leader"),
            ("sami", hash_password("sami123"), "Sami Ur Rehman", "EB-24210006086", "Group Member"),
            ("behroz", hash_password("behroz123"), "M. Behroz Abid", "EB-24210006001", "Group Member"),
            ("instructor", hash_password("instructor123"), "Course Instructor / Evaluator", "FACULTY-01", "Evaluator / Sir"),
            ("guest", hash_password("guest123"), "Guest Student", "EB-GUEST", "Student")
        ]
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, roll_number, role)
            VALUES (?, ?, ?, ?, ?)
        """, default_users)
        conn.commit()
        
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_user(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    p_hash = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username.strip().lower(), p_hash))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def register_user(username: str, password: str, full_name: str, roll_number: str, role: str = "Student"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, roll_number, role)
            VALUES (?, ?, ?, ?, ?)
        """, (username.strip().lower(), hash_password(password), full_name.strip(), roll_number.strip(), role))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def log_action(username: str, action: str, status: str, details: str, code: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Store clean preview of code
    snippet = code.strip()[:200]
    cursor.execute("""
        INSERT INTO audit_logs (username, action, status, details, code_snippet, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, action, status, details, snippet, now_str))
    conn.commit()
    conn.close()

def get_recent_logs(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def clear_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audit_logs")
    conn.commit()
    conn.close()

