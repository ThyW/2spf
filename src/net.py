from typing import List, Optional, Tuple

from .router import Router
from .ip import IpAddress
from .link_state import LinkStateAdvertisement, RLABody

class Network:
    """
    A representation and a simulation of a network running the OSPF protocol.
    This is not a continuous network, it's but a simple snapshot of the network
    in at one point in time.

    ---
    Attributes:
    ---
    * _routers: List[Router] : all routers in the network.
    * _lsas: List[LinkStateAdvertisement] : all link state advertisement
      generated, when initializing the network.
    * _last_address: IpAddress : when no IPv4 address is assigned to a new
      router, the network automatically assigns a new, one higher address than
      the last time.
    """
    def __init__(self) -> None:
        self._routers: List[Router] = list()
        self._lsas: List[LinkStateAdvertisement] = list()
        self._last_address: IpAddress = IpAddress(x) if\
                (x := IpAddress.int_from_str("192.168.0.0")) else IpAddress(0)

    def add_routers(self, input: List[int]) -> None:
        """
        Given a list of router settings, create new routers on the network.
        """
        for index in input:
            id = self._last_address + 1
            if id.get() != self._last_address.get():
                new_router = Router(id, index)
                self._routers.append(new_router)
                self._last_address += 1

    def add_links(self, input: List[Tuple[int, int, int]]) -> None:
        """
        Given a list of link configurations, create a list of link state
        advertisements from the list of configurations. After this step,
        link all routers and establish neighboring relationships.
        """
        # TODO handle DRs and BDRs
        for link in input:
            a, b, cost = link
            r1 = self.find_id(a)
            r2 = self.find_id(b)

            if not (r1 and r2):
                return

            # simulation of becoming neighbors between two routers
            r1.add_neighbor(r2.send_hello())

            if r1 and r2:
                lsa = LinkStateAdvertisement(0,
                                             0,
                                             1,
                                             r1.id.get(),
                                             r1.id.get(),
                                             1,
                                             0,
                                             0,
                                             False,
                                             False,
                                             False,
                                             1,
                                             [RLABody(
                                                 r2.id.get(),
                                                 r2.index,
                                                 0,
                                                 cost,
                                                 {}
                                                 )])
                self._lsas.append(lsa)

    def find_id(self, id: int) -> Optional[Router]:
        """
        Find a router given its unique index.
        """
        for router in self._routers:
            if router.index == id:
                return router
        return None

    def run(self) -> None:
        # todo
        pass
