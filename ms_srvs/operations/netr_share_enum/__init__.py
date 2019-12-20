from typing import Final

from .netr_share_enum_request import *
from .netr_share_enum_response import *
from ms_srvs.operations import MsSrvsMessage, Operation
from ms_srvs.operations.netr_share_enum import NetrShareEnumRequest, NetrShareEnumResponse

from rpc.connection import Connection as RPCConnection
from rpc.pdu_headers.request_header import RequestHeader


class NetrShareEnumMessage(MsSrvsMessage):
    operation: Final[Operation] = Operation.NETR_SHARE_ENUM


async def netr_share_enum(
    rpc_connection: RPCConnection,
    netr_share_enum_request: NetrShareEnumRequest
) -> NetrShareEnumResponse:

    # TODO: The RPC connection will need to make sure that I get the proper response. `assoc_group` + `call_id`?
    #   Use the same `Future`-based approach as is used with SMB => done inside the RPC connection.

    # TODO: Use a `send_message` method instead.
    await rpc_connection.write(
        bytes(
            RequestHeader(
                opnum=NetrShareEnumRequest.operation.value,
                stub_data=bytes(netr_share_enum_request)
            )
        )
    )

