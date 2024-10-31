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

# def get_username() -> str | None:
#     result = db.get_username()
#     return result if result else None

def signup(username: str) -> None:
    stub.CreateUser(User(username=username, password="", room_ids=[]))
    db.set_username(username)

def get_rooms(username: str) -> list:
    rooms = stub.GetUser(UserRequest(username=username)).room_ids
    db.update_rooms(rooms)
    return rooms

def create_room(room_name: str, username: str) -> None:
    stub.CreateRoom(Room(room_id=room_name.replace(" ", "-"), name=room_name, user_ids=[username]))

def invite_user(room_id: str, username: str) -> None:
    room = stub.GetRoom(RoomRequest(room_id=room_id))
    stub.JoinRoom(JoinRoomRequest(room_id=room.room_id, user_id=username))

def send_message(room_id: str, author_id: str, message: str) -> None:
    timestamp=Timestamp()
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

def join_room(room_id: str, username: str) -> None:
    room = stub.GetRoom(RoomRequest(room_id=room_id))
    stub.JoinRoom(JoinRoomRequest(room_id=room.room_id, user_id=username))
    db.join_room(room.room_id)

async def get_new_messages(room_id: str) -> None:
    for message in stub.GetMessages(UserRequest(username=db.get_username())):
        db.insert_message(message.message_id, message.author_id, room_id, message.text, message.timestamp)
