from typing import Final

from ms_srvs.operations import Operation, MsSrvsMessage


class NetrShareEnumMessage(MsSrvsMessage):
    operation: Final[Operation] = Operation.NETR_SHARE_ENUM
