from uuid import UUID
from typing import Final

from rpc.structures.presentation_syntax import PresentationSyntax

MS_SRVS_ABSTRACT_SYNTAX: Final[PresentationSyntax] = PresentationSyntax(
    if_uuid=UUID('4b324fc8-1670-01d3-1278-5a47bf6ee188'),
    if_version=3
)
