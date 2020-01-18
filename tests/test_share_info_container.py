from ms_srvs.structures.share_info_container import ShareInfo1Container, ShareInfo1, ShareType


class TestShareInfo1ContainerDeseralization:
    container, num_bytes = ShareInfo1Container.from_bytes(
        data=bytes.fromhex('05000000040002000500000008000200000000800c00020010000200000000801400020018000200000000001c00020020000200030000802400020028000200000000002c000200070000000000000007000000410044004d0049004e002400000000000d000000000000000d000000520065006d006f00740065002000410064006d0069006e000000000003000000000000000300000043002400000000000e000000000000000e000000440065006600610075006c00740020007300680061007200650000000b000000000000000b00000063006f006f006c005f007300680061007200650000000000010000000000000001000000000000000500000000000000050000004900500043002400000000000b000000000000000b000000520065006d006f00740065002000490050004300000000000600000000000000060000005500730065007200730000000100000000000000010000000000')
    )

    def test_num_bytes(self):
        assert self.num_bytes == 352

    def test_level(self):
        assert self.container.LEVEL == 1

    def test_entries_read(self):
        assert self.container.entries_read == 5

    def test_entries(self):

        assert self.container.entries[0] == ShareInfo1(
            netname='ADMIN$',
            share_type=ShareType(disktree=True, special=True),
            remark='Remote Admin'
        )

        assert self.container.entries[1] == ShareInfo1(
            netname='C$',
            share_type=ShareType(disktree=True, special=True),
            remark='Default share'
        )

        assert self.container.entries[2] == ShareInfo1(
            netname='cool_share',
            share_type=ShareType(disktree=True),
            remark=''
        )

        assert self.container.entries[3] == ShareInfo1(
            netname='IPC$',
            share_type=ShareType(ipc=True, special=True),
            remark='Remote IPC'
        )

        assert self.container.entries[4] == ShareInfo1(
            netname='Users',
            share_type=ShareType(disktree=True),
            remark=''
        )
