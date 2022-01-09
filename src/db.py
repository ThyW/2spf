#!/usr/bin/env python3

from typing import List, Optional
from .link_state import LinkStateAdvertisement

class LinkStateDatabase:
    """
    Database holding information about all link state advertisements recieved
    by the router.
    """
    def __init__(self) -> None:
        self._content: List[LinkStateAdvertisement] = list()

    def __getitem__(self, key: int) -> Optional[LinkStateAdvertisement]:
        for each in self._content:
            if each.ls_id == key:
                return each
        return None

    def add(self, adv: LinkStateAdvertisement) -> None:
        """
        Add a new link state advertisement to the link state database. 
        """
        self._content.append(adv)

    def remove(self, adv: LinkStateAdvertisement) -> None:
        """
        Remove a link state advertisement from the link state database.
        """
        for each in self._content:
            if each.ls_id == adv.ls_id:
                del each
