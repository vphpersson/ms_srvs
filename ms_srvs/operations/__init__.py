from enum import IntEnum
from abc import ABC


class Operation(IntEnum):
    OPNUM0_NOT_USED_ON_WIRE = 0
    OPNUM1_NOT_USED_ON_WIRE = 1
    OPNUM2_NOT_USED_ON_WIRE = 2
    OPNUM3_NOT_USED_ON_WIRE = 3
    OPNUM4_NOT_USED_ON_WIRE = 4
    OPNUM5_NOT_USED_ON_WIRE = 5
    OPNUM6_NOT_USED_ON_WIRE = 6
    OPNUM7_NOT_USED_ON_WIRE = 7
    NETR_CONNECTION_ENUM = 8
    NETR_FILE_ENUM = 9
    NETR_FILE_GET_INFO = 10
    NETR_FILE_CLOSE = 11
    NETR_SESSION_ENUM = 12
    NETR_SESSION_DEL = 13
    NETR_SHARE_ADD = 14
    NETR_SHARE_ENUM = 15
    NETR_SHARE_GET_INFO = 16
    NETR_SHARE_SET_INFO = 17
    NETR_SHARE_DEL = 18
    NETR_SHARE_DEL_STICKY = 19
    NETR_SHARE_CHECK = 20
    NETR_SERVER_GET_INFO = 21
    NETR_SERVER_SET_INFO = 22
    NETR_SERVER_DISK_ENUM = 23
    NETR_SERVER_STATISTICS_GET = 24
    NETR_SERVER_TRANSPORT_ADD = 25
    NETR_SERVER_TRANSPORT_ENUM = 26
    NETR_SERVER_TRANSPORT_DEL = 27
    NETR_REMOTE_TOD = 28
    OPNUM29_NOT_USED_ON_WIRE = 29
    NETPR_PATH_TYPE = 30
    NETPR_PATH_CANONICALIZE = 31
    NETPR_PATH_COMPARE = 32
    NETPR_NAME_VALIDATE = 33
    NETPR_NAME_CANONICALIZE = 34
    NETPR_NAME_COMPARE = 35
    NETR_SHARE_ENUM_STICKY = 36
    NETR_SHARE_DEL_START = 37
    NETR_SHARE_DEL_COMMIT = 38
    NETRP_GET_FILE_SECURITY = 39
    NETRP_SET_FILE_SECURITY = 40
    NETR_SERVER_TRANSPORT_ADD_EX = 41
    OPNUM42_NOT_USED_ON_WIRE = 42
    NETR_DFS_GET_VERSION = 43
    NETR_DFS_CREATE_LOCAL_PARTITION = 44
    NETR_DFS_DELETE_LOCAL_PARTITION = 45
    NETR_DFS_SET_LOCAL_VOLUME_STATE = 46
    OPNUM47_NOT_USED_ON_WIRE = 47
    NETR_DFS_CREATE_EXIT_POINT = 48
    NETR_DFS_DELETE_EXIT_POINT = 49
    NETR_DFS_MODIFY_PREFIX = 50
    NETR_DFS_FIX_LOCAL_VOLUME = 51
    NETR_DFS_MANAGER_REPORT_SITE_INFO = 52
    NETR_SERVER_TRANSPORT_DEL_EX = 53
    NETR_SERVER_ALIAS_ADD = 54
    NETR_SERVER_ALIAS_ENUM = 55
    NETR_SERVER_ALIAS_DEL = 56
    NETR_SHARE_DEL_EX = 57


class MsSrvsMessage(ABC):
    operation: Operation = NotImplemented
