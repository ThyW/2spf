#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List
from enum import IntEnum
from .link_state import LinkStateAdvertisement


class DestType(IntEnum):
    NETWORK = 1,
    AREA_BORDER_ROUTER = 2
    AS_BOUNDRY_ROUTER = 3


@dataclass
class RTEntry:
    destination_type: int # alwasy going to be 1
    destination_id: int # id of the destination router
    network_mask: int # ignore
    path_type: int # this will always be one, since we only simulate paths
                   # within a network
    cost: int # total cosst
    next_hop: int # id of the "next hop" router

    @classmethod
    def from_lsa(cls, adv: LinkStateAdvertisement, next_hop_id: int) -> "RTEntry":
        return RTEntry(1, # always 1
                       adv.advertising_router, # advertising router
                       0xffffffff, # full mask
                       1, # always 1, we simulate paths within a network
                       adv.bodies[0].tos_zero, # we only use one tos, tos zero
                                               # as well as each router having
                                               # only one interface, therefore
                                               # only one RLABody
                       next_hop_id) # TODO


class RoutingTable:
    def __init__(self):
        self._entries: List[RTEntry] = list()
