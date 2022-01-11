import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from .constants import *
from .net import Network
from .ip import IpAddress


@dataclass
class RouterGui:
    """
    A GUI abstraction of a router.

    ---
    Attributes:
    ---
    * x: int : x coordinate of this router on the canvas.
    * y: int : y coordinate of this router on the canvas.
    * index: int : unique ID of this router. No two routers or switches can 
                   have the same index.
    * id: int : integer representation of an IPv4 IP Address. More info on this
                is located in the `ip.py` file.
    * priority: int : Integer value specifying how likely a router is to become
                      a Designated Router(DR) or a Backup Designated Router
                     (BDR)
    """
    x: int
    y: int
    index: int
    id: int
    priority: int

    def is_in(self, coords: Tuple[int, int]) -> bool:
        """
        Check, whether a point on is located within this structure.

        :coords: Coordinates of the point.
        """
        x, y = coords
        if (x >= self.x - RADIUS and x <= self.x + RADIUS)\
            and (y >= self.y - RADIUS and y <= self.y + RADIUS):
                return True
        return False

    def _to_tuple(self) -> Tuple[int, int, int]:
        """
        Serializes this object's necessary information into a tuple.
        """
        # TODO update this
        return (self.x, self.y, self.index)


@dataclass
class SwitchGui:
    """
    A GUI abstraction over a switch.

    ---
    Attributes:
    ---

    * x: int : x coordinate of the switch on the canvas.
    * y: int : y coordinate of the switch on the canvas.
    * index: int : unique ID of a switch. No two routers or switches can have
                   the same ID.
    * routers: List[RouterGui] : a list of routers connected to this switch.
    """
    x: int
    y: int
    index: int
    routers: List[RouterGui]

    def is_in(self, coords: Tuple[int, int]) -> bool:
        """
        Check, whether a point on is located within this structure.

        :coords: Coordinates of the point.
        """
        x, y = coords
        if (x >= self.x - RADIUS and x <= self.x + RADIUS)\
            and (y >= self.y - RADIUS and y <= self.y + RADIUS):
                return True
        return False


@dataclass
class Link:
    """
    A GUI representation of a link between two structures, points on the 
    canvas.

    ---
    Attributes:
    ---
    * a: Union[RouterGui, SwitchGui] : first point of the link, either a router
                                       or a switch.
    * b: Union[RouterGui, SwitchGui] : second point of the link, either a 
                                       router or a switch.
    * cost: int : cost of this link.
    """
    a: Union[RouterGui, SwitchGui]
    b: Union[RouterGui, SwitchGui]
    cost: int

    def _to_tuple(self) -> Tuple[int, int, int]:
        """
        Serializes a link's necessary information into a tuple.
        """
        return (self.a.index, self.b.index, self.cost)


