# Architecture

## GUI
Whenever the program is run, a GUI is shown. There are multiple buttons(B) and entry fields(EF):
- **Priority(EF)**: this field specifies the priority of a router to become a Designated Router. Values can range from 0 to 255. Any values larger than 255 will be discarded and 255 will be used instead. If a routers priority is set to 0, it can never become a designated router.
- **Speed(EF)**: this field specifies the internet speed of the router's connection to the network. This is also the value, which will be used when calculating the shortest path using Dijkstra's algorithm. If not specified, the default value of *10* (EI) will be assumed. You can use either the value, or the abbreviated name, for example *ei* or *Fei* will do. The list of available values, as well as their costs follows:
    - Gigabit Ethernet Interface [1 Gbps] (GEI): 1
    - Fast Ethernet Interface [100 Mbps] (FEI): 1
    - Ethernet Interface [10 Mbps] (EI): 10
    - DS1 [1.544 Mbps]: 64
    - DSL [0.768 Mbps]: 133
- **Source(EF)**: this field specifies the IP address or index of the packet's source router. This field is needed for the shortest path algorithm.
- **Destination(EF)**: this field specifies the IP address or index of the packet's destination router. This field is needed for the shortest path algorithm.
- **SP(B)**: this button will simulate the shortest path. In order to work, the value of the *Destination* and *Source* entry fields must be filled out and must be correct.

After clicking the *SP* button, the shortest path will be calculated and the path between routers will be drawn, as well as their costs. Note, if the *Source*'s entry field value is invalid or not provided at all, the beginning point of shortest path algorithm will be the *designated router*, which the network chooses according to the specification in the [RFC 1583](https://www.freesoft.org/CIE/RFC/1583/index.htm).

Router addition and deletion is done by clicking the left and middle mouse buttons on the canvas, respectively. In order for a new router to be created, entry field *Priority* needs to be filled out correctly. A linking of a router is done via right clicking a router and then right clicking a different router. This requires the entry filed *Speed* to be filled out correctly.

After a new router is created and added to the network, it is drawn to the canvas as a sphere with two additional information, its router id(IPv4 address) and its network index (a number from 1 to 254). There is also a color assigned to the sphere: __Red__, if the router is a chosen to be a *Dedicated router*(DR), __blue__, if the router is chosen as a *backup dedicated router*(BDR) and finally __grey__, if the router is chosen to be neither.

## Back end
Everything happens in the *Network* class. Whenever a new router is added, the *Network* adds it a its list of routers. After that, these steps are taken:
- Is there a DR or a BDR on the network?
    - if yes, these routers then establish first a neighbor relationship and then adjacency with the new router. This means, that they first exchange Hello packets, which makes them neighbors. After that, the new router asks for a database description from the DR. After exchanging and synchronizing their databases, the new router is now a part of the network. As a final step, each router is then synchronized with the DR and, in turn, with the new router.
    - if no, a DR and BDR are attempted to be elected. If the election succeeds, the process described above will take place. If the election fails however, all the routers will become neighbors and adjacencies.

If a router is removed, a synchronization process will take place and the DR or BDR will notify all other routers that a router was destroyed. If a DR is removed, the BDR will assume its place, and the election for a new BDR will take place. If a BDR is removed, an election for a new BDR will take place.

## Router communication
All routers communicate with messages which should directly simulate the data structures(packets) used by the RFC. Complete simulation is not possible, because of the language constraints of python as well as the overall complexity this would bring to this project. Instead, only a partial simulation and implementation of the different data structures required by the OSPF algorithm are used.

### Router class
Each router has its `Link State Database`, `Routing Table` and a list of `Neighbor`s. A neighbor relationship is established between two routers after a router receives a *Hello* message from another router. After becoming neighbors and after being allowed to link, the routers exchange `Link State Databse` information, so that every router has their databases synchronized. Each router then calculates its own `Routing Table`. A `Routing Table` consists of entries, where each entry has a destination router id, complete cost of the path to the destination router and the *"next  hop"*: the router id of the next router on the packets journey to the destination. Note, that in the [RFC](https://www.freesoft.org/CIE/RFC/1583/index.htm), for each IP Type of Service a different routing table is constructed and maintained, however this functionality is excluded from this simulation implementation of the shortest path first algorithm.

### Linking
After becoming neighbours, two routers stay idle. They form an *adjacent* relationship only if they are allowed to link via the GUI. They exchange link state requests and calculate and construct their routing tables as described in the above section. There is a single exception to this rule, however two routers become adjacent by default, if one of them is either a *Dedicated Router* or a *Backup Dedicated Router*. These routers won't stay idle, they will form an adjacency instantly.

# Docs
Each class is documented and the source code is meant to be readable and easily understandable.
