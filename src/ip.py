#!/usr/bin/env python3

from typing import Optional


class IpAddress:
    """
    A simple handler for all work related to working with and displaying IPv4
    addresses.
    """
    def __init__(self, n: Optional[int] = None, string: Optional[str] = None) -> None:
        """
        Create a new IpAddress object from either a string or an integer.
        """
        self._num: int
        if not n and not string:
            ip = IpAddress.int_from_str("192.168.0.1")
            if ip:
                self._num = ip
        if not n and string:
            ip = IpAddress.int_from_str(string)
            if ip:
                self._num = ip
        else:
            if n:
                self._num = n

    def get(self) -> int:
        """
        Return the underlying 32-bit number(0x01010101)
        """
        return self._num

    def to_str(self) -> str:
        """
        Turn the number into a string representation(1.1.1.1).
        """
        ip = IpAddress.str_from_int(self._num)
        if ip:
            return ip
        return "error"

    def __add__(self, o: int):
        if self._num & 0xff + o <= 255:
            self._num += o
        return IpAddress(n=self._num)
    
    def __int__(self) -> int:
        return self._num

    @classmethod
    def int_from_str(cls, s: str) -> Optional[int]:
        """
        Create a string version of an IPv4 address from a 32-bit integer.
        """
        nums = []
        for c in s.split("."):
            num: int
            try:
                num = int(c)
            except ValueError:
                print(f"[ERROR] invalid integer value {c}")
                return None
            if num > 255 and num < 0:
                print(f"[ERROR] {c} is not within the range of unsigned 8 bit integer!")
                return None
            nums.append(num)
        if len(nums) == 4:
            return (nums[3] | (nums[2] << 24) | (nums[1] << 16) | nums[0] << 8)

    @classmethod
    def str_from_int(cls, i: int) -> Optional[str]:
        """
        Create a string version of a IPv4 address, given a 32-bit integer.
        """
        mask = 0xff

        a, b, c, d = i, i, i, i

        a >>= 8
        a &= mask
        b >>= 16
        b &= mask
        c >>=24
        c &= mask
        d &= mask

        return f"{a}.{b}.{c}.{d}"
