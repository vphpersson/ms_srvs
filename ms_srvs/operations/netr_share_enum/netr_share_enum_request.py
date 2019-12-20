from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from struct import pack as struct_pack

from ms_srvs.operations.netr_share_enum import NetrShareEnumMessage
from ms_srvs.structures.share_enum_struct import ShareEnumStruct
from ms_srvs.structures.share_info_container import ShareInfoContainer

from rpc.ndr import Pointer, ConformantVaryingString


@dataclass
class NetrShareEnumRequest(NetrShareEnumMessage):
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
