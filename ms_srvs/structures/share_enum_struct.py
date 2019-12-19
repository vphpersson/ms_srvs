from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from struct import unpack as struct_unpack, pack as struct_pack

from ms_srvs.structures.share_info_container import ShareInfoContainer, ShareInfo1Container

from rpc.ndr import NDRType, NDRUnion, Pointer


@dataclass
class ShareEnumStruct(NDRType):
    level: int
    share_info: ShareInfoContainer

    # TODO: Have the level be obtained in a property method (using an `Enum`?)

    @classmethod
    def from_bytes(cls, data: bytes) -> Tuple[ShareEnumStruct, int]:
        level: int = struct_unpack('<I', data[:4])[0]
        # TODO: Temporary.
        share_info, num_share_info_bytes = ShareInfo1Container.from_level_and_bytes(
            level=level,
            data=Pointer.from_bytes(data=NDRUnion.from_bytes(data=data[4:]).representation).representation
        )

        # level + union overhead + pointer overhead?
        return cls(level=level, share_info=share_info), 12 + num_share_info_bytes

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.level) + bytes(
            NDRUnion(
                tag=self.level,
                representation=Pointer(
                    representation=self.share_info
                )
            )
        )
