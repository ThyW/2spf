from typing import List

from .db import LinkStateDatabase
from .ip import IpAddress
from .rt import RoutingTable

class Router:
    def __init__(self, id: IpAddress, index: int) -> None:
        self._database: LinkStateDatabase = LinkStateDatabase()
        self._routing_table: RoutingTable = RoutingTable()
        self._neighbors: List[Router] = list()

        self.index: int = index
        self.id: IpAddress = id

    def add_neighbor(self, r: "Router") -> None:
        self._neighbors.append(r)

    def remove_neighbor(self, r: "Router") -> None:
        id = r.index
        for n in self._neighbors:
            if n.id == id:
                self._neighbors.remove(n)
