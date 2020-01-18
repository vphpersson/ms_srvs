from enum import IntFlag
from msdsalgs.utils import Mask


class ShareTypeFlag(IntFlag):
    STYPE_DISKTREE = 0x00000000
    STYPE_PRINTQ = 0x00000001
    STYPE_DEVICE = 0x00000002
    STYPE_IPC = 0x00000003
    STYPE_CLUSTER_FS = 0x02000000
    STYPE_CLUSTER_SOFS = 0x04000000
    STYPE_CLUSTER_DFS = 0x08000000
    STYPE_SPECIAL = 0x80000000
    STYPE_TEMPORARY = 0x40000000


ShareType = Mask.make_class(
    int_flag_class=ShareTypeFlag,
    prefix='STYPE_'
)
