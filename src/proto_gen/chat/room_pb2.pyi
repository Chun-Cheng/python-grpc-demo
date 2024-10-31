from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Room(_message.Message):
    __slots__ = ('room_id', 'name', 'user_ids')
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    name: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, room_id: _Optional[str]=..., name: _Optional[str]=..., user_ids: _Optional[_Iterable[str]]=...) -> None:
        ...