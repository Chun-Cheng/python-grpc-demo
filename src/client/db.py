import sqlite3
from datetime import datetime

con = sqlite3.connect("client.db")
cur = con.cursor()

def init_db() -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS host (id INTEGER PRIMARY KEY, host TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, target_username TEXT, msg_id TEXT, author_username TEXT, room_id TEXT, message TEXT, timestamp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, room_id TEXT)")
    con.commit()

def get_host() -> str:
    cur.execute("SELECT host FROM host")
    return cur.fetchone()[0]

def set_host(host: str) -> None:
    cur.execute("INSERT INTO host (host) VALUES (?)", (host,))
    con.commit()

def get_users() -> list:
    cur.execute("SELECT username FROM users")
    return [row[0] for row in cur.fetchall()]

def set_username(username: str) -> None:
    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
    con.commit()

def insert_message(target_username: str, msg_id: str, author_username: str, room_id: str, message: str, timestamp: datetime) -> None:
    cur.execute(
        "INSERT INTO messages (target_username, msg_id, author_username, room_id, message, timestamp) VALUES (?, ?, ?, ?, ?, ?)", 
        (target_username, msg_id, author_username, room_id, message, timestamp)
    )
    con.commit()

def get_messages(target_username: str, room_id: str) -> list:
    cur.execute("SELECT msg_id, author_username, room_id, message, timestamp FROM messages WHERE target_username = ? AND room_id = ? ORDER BY timestamp ASC", (target_username, room_id))
    return [
        {
            "msg_id": row[0],
            "author": row[1],
            "room_id": row[2],
            "text": row[3],
            "timestamp": row[4]
        } for row in cur.fetchall()
    ]

def update_rooms(rooms: list) -> None:
    cur.execute("DELETE FROM rooms")
    for room in rooms:
        cur.execute("INSERT INTO rooms (room_id) VALUES (?)", (room,))
    con.commit()

def join_room(room_id: str) -> None:
    cur.execute("INSERT INTO rooms (room_id) VALUES (?)", (room_id,))
    con.commit()
