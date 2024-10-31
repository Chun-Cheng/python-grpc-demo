import asyncio
import logging
from datetime import datetime
from typing import Any

import grpc
from proto_gen.chat import message_pb2
from proto_gen.chat import room_pb2
from proto_gen.chat import user_pb2
from proto_gen.chat import service_pb2
from proto_gen.chat import service_pb2_grpc

from google.protobuf import empty_pb2
# from google.protobuf.timestamp_pb2 import Timestamp

import db as db


class ServiceServicer(service_pb2_grpc.ServiceServicer):
    def CreateUser(self: Any, request: service_pb2.UserRequest, unused_context) -> empty_pb2.Empty:
        logging.info(f"Creating user {request.username}")
        db.new_user(request.username, "")
        return empty_pb2.Empty()

    def GetUser(self: Any, request: service_pb2.UserRequest, unused_context) -> user_pb2.User:
        logging.info(f"Getting user {request.username}")
        user = db.get_user(request.username)
        return user_pb2.User(username=user["username"], password="", room_ids=user["rooms"])
        return user_pb2.User(
            username="test_user_1", 
            password="", 
            room_ids=["test_room"]
        )

    def CreateRoom(self: Any, request: room_pb2.Room, unused_context) -> empty_pb2.Empty:
        logging.info(f"Creating room {request.name}")
        db.new_room(request.name, request.user_ids[0])
        return empty_pb2.Empty()
    
    def JoinRoom(self: Any, request: service_pb2.JoinRoomRequest, unused_context) -> empty_pb2.Empty:
        logging.info(f"Joining room {request.room_id}")
        db.join_room(request.user_id, request.room_id)
        return empty_pb2.Empty()

    def GetRoom(self: Any, request: service_pb2.RoomRequest, unused_context) -> room_pb2.Room:
        logging.info(f"Getting room {request.room_id}")
        room = db.get_room(request.room_id)
        return room_pb2.Room(room_id=room["room_id"], name=room["name"], user_ids=room["user_id"])
        return room_pb2.Room(
            room_id="test_room_id", 
            name="test_room", 
            user_ids=["test_user_1", "test_user_2"]
        )

    def SendMessage(self: Any, request: message_pb2.Message, unused_context) -> empty_pb2.Empty:
        logging.info("Sending message")
        server_time = datetime.now()
        user_timestamp = request.timestamp
        user_time = datetime.fromtimestamp(user_timestamp.seconds + user_timestamp.nanos/1e9)
        # compare user_time and server_time
        if user_time < server_time and (server_time - user_time).total_seconds() < 0.5:
            msg_time = user_time
        else:
            msg_time = server_time

        db.new_message(request.author_id, request.room_id, request.text, msg_time)
        return empty_pb2.Empty()

    async def GetMessages(self: Any, request: service_pb2.UserRequest, unused_context):
        # get user new messages
        while True:
            for message in db.get_user_messages(request.username):
                logging.info(f"Sending message {message['msg_id']}")
                yield message_pb2.Message(
                    message_id=message["msg_id"], 
                    author_id=message["author_user_id"], 
                    room_id=message["room_id"], 
                    text=message["message"], 
                    timestamp=message["timestamp"]
                )
            await asyncio.sleep(0.1)


async def serve() -> None:
    db.init_db()
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()
    service_pb2_grpc.add_ServiceServicer_to_server(ServiceServicer(), server)
    server.add_insecure_port("[::]:3000")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
