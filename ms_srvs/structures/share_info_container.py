from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC
from typing import Tuple, ClassVar, List
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.ndr import NDRType, Pointer, ConformantVaryingString


@dataclass
class ShareInfo1:
    shi1_netname: str
    shi1_type: int
    shi1_remark: str


@dataclass
class ShareInfoContainer(NDRType, ABC):

    @classmethod
    def from_level_and_bytes(cls, level: int, data: bytes) -> Tuple[ShareInfoContainer, int]:
        if level == 1:
            return ShareInfo1Container.from_bytes(data=data)
        else:
            raise ValueError


@dataclass
class ShareInfo1Container(ShareInfoContainer):
    level: ClassVar[int] = 1

    entries: Tuple[ShareInfo1, ...] = field(default_factory=tuple)

    @property
    def entries_read(self) -> int:
        return len(self.entries)

    @classmethod
    def from_bytes(cls, data: bytes) -> Tuple[ShareInfo1Container, int]:
        entries_read: int = struct_unpack('<I', data[:4])[0]
        pointer_data = Pointer.from_bytes(data[4:]).representation
        max_count = struct_unpack('<I', pointer_data[:4])

        offset = 4
        entry_share_type_list: List[int] = []
        for i in range(entries_read):
            entry_share_type_list.append(struct_unpack('>I', pointer_data[offset + 4:offset + 8])[0])
            offset += 12

        entries: List[ShareInfo1] = []
        for i in range(entries_read):
            netname_cvs = ConformantVaryingString.from_bytes(data=pointer_data[offset:])
            offset += len(netname_cvs) + (4 - (len(netname_cvs) % 4)) % 4
            remark_cvs = ConformantVaryingString.from_bytes(pointer_data[offset:])
            offset += len(remark_cvs) + (4 - (len(remark_cvs) % 4)) % 4

            entries.append(
                ShareInfo1(
                    shi1_netname=netname_cvs.representation,
                    shi1_type=entry_share_type_list[i],
                    shi1_remark=remark_cvs.representation
                )
            )

        return cls(entries=tuple(entries)), 8 + offset

    def __bytes__(self) -> bytes:
        fixed_part: bytes = b''
        variable_part: bytes = b''
        for entry in self.entries:
            netname_pointer = Pointer(representation=ConformantVaryingString(representation=entry.shi1_netname))
            share_type = entry.shi1_type
            remark_pointer = Pointer(representation=ConformantVaryingString(representation=entry.shi1_remark))

            fixed_part += b''.join([
                struct_pack('<I', netname_pointer.referent_id),
                struct_pack('<I', share_type),
                struct_pack('<I', remark_pointer.referent_id)
            ])

            netname_bytes: bytes = bytes(netname_pointer.representation)
            remark_bytes: bytes = bytes(remark_pointer.representation)

            variable_part += b''.join([
                netname_bytes + b'\x00' * (4 - (len(netname_bytes) % 4)) % 4,
                remark_bytes + b'\x00' * (4 - (len(remark_bytes) % 4)) % 4
            ])

        return b''.join([
            struct_pack('<I', self.entries_read),
            bytes(
                Pointer(
                    representation=b''.join([fixed_part, variable_part]) or b'\x00\x00\x00\x00'
                )
            )
        ])