class Gui:
    """
    The main class responsible for running the simulator.

    Handles all graphics and configurations.

    All you need to do is create an instance of this class and then call
    its `run()` method.

    ---
    Attributes:
    ---

    * _routers: List[RouterGui] : a list of all routers in the GUI.
    * _links: List[Link] : a list of all links in the GUI.
    * _index: int : last index of a new router or a switch in the GUI.
    * _network: Optional[Network] : Network object created after hitting the 
      `Construct Network` button.
    * _link_start: Optional[Union[RouterGui, SwitchGui]] : linking things is
      done by right-clicking two objects on the canvas. If this objects are
      valid, a link between them is created, the first click or, in other
      words, the first structure of a link is stored in this variable.
    * _switches: List[SwitchGui] : a list of all switches in the GUI.
    * _win: tkinter.Tk : backing window of the program.
    
    The rest the attributes are unimportant, as they are all just parts of the
    GUI such as buttons, entries and labels. They won't be documented here as
    their usage should be self explanatory just by glancing over the code.
    """
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
        """
        Create the window and the GUI, than run it..
        """
        self._can.mainloop()

    def _construct(self) -> None:
        """
        Create a network. All the processes needed for a network to be created
        and used are described in the `net.py` file and its documentation.
        """
        net = Network()
        self._network = net

    def _new_router(self, coords: Tuple[int, int], id: str, priority: int) -> None:
        """
        When left clicking anywhere on the canvas, the user is prompted to
        with a choice of either creating a switch or a router. When the user
        chooses to create a router, this function is responsible for creating
        a new router, as well as redrawing all the entities to the canvas.

        :coords: the coordinates of the new router.
        :id: the router ID, an IPv4 address in the form of a string(1.1.1.1).
             Later translated into an actual IPv4 address.
        :priority: router's priority of becoming either a DR or a BDR.
        """
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
        """
        Remove a router based on coordinates supplied, if they do not point to
        any router the function just returns.

        :coords: coordinates of the remove request.
        """
        for router in self._routers:
            if router.is_in(coords):
                self._routers.remove(router)

    def _remove_links(self, r: Union[RouterGui, SwitchGui]) -> None:
        """
        Remove all links in the GUI which originate from, or point to a 
        supplied object.

        :r: object we want all links removed from.
        """
        to_remove = list()
        for each in self._links:
            if (each.a.index == r.index) or (each.b.index == r.index):
                to_remove.append(each)
        _ = [self._links.remove(x) for x in to_remove]

    def _remove(self, coords: Tuple[int, int]) -> None:
        """
        Remove either a switch or a router based on the supplied coordinates.
        If no object is present on these coordinates, the function simply
        returns without doing anything.

        :coords: the coordinates of the point we want to check for switches, or
                 routers.
        """
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
        """
        Handle an incoming left-click event.
        """
        coords = (event.x, event.y)
        self._pop_up("choice", coords)

    def _right_click(self, event) -> None:
        """
        Handle an incoming right-click event.
        """
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
        """
        Handle an incoming middle-click event.
        """
        coords = (event.x, event.y)
        self._remove(coords)
        self._draw()

    def _draw(self) -> None:
        """
        Draw all routers, switches and links to the canvas.
        """
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
        """
        Link two objects. This means two links are created, one originating
        from the first and the other from the second object. This function is
        also responsible for redrawing all objects.

        :i1: first object, either a switch or a router.
        :i2: second object, either a switch or a router.
        :cost: cost of the link.
        """
        # we do this both ways, since we simulate how the OSPF actually works
        self._links.append(Link(i1, i2, cost))
        self._links.append(Link(i2, i1, cost))
        self._draw()

    def _pop_up(self,
                type: str,
                coords: Tuple[int, int],
                win: Optional[tk.Toplevel] = None,
                r: Union[RouterGui, SwitchGui] = None) -> None:
        """
        Handle the action of showing appropriate pop up windows based on their
        type.

        :type: type of the pop up can be: 
               - 'router'
               - 'switch'
               - 'link'
               - 'choice'
        :coords: coordinates of the originating event.
        :win: close an already existing pop up.
        :r: optional, used only when calling with the 'link' type.
        """
        if win:
            win.destroy()
        x, y = coords
        if type == "router":
            self._router_popup(x, y)
            pass
        elif type == "switch":
            self._create_switch(x, y)
            pass
        elif type == "choice":
            self._choice_popup(x, y)
            pass
        elif type == "link":
            if r:
                self._link_popup(x, y, r)

    def _handle_popup(self, type: str, win: tk.Toplevel, *args) -> None:
        """
        This function is called from within a pop up and is responsible for
        doing the necessary actions such as getting additional information from
        the pop up in the form of entry values, while also being responsible 
        for closing the pop up after.

        :type: either 'r' or 'l', suggest what should be done with the pop up's
               info.
        :win: the pop up window itself
        :args: other data which is needed from the pop up.
        """
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

    def _router_popup(self, x: int, y: int) -> None:
        """
        Create a router creation and configuration pop up window.
        """
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

    def _create_switch(self, x: int, y: int) -> None:
        """
        Creates a new switch and re-renders the screen.

        :x: x part of the coordinates of the new switch.
        :y: y part of the coordinates of the new switch.
        """
        self._index =+ 1
        self._switches.append(SwitchGui(x, y, self._index, []))
        self._draw()

    def _choice_popup(self, x: int, y: int) -> None:
        """
        Create a pop up for choice between a router and a switch.
        """
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
        """
        Create a pop up for the configuration of a new link which is being
        created.
        """
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
        return [i._to_tuple() for i in input]
