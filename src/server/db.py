import sqlite3
from snowflake import SnowflakeGenerator
from datetime import datetime

id_gen = SnowflakeGenerator(1)

def list_to_str(a_list: list) -> str:
    return ",".join(a_list)

def str_to_list(a_string: str) -> list:
    if not a_string:
        return []
    return a_string.split(",")


con = sqlite3.connect('nori_server.db', check_same_thread=False)
cur = con.cursor()

def init_db() -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, rooms TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, room_id TEXT, name TEXT, user_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, msg_id TEXT, author_user_id TEXT, room_id TEXT, message TEXT, timestamp TEXT)")
    con.commit()

def new_user(username: str, password: str) -> None:
    cur.execute("INSERT INTO users (username, password, rooms) VALUES (?, ?, ?)", (username, hash(password), ""))
    con.commit()

def get_user(username: str) -> dict:
    cur.execute("SELECT username, rooms FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    return {
        "username": result[0] if result else "",
        "rooms": str_to_list(result[1]) if result else []
    }

def generate_room_id() -> str:
    return str(next(id_gen))

def new_room(room_id: str, name: str, user_ids: list[str]) -> None:
    cur.execute("INSERT INTO rooms (room_id, name, user_id) VALUES (?, ?, ?)", (room_id, name, list_to_str(user_ids)))
    # add room_id into users table
    for user_id in user_ids:
        cur.execute("SELECT rooms FROM users WHERE username = ?", (user_id,))
        result = cur.fetchone()
        user_rooms = result[0] if result else ""
        user_rooms = str_to_list(user_rooms)
        user_rooms.append(room_id)
        cur.execute("UPDATE users SET rooms = ? WHERE username = ?", (list_to_str(user_rooms), user_id))
    con.commit()

def join_room(user_id: str, room_id: str) -> None:
    # add room_id into users table
    cur.execute("SELECT rooms FROM users WHERE username = ?", (user_id,))
    result = cur.fetchone()
    user_rooms = result[0] if result else ""
    user_rooms = str_to_list(user_rooms)
    user_rooms.append(room_id)
    cur.execute("UPDATE users SET rooms = ? WHERE username = ?", (list_to_str(user_rooms), user_id))
    # add user_id into rooms table
    cur.execute("SELECT user_id FROM rooms WHERE room_id = ?", (room_id,))
    result = cur.fetchone()
    room_users = result[0] if result else ""
    room_users = str_to_list(room_users)
    room_users.append(user_id)
    cur.execute("UPDATE rooms SET user_id = ? WHERE room_id = ?", (list_to_str(room_users), room_id))
    # commit
    con.commit()

def get_room(room_id: str) -> dict:
    cur.execute("SELECT room_id, name, user_id FROM rooms WHERE room_id = ?", (room_id,))
    result = cur.fetchone()
    return {
        "room_id": result[0] if result else "",
        "name": result[1] if result else "",
        "user_ids": str_to_list(result[2]) if result else []
    }

def new_message(author_user_id: str, room_id: str, message: str, timestamp: datetime) -> None:
    cur.execute(
        "INSERT INTO messages (msg_id, author_user_id, room_id, message, timestamp) VALUES (?, ?, ?, ?, ?)", 
        (next(id_gen), author_user_id, room_id, message, timestamp)
    )
    con.commit()

def get_user_messages(user_id: str) -> list:
    # get rooms from users table
    cur.execute("SELECT rooms FROM users WHERE id = ?", (user_id,))
    rooms = str_to_list(cur.fetchone()[0])
    # get messages from messages table (exclude the messages from the user)
    cur.execute("SELECT * FROM messages WHERE room_id room_id IN ? AND author_user_id != ?", (tuple(rooms), user_id))
    result = cur.fetchall()
    # turn result from list of tuple into list of dict and return
    return [
        {
            "msg_id": row[0],
            "author_user_id": row[1],
            "room_id": row[2],
            "message": row[3],
            "timestamp": row[4]
        }
        for row in result
    ]
