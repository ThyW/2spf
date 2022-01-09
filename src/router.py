from typing import List

from .db import LinkStateDatabase
from .ip import IpAddress
from .rt import RoutingTable
from .message import HelloMessage
from .link_state import LinkStateAdvertisement

class Router:
    def __init__(self, id: IpAddress, index: int) -> None:
        self._database: LinkStateDatabase = LinkStateDatabase(id.get())
        self._routing_table: RoutingTable = RoutingTable()
        self._neighbors: List[int] = list()

        self.index: int = index
        self.id: IpAddress = id

    def add_neighbor(self, r: HelloMessage) -> None:
        self._neighbors.append(r.router_id)

    def remove_neighbor(self, r: int) -> None:
        for n in self._neighbors:
            if n == r:
                self._neighbors.remove(n)

    def send_hello(self) -> HelloMessage:
        return HelloMessage(2,
                            1,
                            0,
                            self.id.get(),
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            self._neighbors)

    def recieve_advertisements(self, l: List[LinkStateAdvertisement]) -> None:
        (self._database.add(x) for x in l)

    def init_rt(self) -> None:
        self._routing_table = self._database.create_routing_table()

