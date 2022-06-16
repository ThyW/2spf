# About
`2spf` is a partial implementation of the OSPF network routing algorithm. It was made as a school coding project and supports:
- *Link State Databases*
    - each router has a link state database, which keeps track of all received link state advertisements.
- *Routing Tables*
    - each router has a routing table, which keeps track of all the calculated shortest paths in the network.
- *Hello packets(Hello messages)*
    - two routers become neighbors by sending each other so called *Hello* packets, this is simulated by two routers exchanging *Hello* messages.

## How it works
When running `main.py`, you will be greeted by a UI. White part of the screen, the canvas, is the part on which you can right click, left click and middle mouse click. Left clicking adds a device, either a router or a switch to the network, right clicking creates a link between two routers and middle clicking removes a router from the network, as well as removing each and every one of it's links.

This entry field takes a three(or two) letter string(can be upper or lower case, or both), which identifies the type of the link. These values are the same as the abbreviations stated above (`gei`, `ds1`, `dsl`, etc...).

When left clicking, a pop up window will be shown, asking you what kind of a device you would like to add to the network. All routers connected to a single switch act as a single OSPF area and will therefore choose a Dedicated Router and a Backup Dedicated Router. These are the two routers with the highest priority. When creating adding a router to the network, you will get another pop up asking you about the router id and its priority.

After you are satisfied with your network layout, you can then hit the `Consturct network` button in the lower part of the screen. This may have a bit of a lag, depending on how many links and routers you created. When the network is being constructed, a Dedicated router(red) and a Backup dedicated router(blue) will be elected. After the network's construction, series of animations will play, simulating the network traffic.

Once done, you can again restructure your network and rerun it again.

## Constructing the network.
All linked routers become neighbors and every link is translated into a *Link State Advertisement*. All advertisements are collected and distributed among the routers. Each router is than able to use the SPF(*shortest path first*) algorithm to create its routing table. After all this is done, the simulation will begin. Colorful animations of the network traffic will be displayed, simulating how network packets are routed on the network.

## Datastructures
This project uses `minheap` and data structures specified in the [OSPF v.2 RFC](https://www.freesoft.org/CIE/RFC/1583/index.htm).

## Documentation
Mostly all functions and classes are documented using python's docstrings.
