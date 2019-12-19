from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from struct import unpack as struct_unpack, pack as struct_pack

from ms_srvs.structures.share_info_container import ShareInfoContainer

from rpc.ndr import NDRType, NDRUnion, Pointer


@dataclass
class ShareEnumStruct(NDRType):
    share_info: ShareInfoContainer

    # TODO: Have the level be obtained in a property method (using an `Enum`?)

    @property
    def level(self) -> int:
        return self.share_info.level

    @classmethod
    def from_bytes(cls, data: bytes) -> Tuple[ShareEnumStruct, int]:
        share_info, num_share_info_bytes = ShareInfoContainer.from_level_and_bytes(
            level=struct_unpack('<I', data[:4])[0],
            data=Pointer.from_bytes(data=NDRUnion.from_bytes(data=data[4:]).representation).representation
        )

        # level + union overhead + pointer overhead?
        return cls(share_info=share_info), 12 + num_share_info_bytes

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.level) + bytes(
            NDRUnion(
                tag=self.level,
                representation=Pointer(
                    representation=self.share_info
                )
            )
        )
