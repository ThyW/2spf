#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class LSType(Enum):
    ROUTER = 1
    NETWORK_LINKS = 2
    SUMMARY_LINK_IP = 3
    SUMMARY_LINK_ASBR = 4
    AS_EXTERNAL_LINK = 5


@dataclass
class LSAHeader:
    ls_age: int  # ignore
    options: int # router options, can be filled but are ignored
    ls_type: int # always 1
    ls_id: int   # router id
    advertising_router: int # router id
    ls_seq_num: int # increment from 0
    ls_checksum: int # ignore
    length: int # ignore


@dataclass
class RLABody:
    link_id: int # router id of the router that is being linked to
    link_data: int # ifIndex of the router
    num_tos_metrics: int # 0
    tos_zero: int # link cost
    tos_and_metric: Dict[int, int] # ignore


@dataclass
class RouterLinkAdvertisement(LSAHeader):
    v_b: bool # ignore
    e_b: bool # ignore
    b_b: bool # ignore
    num_links: int # number of links in a single advertisement
    bodies: List[RLABody] # list of *num_links* link bodies


LinkStateAdvertisement = RouterLinkAdvertisement
