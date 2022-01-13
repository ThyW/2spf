from typing import List

from .db import LinkStateDatabase
from .ip import IpAddress
from .rt import RoutingTable
from .message import HelloMessage
from .link_state import LinkStateAdvertisement

class Router:
    """
    A representation of a router running the OSPF protocol.

    ---
    Attributes:
    ---
    * id: IpAddress : router's ID, an IPv4 address.
    * index: int : a unique number identifying a router.
    * priority: int : 8-bit unsigned integer from 0 to 255, which specifies,
      the priority in the DR and BDR election process. If the value is 0, the 
      router can never become a DR or a BDR. The higher the value, the higher
      the chance of a router becoming a DR or a BDR.
    * _database: LinkStateDatabase : each router has it's own link state
      database. For more information about how they work, please consult their
      documentation on in `db.py`.
    * _routing_table: RoutingTable : each router also has a routing table,
      where all the routing information and best paths to every other part
      of the network is located. For more information about a Routing Table,
      please consult the documentation in the `rt.py`.
    * _neighbors: List[int] : list of router IDs of its neighboring routers.
    * _dr: bool : indicates if the routers has been elected as a DR
    * _bdr: bool : indicates if the routers has been elected as a BDR
    * _ma: bool : indicates if the router is connected to a switch, if it has
      multi-access capability. Only routers that have multi-access capability
      can be considered election candidates for the DR and BDR election.
    """
    def __init__(self, id: IpAddress, index: int, priority: int, ma: bool) -> None:
        self._database: LinkStateDatabase = LinkStateDatabase(id.get())
        self._routing_table: RoutingTable = RoutingTable()
        self._neighbors: List[int] = list()
        self._dr: bool = False
        self._bdr: bool = False
        self._ma: bool = ma

        self.index: int = index
        self.id: IpAddress = id
        self.priority: int = priority

    def add_neighbor(self, r: HelloMessage) -> None:
        """
        Add a new number from a parsed Hello message.
        """
        if not r.router_id in self._neighbors:
            self._neighbors.append(r.router_id)

    def remove_neighbor(self, r: int) -> None:
        """
        Remove a neighbor based on its router ID.
        """
        for n in self._neighbors:
            if n == r:
                self._neighbors.remove(n)

    def send_hello(self) -> HelloMessage:
        """
        Create a Hello message describing this router.
        """
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
        """
        Receive and handle any and all incoming link state advertisements.
        """
        (self._database.add(x) for x in l)

    def init_rt(self) -> None:
        """
        Construct a routing table from each router's link state database. For
        more information about this procedure, please consult the documentation
        in `db.py`.
        """
        self._routing_table = self._database.create_routing_table()

    def is_dr(self) -> bool:
        """
        Check if the router is a Dedicated Router.
        """
        return self._dr

    def is_bdr(self) -> bool:
        """
        Check if the router is a Backup Dedicated Router.
        """
        return self._bdr

    def set_dr(self) -> None:
        """
        Tell the router that it has been elected as a DR.
        """
        self._dr = True

    def set_bdr(self) -> None:
        """
        Tell the router that it has been elected as a BDR.
        """
        self._bdr = True

    def has_ma(self) -> bool:
        """
        Check if the router is on a multi-access part of the network, in other
        words, if it's connected to a switch.
        """
        return self._ma
