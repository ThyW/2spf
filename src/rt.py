#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List
from enum import IntEnum
from .link_state import LinkStateAdvertisement


class DestType(IntEnum):
    """
    Type of the destination in a Routing Table Entry
    """
    NETWORK = 1,
    AREA_BORDER_ROUTER = 2
    AS_BOUNDRY_ROUTER = 3


@dataclass
class RTEntry:
    """
    Single entry in a routing table.

    ---
    Attributes:
    ---
    * destination_type: int : the type of the destination this route leads to.
      `ALWAYS 1`
    * destination_id: int : router ID of the destination router.
    * network_mask: int : network mask with which a sub net can be derived. 
      `IGNORE`
    * path_type: type of the path, intra-network, inter-network and others.
      `ALWAYS 1`
    * cost: int : total cost of this path.
    * next_hop: int : router ID of the next step in packet's journey.
    """
    destination_type: int # alwasy going to be 1
    destination_id: int   # id of the destination router
    network_mask: int     # ignore
    path_type: int     # this will always be one, since we only simulate paths
                       # within a network
    cost: int          # total cost
    next_hop: int      # id of the "next hop" router

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
                       next_hop_id)            # TODO

    @classmethod
    def create(cls, dest: int, cost: int, next_hop: int) -> "RTEntry":
        """
        Create a new Router Entry given only the necessary information.
        """
        return RTEntry(1,
                       dest,
                       0xffffffff,
                       1,
                       cost,
                       next_hop)


class RoutingTable:
    """
    A table or a database of all the best paths within a network.

    ---
    Attributes:
    ---
    * _entries: List[RTEntry] : a list of all router entries
    """
    def __init__(self):
        self._entries: List[RTEntry] = list()

    def add_entry(self, entry: RTEntry) -> None:
        """
        Add a new entry to the routing table.
        """
        self._entries.append(entry)

    def get_entries(self) -> List[RTEntry]:
        """
        Basically return self in a List form so all entries can be easily
        iterated through.
        """
        return self._entries

    def __str__(self) -> str:
        s = ""

        for each in self._entries:
            s += f"{each.destination_id}; {each.next_hop}\n"
        return s
