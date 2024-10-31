from datetime import datetime

import grpc
from proto_gen.chat import message_pb2
from proto_gen.chat import room_pb2
from proto_gen.chat import user_pb2
from proto_gen.chat import service_pb2
from proto_gen.chat import service_pb2_grpc
from google.protobuf import timestamp_pb2

import db as db

channel = grpc.insecure_channel('localhost:3000')
stub = service_pb2_grpc.ServiceStub(channel)

def get_username() -> str:
    result = db.get_username()
    return result if result else None

def signup(username: str) -> None:
    stub.CreateUser(user_pb2.User(username=username, password="", room_ids=[]))
    db.set_username(username)

def get_rooms(username: str = db.get_username()) -> list:
    return [
        room for room in stub.GetUser(service_pb2.UserRequest(username=username)).room_ids
    ]

def create_room(room_name: str) -> None:
    stub.CreateRoom(room_pb2.Room(room_id="", name=room_name, user_ids=[get_username()]))

def invite_user(room_id: str, username: str) -> None:
    room = stub.GetRoom(service_pb2.RoomRequest(room_id=room_id))
    stub.JoinRoom(service_pb2.JoinRoomRequest(room_id=room.room_id, user_id=username))

def send_message(room_id: str, message: str) -> None:
    msg = message_pb2.Message(
        message_id="",
        author_id=db.get_username(),
        room_id=room_id,
        text=message,
        timestamp=timestamp_pb2.Timestamp().FromDatetime(datetime.now())
    )
    stub.SendMessage(msg)
    db.insert_message(msg.message_id, msg.author_id, msg.room_id, msg.text, datetime.fromtimestamp(msg.timestamp.seconds + msg.timestamp.nanos/1e9))

def join_room(room_id: str, username: str = db.get_username()) -> None:
    room = stub.GetRoom(service_pb2.RoomRequest(room_id=room_id)) # TODO: search in local db
    stub.JoinRoom(service_pb2.JoinRoomRequest(room_id=room.room_id, user_id=username))
    # db.join_room(room.room_id)

async def get_new_messages(room_id: str) -> None:
    for message in stub.GetMessages(service_pb2.UserRequest(username=db.get_username())):
        db.insert_message(message.message_id, message.author_id, room_id, message.text, message.timestamp)


#
# stub.CreateUser(user_pb2.User())

# user = stub.GetUser(user_pb2.User())

# stub.CreateRoom(room_pb2.Room())

# stub.JoinRoom(service_pb2.JoinRoomRequest())

# room = stub.GetRoom(room_pb2.Room())

# stub.SendMessage(message_pb2.Message())

# for message in stub.GetMessages(message_pb2.Message()):
#     pass
