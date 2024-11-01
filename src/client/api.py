from datetime import datetime, timezone
from typing import Any

import grpc
from proto_gen.chat.message_pb2 import Message
from proto_gen.chat.room_pb2 import Room
from proto_gen.chat.user_pb2 import User
from proto_gen.chat.service_pb2 import UserRequest, RoomRequest, JoinRoomRequest
from proto_gen.chat.service_pb2_grpc import ServiceStub
from google.protobuf.timestamp_pb2 import Timestamp

import db as db

class API:
    def __init__(self: Any) -> None:
        self.channel = grpc.insecure_channel(db.get_host())
        self.stub = ServiceStub(self.channel)

    def signup(self: Any, username: str) -> None:
        self.stub.CreateUser(UserRequest(username=username))
        db.set_username(username)
        db.update_rooms([])  # Initialize with an empty list of rooms

    def get_rooms(self: Any, username: str) -> list:
        rooms = self.stub.GetUser(UserRequest(username=username)).room_ids
        db.update_rooms(rooms)
        return rooms

    def create_room(self: Any, room_name: str, username: str) -> None:
        if not room_name.strip():
            raise ValueError("Room name cannot be empty")
        room_id = room_name.replace(" ", "-")
        self.stub.CreateRoom(Room(room_id=room_id, name=room_name, usernames=[username]))

    def invite_user(self: Any, room_id: str, username: str) -> None:
        self.stub.JoinRoom(JoinRoomRequest(room_id=room_id, username=username))

    def get_room(self: Any, room_id: str) -> Room:
        room = self.stub.GetRoom(RoomRequest(room_id=room_id))
        return {
            "room_id": room.room_id,
            "name": room.name,
            "usernames": room.usernames
        }

    def send_message(self: Any, room_id: str, author_id: str, message: str) -> None:
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now(timezone.utc))
        msg = Message(
            message_id="",
            author_id=author_id,
            room_id=room_id,
            text=message,
            timestamp=timestamp
        )
        self.stub.SendMessage(msg)
        db.insert_message(author_id, msg.message_id, msg.author_id, msg.room_id, msg.text, datetime.fromtimestamp(msg.timestamp.seconds + msg.timestamp.nanos / 1e9))

    def get_new_messages(self: Any, username: str) -> None:
        for message in self.stub.GetMessages(UserRequest(username=username)):
            db.insert_message(username, message.message_id, message.author_id, message.room_id, message.text, datetime.fromtimestamp(message.timestamp.seconds + message.timestamp.nanos / 1e9))
