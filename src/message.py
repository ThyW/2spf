#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import List, Union
from .link_state import *


class MessageType(Enum):
    HELLO = 1
    DD = 2
    LSR = 3
    LSU = 4
    LSA= 5


@dataclass
class MessageHeader:
    version: int        # used
    type: int           # used
    length: int         # not used, no message checking and verifing is done, 0
    router_id: int      # used
    area_id: int        # not used, we only work on a single area, always 0
    checksum: int       # 0, not used
    auth_type: int      # not auth is used, 0
    auth: int           # n password is used, 0


@dataclass
class HelloMessage(MessageHeader):
    net_mask: int               # not used
    options: int                # present, but not used
    priority: int               # used
    router_dead_interval: int   # not used
    dr: int                     # used
    bdr: int                    # used
    neighbors: List[int]        # used


@dataclass
class DatabaseDescription(MessageHeader):
    options: int
    init_b: bool
    more_b: bool
    ms_sl_b: bool
    dd_seq_num: int
    ls_headers: List[LSAHeader]


@dataclass
class LSRequest(MessageHeader):
    ls_type: int
    ls_id: int
    advertising_router: int


@dataclass
class LSUpdate(MessageHeader):
    num_advertisements: int
    advertisements: List[LinkStateAdvertisement]


@dataclass
class LSAck(MessageHeader):
    acks: List[LSAHeader]


RouterMessage = Union[HelloMessage,
                      DatabaseDescription,
                      LSUpdate,
                      LSRequest,
                      LSAck]
