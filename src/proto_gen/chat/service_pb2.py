"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 27, 2, '', 'chat/service.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ..chat import message_pb2 as chat_dot_message__pb2
from ..chat import room_pb2 as chat_dot_room__pb2
from ..chat import user_pb2 as chat_dot_user__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12chat/service.proto\x12\x04chat\x1a\x1bgoogle/protobuf/empty.proto\x1a\x12chat/message.proto\x1a\x0fchat/room.proto\x1a\x0fchat/user.proto"\x1f\n\x0bUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t"\x1e\n\x0bRoomRequest\x12\x0f\n\x07room_id\x18\x01 \x01(\t"4\n\x0fJoinRoomRequest\x12\x0f\n\x07room_id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t2\xfa\x02\n\x07Service\x129\n\nCreateUser\x12\x11.chat.UserRequest\x1a\x16.google.protobuf.Empty"\x00\x12*\n\x07GetUser\x12\x11.chat.UserRequest\x1a\n.chat.User"\x00\x122\n\nCreateRoom\x12\n.chat.Room\x1a\x16.google.protobuf.Empty"\x00\x12;\n\x08JoinRoom\x12\x15.chat.JoinRoomRequest\x1a\x16.google.protobuf.Empty"\x00\x12*\n\x07GetRoom\x12\x11.chat.RoomRequest\x1a\n.chat.Room"\x00\x126\n\x0bSendMessage\x12\r.chat.Message\x1a\x16.google.protobuf.Empty"\x00\x123\n\x0bGetMessages\x12\x11.chat.UserRequest\x1a\r.chat.Message"\x000\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat.service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_USERREQUEST']._serialized_start = 111
    _globals['_USERREQUEST']._serialized_end = 142
    _globals['_ROOMREQUEST']._serialized_start = 144
    _globals['_ROOMREQUEST']._serialized_end = 174
    _globals['_JOINROOMREQUEST']._serialized_start = 176
    _globals['_JOINROOMREQUEST']._serialized_end = 228
    _globals['_SERVICE']._serialized_start = 231
    _globals['_SERVICE']._serialized_end = 609