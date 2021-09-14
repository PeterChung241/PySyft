# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/action/get_set_static_attribute.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# relative
from ....common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from ....io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2
from ....pointer import pointer_pb2 as proto_dot_core_dot_pointer_dot_pointer__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/common/action/get_set_static_attribute.proto",
    package="syft.core.node.common.action",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n<proto/core/node/common/action/get_set_static_attribute.proto\x12\x1csyft.core.node.common.action\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto\x1a proto/core/pointer/pointer.proto"\xe6\x01\n\x1bGetSetStaticAttributeAction\x12\x0c\n\x04path\x18\x01 \x01(\t\x12+\n\x07set_arg\x18\x02 \x01(\x0b\x32\x1a.syft.core.pointer.Pointer\x12-\n\x0eid_at_location\x18\x03 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address\x12%\n\x06msg_id\x18\x05 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x0e\n\x06\x61\x63tion\x18\x06 \x01(\x05\x62\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_io_dot_address__pb2.DESCRIPTOR,
        proto_dot_core_dot_pointer_dot_pointer__pb2.DESCRIPTOR,
    ],
)


_GETSETSTATICATTRIBUTEACTION = _descriptor.Descriptor(
    name="GetSetStaticAttributeAction",
    full_name="syft.core.node.common.action.GetSetStaticAttributeAction",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="path",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.path",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="set_arg",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.set_arg",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="id_at_location",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.id_at_location",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.address",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.msg_id",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="action",
            full_name="syft.core.node.common.action.GetSetStaticAttributeAction.action",
            index=5,
            number=6,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=197,
    serialized_end=427,
)

_GETSETSTATICATTRIBUTEACTION.fields_by_name[
    "set_arg"
].message_type = proto_dot_core_dot_pointer_dot_pointer__pb2._POINTER
_GETSETSTATICATTRIBUTEACTION.fields_by_name[
    "id_at_location"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_GETSETSTATICATTRIBUTEACTION.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_io_dot_address__pb2._ADDRESS
_GETSETSTATICATTRIBUTEACTION.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
DESCRIPTOR.message_types_by_name[
    "GetSetStaticAttributeAction"
] = _GETSETSTATICATTRIBUTEACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetSetStaticAttributeAction = _reflection.GeneratedProtocolMessageType(
    "GetSetStaticAttributeAction",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETSETSTATICATTRIBUTEACTION,
        "__module__": "proto.core.node.common.action.get_set_static_attribute_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.action.GetSetStaticAttributeAction)
    },
)
_sym_db.RegisterMessage(GetSetStaticAttributeAction)


# @@protoc_insertion_point(module_scope)
