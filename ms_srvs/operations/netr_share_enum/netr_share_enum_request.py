from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class NetrShareEnumRequest:
    level: int
    preferred_maximum_length: int = -1
    server_name: Optional[str] = None
    resume_handle: Optional[bytes] = None

    def __bytes__(self) -> bytes:
        ...
        # return b''.join([
        #     bytes(
        #         Pointer(
        #             referent_id=token_bytes(nbytes=4),
        #             representation=ConformantVaryingString(
        #                 representation=self.server_name
        #             )
        #         ),
        #     ),
        #     # TODO: Add padding.
        #     bytes(
        #         ShareEnumStruct()
        #     )
        #
        #
        #     struct_pack('<i', self.preferred_maximum_length),
        #     bytes(
        #         Pointer(
        #             referent_id=token_bytes(nbytes=4),
        #             representation=self.resume_handle or b'\x00\x00\x00\x00'
        #         )
        #     )
        # ])
