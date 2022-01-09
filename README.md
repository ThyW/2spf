# About
**2spf** is a partial implementation of the OSPF network routing algorithm. Partial, because only point-to-point and single area networks are supported, as well as only some parts of the protocol are supported and implemented (for example, the exchange process of database descriptions and the tedious process of two routers becoming neighbors). This is due to the overall complexity and un-necessity of the entire project. So let's get to the stuff that is supported and used:
- *Link State Databases*
    - each router has a link state database, which keeps track of all received link state advertisements.
- *Routing Tables*
    - each router has a routing table, which keeps track of all the calculated shortest paths in the network.
- *Hello packets(Hello messages)*
    - two routers become neighbors by sending each other so called *Hello* packets, this is simulated by the two routers exchanging *Hello* messages.

## How it works
When running `main.py`, you will be greeted by a UI. White part of the screen, the canvas, is the part on which you can right click, left click and middle mouse click. Left clicking adds a new router to the network, right clicking creates a link between two routers and middle clicking removes a router from the network, as well as removing each and every one of it's links. There is also a single entry field titled `Cost`. Here we can specify the cost of the link, as per the OSPF specification:
- Gigabit Ethernet Interface [1 Gbps] (GEI): 1
- Fast Ethernet Interface [100 Mbps] (FEI): 1
- Ethernet Interface [10 Mbps] (EI): 10
- DS1 [1.544 Mbps]: 64
- DSL [0.768 Mbps]: 133

This entry field takes a three(or two) letter string(can be upper or lower case, or both), which identifies the type of the link. These values are the same as the abbreviations stated above (`gei`, `ds1`, `dsl`, etc...).

After you are satisfied with your network layout, you can then hit the `Consturct network` button in the lower part of the screen. This may have a bit of a lag, depending on how many links and routers you created. This button then constructs the network.

## Constructing the network.
All linked routers become neighbors and every link is translated into a *Link State Advertisement*. All advertisements are collected and distributed among the routers. Each router is than able to use the SPF(*shortest path first*) algorithm to create its routing table. After all this is done, the simulation will begin. Colorful animations of the network traffic will be displayed, simulating how network packets are routed on the network. After all this is done, the program exits. A `--print` option can be specified when running `main.py`, which will also print information above each link and each path to the standard output.

## Datastructures
Min heap and also data structures specified in the [OSPF v.2 RFC](https://www.freesoft.org/CIE/RFC/1583/index.htm).
