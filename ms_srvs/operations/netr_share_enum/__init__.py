from .netr_share_enum_request import *
from .netr_share_enum_response import *

from rpc.connection import Connection as RPCConnection
from rpc.pdu_headers.base import MSRPCHeader
from rpc.pdu_headers.request_header import RequestHeader
from rpc.pdu_headers.response_header import ResponseHeader


async def netr_share_enum(rpc_connection: RPCConnection, request: NetrShareEnumRequest) -> NetrShareEnumResponse:
    """

    :param rpc_connection:
    :param request:
    :return:
    """

    response_message: MSRPCHeader = await (
        await rpc_connection.send_message(
            RequestHeader(
                opnum=NetrShareEnumRequest.operation.value,
                stub_data=bytes(request)
            )
        )
    )

    if not isinstance(response_message, ResponseHeader):
        # TODO: Use proper exception.
        raise ValueError

    return NetrShareEnumResponse.from_bytes(data=response_message.stub_data)

