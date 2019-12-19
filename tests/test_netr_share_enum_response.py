from ms_srvs.operations.netr_share_enum.netr_share_enum_response import NetrShareEnumResponse
from ms_srvs.structures.share_enum_struct import ShareEnumStruct


class TestResponseDeserialization1:
    response = NetrShareEnumResponse.from_bytes(
        data=bytes.fromhex(
            '01000000010000000000020005000000040002000500000008000200000000800c00020010000200000000801400020018000200000000001c00020020000200030000802400020028000200000000002c000200070000000000000007000000410044004d0049004e002400000000000d000000000000000d000000520065006d006f00740065002000410064006d0069006e000000000003000000000000000300000043002400000000000e000000000000000e000000440065006600610075006c00740020007300680061007200650000000b000000000000000b00000063006f006f006c005f007300680061007200650000000000010000000000000001000000000000000500000000000000050000004900500043002400000000000b000000000000000b000000520065006d006f00740065002000490050004300000000000600000000000000060000005500730065007200730000000100000000000000010000000000000005000000300002000000000000000000'
        )
    )

    def test_total_entries(self):
        assert self.response.total_entries == 5

    def test_resume_handle(self):
        assert self.response.resume_handle == b'\x00\x00\x00\x00'

    def test_return_value(self):
        assert self.response.return_value == b'\x00\x00\x00\x00'

    def test_info_struct_type(self):
        assert isinstance(self.response.info_struct, ShareEnumStruct)
