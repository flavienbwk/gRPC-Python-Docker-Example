# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: image_transform.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='image_transform.proto',
  package='flavienbwk',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15image_transform.proto\x12\nflavienbwk\";\n\x0bsourceImage\x12\r\n\x05image\x18\x01 \x01(\x0c\x12\r\n\x05width\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x05\"!\n\x10transformedImage\x12\r\n\x05image\x18\x01 \x01(\x0c\x32U\n\rEncodeService\x12\x44\n\tGetEncode\x12\x17.flavienbwk.sourceImage\x1a\x1c.flavienbwk.transformedImage\"\x00\x62\x06proto3'
)




_SOURCEIMAGE = _descriptor.Descriptor(
  name='sourceImage',
  full_name='flavienbwk.sourceImage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='flavienbwk.sourceImage.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='width', full_name='flavienbwk.sourceImage.width', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='flavienbwk.sourceImage.height', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=96,
)


_TRANSFORMEDIMAGE = _descriptor.Descriptor(
  name='transformedImage',
  full_name='flavienbwk.transformedImage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='flavienbwk.transformedImage.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=131,
)

DESCRIPTOR.message_types_by_name['sourceImage'] = _SOURCEIMAGE
DESCRIPTOR.message_types_by_name['transformedImage'] = _TRANSFORMEDIMAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

sourceImage = _reflection.GeneratedProtocolMessageType('sourceImage', (_message.Message,), {
  'DESCRIPTOR' : _SOURCEIMAGE,
  '__module__' : 'image_transform_pb2'
  # @@protoc_insertion_point(class_scope:flavienbwk.sourceImage)
  })
_sym_db.RegisterMessage(sourceImage)

transformedImage = _reflection.GeneratedProtocolMessageType('transformedImage', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFORMEDIMAGE,
  '__module__' : 'image_transform_pb2'
  # @@protoc_insertion_point(class_scope:flavienbwk.transformedImage)
  })
_sym_db.RegisterMessage(transformedImage)



_ENCODESERVICE = _descriptor.ServiceDescriptor(
  name='EncodeService',
  full_name='flavienbwk.EncodeService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=133,
  serialized_end=218,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetEncode',
    full_name='flavienbwk.EncodeService.GetEncode',
    index=0,
    containing_service=None,
    input_type=_SOURCEIMAGE,
    output_type=_TRANSFORMEDIMAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ENCODESERVICE)

DESCRIPTOR.services_by_name['EncodeService'] = _ENCODESERVICE

# @@protoc_insertion_point(module_scope)