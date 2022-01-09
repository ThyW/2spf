import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from .constants import *
from .net import Network


@dataclass
class RouterGui:
    x: int
    y: int
    index: int

    def is_in(self, coords: Tuple[int, int]) -> bool:
        x, y = coords
        if (x >= self.x - RADIUS and x <= self.x + RADIUS)\
            and (y >= self.y - RADIUS and y <= self.y + RADIUS):
                return True
        return False

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.index)


@dataclass
class Link:
    a: RouterGui
    b: RouterGui
    cost: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.a.index,self.b.index, self.cost)


class Gui:
    def __init__(self) -> None:
        self._routers: List[RouterGui] = list()
        self._links: List[Link] = list()
        self._index: int = 0
        self._network: Optional[Network] = None
        self._link_start: Optional[RouterGui] = None

        self._win = tk.Tk()
        self._can = tk.Canvas(self._win,
                              width=CANVAS_WIDTH,
                              height=CANVAS_HEIGHT,
                              bg="white")

        self._consturct_network_b = tk.Button(self._win,
                                              text="Construct Network",
                                              command=self._construct)
        self._cost_e = tk.Entry(self._win)
        self._cost_l = tk.Label(self._win,
                                text="Link cost")

        self._can.pack()

        self._cost_l.pack()
        self._cost_e.pack()
        self._consturct_network_b.pack()

        self._can.bind("<Button-1>", self._left_click)
        self._can.bind("<Button-3>", self._right_click)
        self._can.bind("<Button-2>", self._middle_click)

    def run(self) -> None:
        self._can.mainloop()

    def _cost_checked(self) -> int:
        ty = ""
        try:
            ty = self._cost_e.get()
        except ValueError:
            ty = "ei"
            print("[WARN] No cost specified, using the default value of 10.")
        types = {
                "gei": 1,
                "fei": 1,
                "ei": 10,
                "ds1": 64,
                "dsl": 134
                }
        if not ty.lower() in types.keys():
            return 10
        else:
            return types[ty.lower()]

    def _construct(self) -> None:
        net = Network()
        self._network = net

    def _new_router(self, coords: Tuple[int, int]) -> None:
        self._index += 1
        self._routers.append(RouterGui(coords[0], coords[1], self._index))

    def _remove_router(self, coords: Tuple[int, int]) -> None:
        for router in self._routers:
            if router.is_in(coords):
                self._routers.remove(router)


    def _left_click(self, event) -> None:
        coords = (event.x, event.y)
        self._new_router(coords)
        self._draw()

    def _right_click(self, event) -> None:
        coords = (event.x, event.y)
        r_i = None

        for router in self._routers:
            if router.is_in(coords):
                r_i = router
                break
        if not r_i:
            return

        if self._link_start:
            self._link(r_i, self._link_start)
            self._link_start = None
        else:
            self._link_start = r_i
        self._draw()

    def _middle_click(self, event) -> None:
        coords = (event.x, event.y)
        self._remove_router(coords)
        self._draw()

    def _draw(self) -> None:
        self._can.delete("all")
        for router in self._routers:
            self._can.create_oval(router.x - RADIUS,
                                  router.y - RADIUS,
                                  router.x + RADIUS,
                                  router.y + RADIUS)
            self._can.create_text(router.x,
                                  router.y + 25,
                                  text=str(router.index))

        for link in self._links:
            a = link.a
            b = link.b
            c = link.cost

            self._can.create_line(a.x, a.y,  b.x, b.y)
            self._can.create_text((a.x + b.x) / 2 + 10,
                                  (a.y + b.y) / 2 - 10,
                                  text=f"{c}")

    def _link(self, i1: RouterGui, i2: RouterGui) -> None:
        cost = self._cost_checked()
        # we do this both ways, since we simulate how the OSPF actually works
        self._links.append(Link(i1, i2, cost))
        self._links.append(Link(i2, i1, cost))

    @classmethod
    def tuplify(cls, input: Union[List[RouterGui], List[Link]]) -> List[Tuple[int, int, int]]:
        return [i.to_tuple() for i in input]
