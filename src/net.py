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
    * has_dr: bool : indicate if the network has a DR
    * has_bdr: bool : indicate if the network has a BDR
    """
    def __init__(self) -> None:
        self._routers: List[Router] = list()
        self._lsas: List[LinkStateAdvertisement] = list()
        self._last_address: IpAddress = IpAddress(x) if\
                (x := IpAddress.int_from_str("192.168.0.0")) else IpAddress(0)
        self.has_dr: bool = False
        self.has_bdr: bool = False

    def add_routers(self, input: List[Tuple[int, int, int, bool]]) -> None:
        """
        Given a list of router settings, create new routers on the network.
        """
        for info in input:
            index, id, priority, ma = info
            new_router = Router(IpAddress(id), index, priority, ma)
            self._routers.append(new_router)

    def add_links(self, input: List[Tuple[int, int, int]]) -> None:
        """
        Given a list of link configurations, create a list of link state
        advertisements from the list of configurations. After this step,
        link all routers and establish neighboring relationships.
        """
        for link in input:
            a, b, cost = link
            r1 = self.find_id(a)
            r2 = self.find_id(b)

            if not (r1 and r2):
                return

            # simulation of becoming neighbors between two routers
            r1.add_neighbor(r2.send_hello())
            # print(f"{r1._neighbors} neighbor")

            if r1 and r2:
                lsa = LinkStateAdvertisement(0,
                                             0,
                                             1,
                                             r1.id.get(),
                                             r1.index,
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
                # print(lsa)
                self._lsas.append(lsa)
                # print("added lsa")

    def find_id(self, id: int) -> Optional[Router]:
        """
        Find a router given its unique index.
        """
        for router in self._routers:
            if router.index == id:
                return router
        return None

    def get_dr_and_bdr(self) -> Optional[Tuple[int, int]]:
        """
        Return the indexes of DR and BDR on the network.
        """

        if self.has_dr and self.has_bdr:
            return (self._dr, self._bdr)
        else:
            self.election()
            if self.has_dr and self.has_bdr:
                return (self._dr, self._bdr)
            else:
                return (self._routers[0].index, self._routers[1].index)

    def run(self) -> List[Tuple[int, int, List[int]]]:
        """
        Run the network simulation.

        1. Elect a DR and BDR
        2. Simulate all shortest paths from every to every router on the
           Network.
        3. Communicate all these changes and processes back to the GUI so it
           can be drawn on the canvas.
        """
        self.election()
        for each in self._routers:
            each.recieve_advertisements(self._lsas)

        path_list = []
        [r.init_rt() for r in self._routers]
        for _ in self._routers:
            # print(f"{r.index}: {r._routing_table}")
            pass
        for router in self._routers:
            path_list.extend(self._get_paths(router))

        # print(path_list)
        return path_list

    def _get_paths(self, start: Router) -> List[Tuple[int, int, List[int]]]:
        """
        Get best path from every router on the network to every router on the
        network.
        """
        path_list = []
        for entry in start.get_rt_entries():
            l = []
            dest = entry.destination_id
            next = entry.next_hop
            l.append(next)
            if not next == dest:
                while next != dest:
                    if not next:
                        break
                    res = self.find_id(next)
                    if res:
                        if next not in l:
                            l.append(next)
                        next = res.get_next_for(dest)
                    else:
                        break

            path_list.append((start.index, dest, l))

        return path_list

    def election(self) -> None:
        """
        Run the process of electing a DR and a BDR on the network. These
        routers will be marked as such, DR will be RED and BDR will be BLUE.
        """
        ma_capable = [r for r in self._routers if r.has_ma()]

        if not ma_capable:
            return

        s = sorted(ma_capable, key=lambda x: x.priority, reverse=True)

        if self.has_dr and self.has_bdr:
            return

        for each in s:
            if not self.has_dr or not each.is_bdr() or not each.priority == 0:
                each.set_dr()
                self._dr = each.index
                self.has_dr = True
                break
        for each in s:
            if not each.is_dr() or self.has_bdr or not each.priority == 0:
                each.set_bdr()
                self._bdr = each.index
                self.has_bdr = True
                break
