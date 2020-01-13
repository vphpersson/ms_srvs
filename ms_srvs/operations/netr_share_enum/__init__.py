from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Final, Type
from struct import pack as struct_pack, unpack as struct_unpack
from abc import ABC

from rpc.connection import Connection as RPCConnection
from rpc.ndr import Pointer, ConformantVaryingString
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response

from ms_srvs.operations import Operation
from ms_srvs.structures.share_enum_struct import ShareEnumStruct
from ms_srvs.structures.share_info_container import ShareInfoContainer


class NetrShareEnumRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.NETR_SHARE_ENUM


class NetrShareEnumResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[NetrShareEnumError]] = NetrShareEnumError


@dataclass
class NetrShareEnumRequest(NetrShareEnumRequestBase):
    level: int
    preferred_maximum_length: int = -1
    server_name: Optional[str] = None
    resume_handle: Optional[bytes] = None

    def __bytes__(self) -> bytes:
        server_name_bytes = bytes(
            Pointer(representation=ConformantVaryingString(representation=self.server_name or ''))
        )

        return b''.join([
            server_name_bytes,
            ((4 - (len(server_name_bytes) % 4)) % 4) * b'\x00',
            bytes(ShareEnumStruct(share_info=ShareInfoContainer.from_level_and_params(level=self.level))),
            struct_pack('<i', self.preferred_maximum_length),
            bytes(Pointer(representation=self.resume_handle or b'\x00\x00\x00\x00'))
        ])

    # TODO: Add a `from_bytes` method.


@dataclass
class NetrShareEnumResponse(NetrShareEnumResponseBase):
    info_struct: ShareEnumStruct
    total_entries: int
    resume_handle: bytes
    # TODO: Use enum.
    return_value: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> NetrShareEnumResponse:

        # TODO: Make this more concise.

        info_struct, num_info_struct_bytes = ShareEnumStruct.from_bytes(data=data)
        offset = num_info_struct_bytes

        total_entries = struct_unpack('<I', data[offset:offset+4])[0]
        offset += 4

        resume_handle = Pointer.from_bytes(data=data[offset:offset+8]).representation
        offset += len(resume_handle)

        return_value = data[offset:offset+4]

        return cls(
            info_struct=info_struct,
            total_entries=total_entries,
            resume_handle=resume_handle,
            return_value=return_value
        )


NetrShareEnumResponseBase.REQUEST_CLASS = NetrShareEnumRequest
NetrShareEnumRequestBase.RESPONSE_CLASS = NetrShareEnumResponse


async def netr_share_enum(
    rpc_connection: RPCConnection,
    request: NetrShareEnumRequest,
    raise_exception: bool = True
) -> NetrShareEnumRequest:
    """

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """
    
    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)

