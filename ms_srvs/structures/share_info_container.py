from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Tuple, ClassVar, List, Dict, Type, Any
from struct import pack as struct_pack, unpack as struct_unpack

from ndr.structures.pointer import Pointer
from ndr.structures.conformant_varying_string import ConformantVaryingString
from ndr.structures import NDRType
from ndr.utils import pad as ndr_pad, calculate_pad_length

from ms_srvs.structures.share_type import ShareType


@dataclass
class ShareInfo1:
    netname: str
    share_type: ShareType
    remark: str


@dataclass
class ShareInfoContainer(NDRType, ABC):
    LEVEL: ClassVar[int] = NotImplemented
    LEVEL_TO_CLASS: ClassVar[Dict[int, Type[ShareInfoContainer]]] = {}

    @classmethod
    def from_level_and_params(cls, level: int, **params: Dict[str, Any]) -> ShareInfoContainer:
        return cls.LEVEL_TO_CLASS[level](**params)

    @classmethod
    def from_level_and_bytes(cls, level: int, data: bytes) -> Tuple[ShareInfoContainer, int]:
        if cls != ShareInfoContainer:
            if level != cls.LEVEL:
                # TODO: Use proper exception.
                raise ValueError
            return cls.from_bytes(data=data)
        else:
            return cls.LEVEL_TO_CLASS[level].from_bytes(data=data)

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Tuple[ShareInfoContainer, int]:
        raise NotImplementedError


@dataclass
class ShareInfo1Container(ShareInfoContainer):
    LEVEL: ClassVar[int] = 1

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
        entry_share_type_list: List[ShareType] = []
        for _ in range(entries_read):
            entry_share_type_list.append(
                ShareType.from_int(struct_unpack('<I', pointer_data[offset+4:offset+8])[0])
            )
            offset += 12

        entries: List[ShareInfo1] = []
        for i in range(entries_read):
            netname_cvs = ConformantVaryingString.from_bytes(data=pointer_data[offset:])
            offset += calculate_pad_length(len(netname_cvs))
            remark_cvs = ConformantVaryingString.from_bytes(pointer_data[offset:])
            offset += calculate_pad_length(len(remark_cvs))

            entries.append(
                ShareInfo1(
                    netname=netname_cvs.representation,
                    share_type=entry_share_type_list[i],
                    remark=remark_cvs.representation
                )
            )

        return cls(entries=tuple(entries)), 8 + offset

    def __bytes__(self) -> bytes:
        fixed_part: bytes = b''
        variable_part: bytes = b''
        for entry in self.entries:
            netname_pointer = Pointer(representation=ConformantVaryingString(representation=entry.netname))
            remark_pointer = Pointer(representation=ConformantVaryingString(representation=entry.remark))

            fixed_part += b''.join([
                struct_pack('<I', netname_pointer.referent_id),
                struct_pack('<I', int(entry.share_type)),
                struct_pack('<I', remark_pointer.referent_id)
            ])

            variable_part += b''.join([
                ndr_pad(bytes(netname_pointer.representation)),
                ndr_pad(bytes(remark_pointer.representation))
            ])

        return b''.join([
            struct_pack('<I', self.entries_read),
            b''.join([fixed_part, variable_part]) or b'\x00\x00\x00\x00'
        ])


ShareInfoContainer.LEVEL_TO_CLASS = {
    1: ShareInfo1Container
}
