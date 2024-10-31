import sqlite3
from datetime import datetime

con = sqlite3.connect("nori_client.db")
cur = con.cursor()

def init_db() -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, msg_id TEXT, author_user_id TEXT, room_id TEXT, message TEXT, timestamp TEXT)")
    con.commit()

def get_username() -> str | None:
    try:
        cur.execute("SELECT username FROM users")
        result = cur.fetchone()
        return result[0] if result else None
    except sqlite3.OperationalError:
        return None

def set_username(username: str) -> None:
    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
    con.commit()

def insert_message(msg_id: str, author_user_id: str, room_id: str, message: str, timestamp: datetime) -> None:
    cur.execute("INSERT INTO messages (msg_id, author_user_id, room_id, message, timestamp) VALUES (?, ?, ?, ?, ?)", (msg_id, author_user_id, room_id, message, timestamp))
    con.commit()

def get_messages(room_id: str) -> list:
    cur.execute("SELECT message FROM messages WHERE room_id = ? ORDER BY timestamp ASC", (room_id,))
    return [row[0] for row in cur.fetchall()]
