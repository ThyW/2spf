#!/usr/bin/env python3
from .link_state import LinkStateAdvertisement
from .rt import RoutingTable, RTEntry
from heapq import heappop, heappush
from typing import List, Optional, Tuple
from sys import maxsize


class Node:
    """
    Node in a graph.

    This is used when we run the Dijkstra's algorithm for finding the best
    paths to each router in a network.

    ---
    Attributes:
    ---
        * id : int : Router ID of this router represented as a graph vertex(node).
        * cost int : Cost of getting to this vertex. The lower the index, the 
                     likelier is a vertex going to be visited.
        * neighbors: List[Tuple[Node, int]] : A list of all neighbor vertices.
        * previous : A reference to the previous node.
    """
    def __init__(self, id: int) -> None:
        """
        Create a new node.

        :id: unique id of the Node, in our case a router, therefore, this
             should be the router ID of the router we are interpreting as a
             node.
        """
        self.id: int = id
        self.cost: int = maxsize
        self.neighbors: List[Tuple[Node, int]] = list()
        self.previous: Optional[Node] = None

    def add(self, n: "Node", cost: int) -> None:
        """
        Add a new neighbor to an existing node.

        :n: Node object we want to add as a neighbor.
        :cost: The cost of the link between this node and the one we are
        adding.
        """
        self.neighbors.append((n, cost))

    def __lt__(self, o: "Node") -> bool:
        """
        This method is implemented due to the fact that we are passing nodes
        into a heap, because our Dijkstra's algorithm is implemented using a min
        heap.
        """
        return self.cost < o.cost

    def __str__(self) -> str:
        return f"Node: {{ {self.id}, {self.cost}, {self.neighbors} }}"


class LinkStateDatabase:
    """
    Database holding all Link State Advertisements received by the router.
    """
    def __init__(self, id: int) -> None:
        """
        Creates a new Link State Database.

        :id: Router ID of our current router. This is required, because we need
             to know our router ID when we run the SPF algorithm.
             Theoretically, this is not necessary to have as a class attribute.
        """
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

        :adv: A Link State Advertisement we wish to be added to the database.
        """
        self._content.append(adv)

    def remove(self, adv: LinkStateAdvertisement) -> None:
        """
        Remove a link state advertisement from the link state database.

        :adv: A Link State Advertisement we wish removed from the database.
        """
        for each in self._content:
            if each.ls_id == adv.ls_id:
                self._content.remove(each)

    def create_routing_table(self) -> RoutingTable:
        """
        This method does three things:
            1. Constructs a graph of the network based on the information from
            all Link State Advertisements received.
            2. Calculate the best route to each of the networks routers. This
            is done with the use of Dijkstra's algorithm.
            3. Create and return a Routing Table, this holds entries about
            every destination (Router) on the network. For more info on how a
            Routing Table is structured, please consult its documentation
            found in the `rt.py` file.
        """
        rt = RoutingTable()
        nodes: List[Node] = list()
        used_ids: List[int] = list()
        # create a graph
        for adv in self._content:
            if not adv.advertising_router in used_ids:
                nodes.append(Node(adv.advertising_router))
                used_ids.append(adv.advertising_router)
        for each in nodes:
            for adv in self._content:
                # start, end, cost of link
                adv_id, id, cost = (adv.advertising_router, adv.bodies[0].link_data, adv.bodies[0].tos_zero)
                # node where the link originates from
                x = [n for n in nodes if adv_id == n.id]
                if len(x) == 1:
                    # if the end of the link is current router
                    if id == each.id:
                        # add it as a neighbor
                        each.add(x[0], cost)

        # run djikstra for each router from with this router as start
        start = self._my_id
        ids = [x.id for x in nodes if x.id != self._my_id]

        # Here is where the real magic happens. We run djikstra's algorithm
        # which is implemented using a min-heap.

        while ids:
            id = ids.pop(0)
            end = None
            heap = []
            for each in nodes:
                if each.id == start:
                    each.cost = 0
                else:
                    each.cost = maxsize
                    if each.id == id:
                        end = each
                heappush(heap, each)

            while heap:
                for pair in heap[0].neighbors:
                    if pair[0].cost > (pair[1] + heap[0].cost):
                        pair[0].cost = pair[1] + heap[0].cost
                        pair[0].previous = heap[0]
                heappop(heap)

            if end:
                cost = end.cost

                if end.previous:
                    p = end.previous
                    x = [end.id]
                    while p.id != start:
                        x.append(p.id)
                        if p.previous:
                            p = p.previous
                    x.reverse()
                    rt.add_entry(RTEntry.create(id, cost, x[0]))
            else:
                print("[ERROR] Incomplete entry, total cost.")

        return rt

    def __str__(self) -> str:
        s = ""
        for each in self._content:
            s += f"{each}\n"
        return s
