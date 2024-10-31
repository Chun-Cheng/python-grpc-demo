from google.protobuf import empty_pb2 as _empty_pb2
from chat import message_pb2 as _message_pb2
from chat import room_pb2 as _room_pb2
from chat import user_pb2 as _user_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class UserRequest(_message.Message):
    __slots__ = ('username',)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str

    def __init__(self, username: _Optional[str]=...) -> None:
        ...

class RoomRequest(_message.Message):
    __slots__ = ('room_id',)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str

    def __init__(self, room_id: _Optional[str]=...) -> None:
        ...

class JoinRoomRequest(_message.Message):
    __slots__ = ('room_id', 'user_id')
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    user_id: str

    def __init__(self, room_id: _Optional[str]=..., user_id: _Optional[str]=...) -> None:
        ...