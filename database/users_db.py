"""
User and Session Database - SQLite persistent user tracking
"""

import sqlite3
from typing import Dict, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def _get_conn():
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        session_id TEXT PRIMARY KEY,
        name TEXT,
        roll_no TEXT,
        email TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_activity (
        session_id TEXT PRIMARY KEY,
        items_reported INTEGER DEFAULT 0,
        notes_uploaded INTEGER DEFAULT 0,
        notes_downloaded INTEGER DEFAULT 0,
        FOREIGN KEY(session_id) REFERENCES users(session_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS current_user (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        session_id TEXT
    )''')
    # Ensure there is always one row in current_user
    c.execute('INSERT OR IGNORE INTO current_user (id, session_id) VALUES (1, NULL)')
    conn.commit()
    conn.close()

_init_db()

def set_current_user(name: str, roll_no: str, email: str):
    """Set the current user information and track in DB"""
    session_id = f"{roll_no}_{name.replace(' ', '_')}"
    conn = _get_conn()
    c = conn.cursor()
    # Insert or update user
    c.execute('''INSERT OR REPLACE INTO users (session_id, name, roll_no, email) VALUES (?, ?, ?, ?)''',
              (session_id, name, roll_no, email))
    # Insert activity row if not exists
    c.execute('''INSERT OR IGNORE INTO user_activity (session_id) VALUES (?)''', (session_id,))
    # Set current user
    c.execute('''UPDATE current_user SET session_id = ? WHERE id = 1''', (session_id,))
    conn.commit()
    conn.close()

def get_current_user() -> Dict:
    """Get current user information from DB"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT session_id FROM current_user WHERE id = 1')
    row = c.fetchone()
    if not row or not row[0]:
        conn.close()
        return {'name': None, 'roll_no': None, 'email': None, 'session_id': None}
    session_id = row[0]
    c.execute('SELECT name, roll_no, email FROM users WHERE session_id = ?', (session_id,))
    user_row = c.fetchone()
    conn.close()
    if user_row:
        return {'name': user_row[0], 'roll_no': user_row[1], 'email': user_row[2], 'session_id': session_id}
    else:
        return {'name': None, 'roll_no': None, 'email': None, 'session_id': None}

def is_logged_in() -> bool:
    """Check if a user is logged in (in DB)"""
    user = get_current_user()
    return user['name'] is not None

def logout():
    """Logout current user (in DB)"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('UPDATE current_user SET session_id = NULL WHERE id = 1')
    conn.commit()
    conn.close()

def update_user_activity(activity_type: str):
    """Update user activity count in DB"""
    user = get_current_user()
    session_id = user['session_id']
    if not session_id:
        return
    conn = _get_conn()
    c = conn.cursor()
    if activity_type == 'item_reported':
        c.execute('UPDATE user_activity SET items_reported = items_reported + 1 WHERE session_id = ?', (session_id,))
    elif activity_type == 'note_uploaded':
        c.execute('UPDATE user_activity SET notes_uploaded = notes_uploaded + 1 WHERE session_id = ?', (session_id,))
    elif activity_type == 'note_downloaded':
        c.execute('UPDATE user_activity SET notes_downloaded = notes_downloaded + 1 WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()

def get_all_users() -> Dict:
    """Get all user sessions and activity from DB"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''SELECT u.session_id, u.name, u.roll_no, u.email, a.items_reported, a.notes_uploaded, a.notes_downloaded
                 FROM users u LEFT JOIN user_activity a ON u.session_id = a.session_id''')
    rows = c.fetchall()
    conn.close()
    result = {}
    for row in rows:
        result[row[0]] = {
            'name': row[1],
            'roll_no': row[2],
            'email': row[3],
            'items_reported': row[4] or 0,
            'notes_uploaded': row[5] or 0,
            'notes_downloaded': row[6] or 0
        }
    return result
