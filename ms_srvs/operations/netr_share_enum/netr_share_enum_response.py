from __future__ import annotations
from dataclasses import dataclass
from struct import unpack as struct_unpack

from ms_srvs.operations.netr_share_enum import NetrShareEnumMessage
from ms_srvs.structures.share_enum_struct import ShareEnumStruct

from rpc.ndr import Pointer


@dataclass
class NetrShareEnumResponse(NetrShareEnumMessage):
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
