#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class LSType(Enum):
    """
    Type of link.
    """
    ROUTER = 1
    NETWORK_LINKS = 2
    SUMMARY_LINK_IP = 3
    SUMMARY_LINK_ASBR = 4
    AS_EXTERNAL_LINK = 5


@dataclass
class LSAHeader:
    """
    Link State Advertisement header.

    ---
    Attributes:
    ---
    * ls_age: int : the age of the advertisement, the larger the number is, the
      advertisement is. IGNORED
    * options: int : router's options as per its configuration. IGNORED
    * ls_type: int : type of the link. ALWAYS 1(ROUTER)
    * advertising_router: int : router ID of the advertising router.
    * ls_seq_num: int : sequence number of the link state advertisement, the
      larger this number is, the newer it is. IGNORED
    * ls_checksum: int : checksum of the entire link state advertisement.
      IGNORED
    * length: int : link state advertisement's length in bytes. IGNORED
    """
    ls_age: int  # ignore
    options: int # router options, can be filled but are ignored
    ls_type: int # always 1
    ls_id: int   # router id
    advertising_router: int # router id
    ls_seq_num: int # increment from 0
    ls_checksum: int # ignore
    length: int # ignore


@dataclass
class RLABody:
    """
    Body of a Router Link Advertisement.

    ---
    Attributes:
    ---
    * link_id: int : router ID of the router this link points to.
    * link_data: int : changes depending on the type of the advertisement,
      since we only work with routers, this is always the unique index of the
      router we are linking to.
    * num_tos_metrics: int : number of metrics for the given link. ALWAYS 0
    * tos_zero: int : default cost for all services.
    * tos_and_metric: Dict[int, int] : Service ID and metric(cost) for the
      service. ALWAYS EMPTY
    """
    link_id: int # router id of the router that is being linked to
    link_data: int # ifIndex of the router
    num_tos_metrics: int # 0
    tos_zero: int # link cost
    tos_and_metric: Dict[int, int] # ignore


@dataclass
class RouterLinkAdvertisement(LSAHeader):
    """
    Router Link State Advertisement.

    ---
    Attributes:
    ---
    * v_b: bool : router is an endpoint of a virtual link. IGNORED
    * e_b: bool : router is an AS boundary router. IGNORED
    * b_b: bool : router is an area border router. IGNORED
    * num_links: int: number of links advertised. ALWAYS 1
    * bodies: List[RLABody] : list of all advertised links.
    """
    v_b: bool # ignore
    e_b: bool # ignore
    b_b: bool # ignore
    num_links: int # number of links in a single advertisement
    bodies: List[RLABody] # list of *num_links* link bodies


LinkStateAdvertisement = RouterLinkAdvertisement
