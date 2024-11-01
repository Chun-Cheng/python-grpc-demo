from datetime import datetime

import grpc
from proto_gen.chat.message_pb2 import Message
from proto_gen.chat.room_pb2 import Room
from proto_gen.chat.user_pb2 import User
from proto_gen.chat.service_pb2 import UserRequest, RoomRequest, JoinRoomRequest
from proto_gen.chat.service_pb2_grpc import ServiceStub
from google.protobuf.timestamp_pb2 import Timestamp

import db as db

channel = grpc.insecure_channel('localhost:3000')
stub = ServiceStub(channel)

def signup(username: str) -> None:
    stub.CreateUser(UserRequest(username=username))
    db.set_username(username)
    db.update_rooms([])  # Initialize with an empty list of rooms

def get_rooms(username: str) -> list:
    rooms = stub.GetUser(UserRequest(username=username)).room_ids
    db.update_rooms(rooms)
    return rooms

def create_room(room_name: str, username: str) -> None:
    if not room_name.strip():
        raise ValueError("Room name cannot be empty")
    room_id = room_name.replace(" ", "-")
    stub.CreateRoom(Room(room_id=room_id, name=room_name, usernames=[username]))

def invite_user(room_id: str, username: str) -> None:
    stub.JoinRoom(JoinRoomRequest(room_id=room_id, username=username))

def get_room(room_id: str) -> Room:
    room = stub.GetRoom(RoomRequest(room_id=room_id))
    return {
        "room_id": room.room_id,
        "name": room.name,
        "usernames": room.usernames
    }

def send_message(room_id: str, author_id: str, message: str) -> None:
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime.now())
    msg = Message(
        message_id="",
        author_id=author_id,
        room_id=room_id,
        text=message,
        timestamp=timestamp
    )
    stub.SendMessage(msg)
    db.insert_message(msg.message_id, msg.author_id, msg.room_id, msg.text, datetime.fromtimestamp(msg.timestamp.seconds + msg.timestamp.nanos/1e9))

def get_new_messages(username: str) -> None:
    for message in stub.GetMessages(UserRequest(username=username)):
        db.insert_message(message.message_id, message.author_id, message.room_id, message.text, datetime.fromtimestamp(message.timestamp.seconds + message.timestamp.nanos/1e9))
