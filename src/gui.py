import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from .constants import *
from .net import Network
from .ip import IpAddress


@dataclass
class RouterGui:
    x: int
    y: int
    index: int
    id: int
    priority: int

    def is_in(self, coords: Tuple[int, int]) -> bool:
        x, y = coords
        if (x >= self.x - RADIUS and x <= self.x + RADIUS)\
            and (y >= self.y - RADIUS and y <= self.y + RADIUS):
                return True
        return False

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.index)


@dataclass
class SwitchGui:
    x: int
    y: int
    index: int
    routers: List[RouterGui]

    def is_in(self, coords: Tuple[int, int]) -> bool:
        x, y = coords
        if (x >= self.x - RADIUS and x <= self.x + RADIUS)\
            and (y >= self.y - RADIUS and y <= self.y + RADIUS):
                return True
        return False


@dataclass
class Link:
    a: Union[RouterGui, SwitchGui]
    b: Union[RouterGui, SwitchGui]
    cost: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.a.index,self.b.index, self.cost)


class Gui:
    def __init__(self) -> None:
        self._routers: List[RouterGui] = list()
        self._links: List[Link] = list()
        self._index: int = 0
        self._network: Optional[Network] = None
        self._link_start: Optional[Union[RouterGui, SwitchGui]] = None
        self._switches: List[SwitchGui] = list()

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

    def _new_router(self, coords: Tuple[int, int], id: str, priority: int) -> None:
        self._index += 1
        ip = IpAddress(0)
        i = IpAddress.int_from_str(id)
        if i:
            ip = IpAddress(i)
        else:
            print("[ERROR] Can't conver to IP Address")
            ip = IpAddress(self._index)

        self._routers.append(RouterGui(coords[0],
                                       coords[1],
                                       self._index,
                                       ip.get(),
                                       priority))
        self._draw()

    def _remove_router(self, coords: Tuple[int, int]) -> None:
        for router in self._routers:
            if router.is_in(coords):
                self._routers.remove(router)

    def _remove_links(self, r: Union[RouterGui, SwitchGui]) -> None:
        to_remove = list()
        for each in self._links:
            if (each.a.index == r.index) or (each.b.index == r.index):
                to_remove.append(each)
        _ = [self._links.remove(x) for x in to_remove]

    def _remove(self, coords: Tuple[int, int]) -> None:
        for router in self._routers:
            if router.is_in(coords):
                self._remove_links(router)
                self._routers.remove(router)
                return

        for switch in self._switches:
            if switch.is_in(coords):
                self._remove_links(switch)
                self._switches.remove(switch)
                return

    def _left_click(self, event) -> None:
        coords = (event.x, event.y)
        self._pop_up("choice", coords)

    def _right_click(self, event) -> None:
        coords = (event.x, event.y)
        r_i = None
        for router in self._routers:
            if router.is_in(coords):
                r_i = router
                break
        for switch in self._switches:
            if switch.is_in(coords):
                r_i = switch
        if not r_i:
            return

        if self._link_start:
            self._pop_up("link", coords, r=r_i)
        else:
            self._link_start = r_i

    def _middle_click(self, event) -> None:
        coords = (event.x, event.y)
        self._remove(coords)
        self._draw()

    def _draw(self) -> None:
        self._can.delete("all")

        # drawing of all routers
        for router in self._routers:
            self._can.create_oval(router.x - RADIUS,
                                  router.y - RADIUS,
                                  router.x + RADIUS,
                                  router.y + RADIUS)
            self._can.create_text(router.x,
                                  router.y + 25,
                                  text=str(router.index))
            self._can.create_line(router.x,
                                  router.y + 2,
                                  router.x,
                                  router.y + RADIUS - 2)
            self._can.create_line(router.x,
                                  router.y - 2,
                                  router.x,
                                  router.y - RADIUS + 2)
            self._can.create_line(router.x + 2,
                                  router.y,
                                  router.x + RADIUS - 2,
                                  router.y)
            self._can.create_line(router.x - 2,
                                  router.y,
                                  router.x - RADIUS + 3,
                                  router.y)
        
        for switch in self._switches:
            x, y = switch.x, switch.y
            self._can.create_rectangle(x - 2 * RADIUS,
                                       y - RADIUS,
                                       x + 2 * RADIUS,
                                       y + RADIUS)

        for link in self._links:
            a = link.a
            b = link.b
            c = link.cost

            self._can.create_line(a.x, a.y,  b.x, b.y)
            self._can.create_text((a.x + b.x) / 2 + 10,
                                  (a.y + b.y) / 2 - 10,
                                  text=f"{c}")

    def _link(self,
              i1: Union[RouterGui, SwitchGui],
              i2: Union[RouterGui, SwitchGui],
              cost: int) -> None:
        # we do this both ways, since we simulate how the OSPF actually works
        self._links.append(Link(i1, i2, cost))
        self._links.append(Link(i2, i1, cost))
        self._draw()

    def _pop_up(self,
                type: str,
                coords: Tuple[int, int],
                win: Optional[tk.Toplevel] = None,
                r: Union[RouterGui, SwitchGui] = None) -> None:
        if win:
            win.destroy()
        x, y = coords
        if type == "router":
            self._router_popup(x, y)
            pass
        elif type == "switch":
            self._switch_popup(x, y)
            pass
        elif type == "choice":
            self._choice_popup(x, y)
            pass
        elif type == "link":
            if r:
                self._link_popup(x, y, r)

    def _handle_popup(self, type: str, win: tk.Toplevel, *args) -> None:
        if type == "r":
            id, priority = (args[0].get(), args[1].get())
            try:
                priority = int(priority)
            except ValueError:
                print("[ERROR] priority must be an integer value!")
                priority = 1
            x, y = args[2]
            self._new_router((x, y), id, priority)
        if type == "l":
            cost = args[0].get()
            try:
                cost = int(cost)
            except ValueError:
                print("[ERROR] Cost has to be an integer value!")
                cost = 10
            link = args[1]

            if self._link_start:
                self._link(link, self._link_start, cost)
                self._link_start = None

        win.destroy()

    def _router_popup(self, x, y) -> None:
        win = tk.Toplevel(self._win)
        win.title("Router Configurator")

        id_label = tk.Label(win, text="ID")
        id_entry = tk.Entry(win)
        priority_label = tk.Label(win, text="Priority")
        priority_entry = tk.Entry(win)

        b = tk.Button(win,
                      text="Create",
                      command=(lambda:\
                              self._handle_popup("r",
                                                 win,
                                                 id_entry,
                                                 priority_entry,
                                                 (x, y))))
        id_label.pack()
        id_entry.pack()
        priority_label.pack()
        priority_entry.pack()
        b.pack()

    def _switch_popup(self, x, y) -> None:
        self._index =+ 1
        self._switches.append(SwitchGui(x, y, self._index, []))
        self._draw()

    def _choice_popup(self, x, y) -> None:
        win = tk.Toplevel(self._win)
        b1 = tk.Button(win,
                       text="Router",
                       command=(lambda: self._pop_up("router",
                                                     (x, y),
                                                     win=win)))
        b2 = tk.Button(win,
                       text="Switch",
                       command=(lambda: self._pop_up("switch",
                                                     (x, y),
                                                     win)))
        b1.pack()
        b2.pack()

    def _link_popup(self, x: int, y: int, u: Union[RouterGui, SwitchGui]) -> None:
        win = tk.Toplevel(self._win)
        coords = (x, y)

        l = tk.Label(win, text="Cost")
        e = tk.Entry(win)

        b = tk.Button(win,
                      text="Create",
                      command=(lambda: self._handle_popup("l",
                                                          win,
                                                          e,
                                                          u,
                                                          coords)))
        l.pack()
        e.pack()
        b.pack()

    @classmethod
    def tuplify(cls, input: Union[List[RouterGui], List[Link]]) -> List[Tuple[int, int, int]]:
        return [i.to_tuple() for i in input]
