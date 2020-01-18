from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, ClassVar
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode
from ndr.structures.pointer import Pointer, NullPointer
from ndr.structures.conformant_varying_string import ConformantVaryingString
from ndr.utils import pad as ndr_pad

from ms_srvs.operations import Operation
from ms_srvs.structures.share_enum_struct import ShareEnumStruct
from ms_srvs.structures.share_info_container import ShareInfoContainer


@dataclass
class NetrShareEnumRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.NETR_SHARE_ENUM

    level: int
    preferred_maximum_length: int = -1
    server_name: Optional[str] = None
    resume_handle: Optional[bytes] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> NetrShareEnumRequest:
        # TODO: Implement.
        raise NotImplementedError

    def __bytes__(self) -> bytes:
        server_name_bytes = bytes(
            Pointer(representation=ConformantVaryingString(representation=self.server_name or ''))
        )

        return b''.join([
            ndr_pad(server_name_bytes),
            bytes(ShareEnumStruct(share_info=ShareInfoContainer.from_level_and_params(level=self.level))),
            struct_pack('<i', self.preferred_maximum_length),
            bytes(Pointer(representation=self.resume_handle) if self.resume_handle else NullPointer())
        ])


@dataclass
class NetrShareEnumResponse(ClientProtocolResponseBase):
    info_struct: ShareEnumStruct
    total_entries: int
    resume_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> NetrShareEnumResponse:

        # TODO: Make this more concise.

        info_struct, num_info_struct_bytes = ShareEnumStruct.from_bytes(data=data)
        offset = num_info_struct_bytes

        total_entries = struct_unpack('<I', data[offset:offset+4])[0]
        offset += 4

        resume_handle = Pointer.from_bytes(data=data[offset:offset+8]).representation
        offset += len(resume_handle)

        return cls(
            info_struct=info_struct,
            total_entries=total_entries,
            resume_handle=resume_handle,
            return_code=Win32ErrorCode(struct_unpack('<I', data[offset:offset+4])[0])
        )

    def __bytes__(self) -> bytes:
        # TODO: Implement.
        raise NotImplementedError


NetrShareEnumResponse.REQUEST_CLASS = NetrShareEnumRequest
NetrShareEnumRequest.RESPONSE_CLASS = NetrShareEnumResponse


async def netr_share_enum(
    rpc_connection: RPCConnection,
    request: NetrShareEnumRequest,
    raise_exception: bool = True
) -> NetrShareEnumResponse:
    """
    Perform the NetrShareEnum operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """
    
    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)

