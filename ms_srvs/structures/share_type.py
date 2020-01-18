from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from abc import ABC
from typing import Dict, Type, ClassVar


class ShareTypeEnum(IntEnum):
    STYPE_DISKTREE = 0x00000000
    STYPE_PRINTQ = 0x00000001
    STYPE_DEVICE = 0x00000002
    STYPE_IPC = 0x00000003
    STYPE_CLUSTER_FS = 0x02000000
    STYPE_CLUSTER_SOFS = 0x04000000
    STYPE_CLUSTER_DFS = 0x08000000


class ShareTypeCharacteristicsFlag(IntFlag):
    STYPE_SPECIAL = 0x80000000
    STYPE_TEMPORARY = 0x40000000


@dataclass
class ShareType(ABC):
    ENUM_VALUE: ClassVar[ShareTypeEnum] = NotImplemented
    DESCRIPTION: ClassVar[str] = NotImplemented
    ENUM_VALUE_TO_CLASS: ClassVar[Dict[ShareTypeEnum, Type[ShareType]]] = {}

    is_special: bool
    is_temporary: bool

    @classmethod
    def from_int(cls, value: int) -> ShareType:
        characteristics_flag = ShareTypeCharacteristicsFlag(value & 0xF0000000)
        is_special = ShareTypeCharacteristicsFlag.STYPE_SPECIAL in characteristics_flag
        is_temporary = ShareTypeCharacteristicsFlag.STYPE_TEMPORARY in characteristics_flag

        share_type_enum = ShareTypeEnum(value & 0x0FFFFFFF)

        if cls != ShareType:
            if share_type_enum is not cls.ENUM_VALUE:
                # TODO: Use proper exception.
                raise ValueError
            return cls(is_special=is_special, is_temporary=is_temporary)
        else:
            return cls.ENUM_VALUE_TO_CLASS[share_type_enum](is_special=is_special, is_temporary=is_temporary)

    def __int__(self) -> int:
        return int(self.ENUM_VALUE) \
           | (ShareTypeCharacteristicsFlag.STYPE_SPECIAL.value if self.is_special else 0) \
           | (ShareTypeCharacteristicsFlag.STYPE_TEMPORARY.value if self.is_temporary else 0)

    def __str__(self) -> str:

        characteristics_list = []
        if self.is_special:
            characteristics_list.append('special')
        if self.is_temporary:
            characteristics_list.append('temporary')

        return f'{self.DESCRIPTION} {("(" + ", ".join(characteristics_list) + ")") if characteristics_list else ""}'


class DiskTree(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_DISKTREE
    DESCRIPTION = 'Disk drive'


class PrintQueue(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_PRINTQ
    DESCRIPTION = 'Print queue'


class Device(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_DEVICE
    DESCRIPTION = 'Communication device'


class IPC(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_IPC
    DESCRIPTION = 'Interprocess communication'


class ClusterFS(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_CLUSTER_FS
    DESCRIPTION = 'A cluster share'


class ClusterSOFS(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_CLUSTER_SOFS
    DESCRIPTION = 'A Scale-Out cluster share'


class ClusterDFS(ShareType):
    ENUM_VALUE = ShareTypeEnum.STYPE_CLUSTER_DFS
    DESCRIPTION = 'A DFS share in a cluster'


ShareType.ENUM_VALUE_TO_CLASS = {
    ShareTypeEnum.STYPE_DISKTREE: DiskTree,
    ShareTypeEnum.STYPE_PRINTQ: PrintQueue,
    ShareTypeEnum.STYPE_DEVICE: Device,
    ShareTypeEnum.STYPE_IPC: IPC,
    ShareTypeEnum.STYPE_CLUSTER_FS: ClusterFS,
    ShareTypeEnum.STYPE_CLUSTER_SOFS: ClusterSOFS,
    ShareTypeEnum.STYPE_CLUSTER_DFS: ClusterDFS
}
