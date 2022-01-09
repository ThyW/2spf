#!/usr/bin/env python3

from typing import List, Optional, Tuple
from .link_state import LinkStateAdvertisement
from .rt import RoutingTable, RTEntry

from heapq import heappop, heappush


class Node:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.cost: int = 100000
        self.neighbors: List[Tuple[Node, int]] = list()

    def add(self, n: "Node", cost: int) -> None:
        self.neighbors.append((n, cost))

    def __lt__(self, o: "Node") -> bool:
        return self.cost < o.cost


class LinkStateDatabase:
    """
    Database holding information about all link state advertisements recieved
    by the router.
    """
    def __init__(self, id) -> None:
        self._content: List[LinkStateAdvertisement] = list()
        self._my_id: int = id

    def __getitem__(self, key: int) -> Optional[LinkStateAdvertisement]:
        for each in self._content:
            if each.ls_id == key:
                return each
        return None

    def add(self, adv: LinkStateAdvertisement) -> None:
        """
        Add a new link state advertisement to the link state database. 
        """
        self._content.append(adv)

    def remove(self, adv: LinkStateAdvertisement) -> None:
        """
        Remove a link state advertisement from the link state database.
        """
        for each in self._content:
            if each.ls_id == adv.ls_id:
                self._content.remove(each)

    def create_routing_table(self) -> RoutingTable:
        """
        Create a graph of all routers, then run the djikstra algorithm and
        consturct a routing table.
        """
        rt = RoutingTable()
        nodes: List[Node] = list()
        # create graph
        for adv in self._content:
            if not adv.advertising_router in nodes:
                nodes.append(Node(adv.advertising_router))
        for each in nodes:
            for adv in self._content:
                id, cost = (adv.bodies[0].link_id, adv.bodies[0].tos_zero)
                x = [n for n in nodes if id == n.id]
                if x[0]:
                    if x[0].id == each.id:
                        each.add(x[0], cost)

        # run djikstra for each router from with this router as start
        start = self._my_id
        ids = [x.id for x in nodes if x.id != self._my_id]

        while ids:
            id = ids.pop(0)
            end = None
            heap = []
            for each in nodes:
                if each.id == start:
                    each.cost = 0
                else:
                    each.cost = 100000
                    if each.id == id:
                        end = each
                heappush(heap, each)

            prevs = []

            while heap:
                for pair in heap[0].neighbors:
                    if pair[0].cost > pair[1] + heap[0].cost:
                        pair[0].cost = pair[1] + heap[0].cost
                        prevs.append(heap[0])
                heappop(heap)
            if end:
                cost = end.cost
                if prevs:
                    prevs.reverse()
                    if len(prevs) == 2:
                        rt.add_entry(RTEntry.create(id, cost, prevs[1]))
                    else:
                        rt.add_entry(RTEntry.create(id, cost, prevs[0]))

            else:
                print("[ERROR] Incomplete entry, total cost.")

        return rt

