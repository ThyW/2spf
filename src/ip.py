#!/usr/bin/env python3

from typing import Optional


class IpAddress:
    def __init__(self, num: Optional[int] = None, string: Optional[str] = None) -> None:
        self.num: int
        if not num and not string:
            ip = IpAddress.int_from_str("192.168.0.1")
            if ip:
                self.num = ip
        if not num and string:
            ip = IpAddress.int_from_str(string)
            if ip:
                self.num = ip
        else:
            if num:
                self.num = num

    def get(self) -> int:
        return self.num

    def to_str(self) -> str:
        ip = IpAddress.str_from_int(self.num)
        if ip:
            return ip
        return "error"

    def __add__(self, o: int):
        if self.num & 0xff + o <= 255:
            self.num += o
        return IpAddress(num=self.num)
    
    def __int__(self) -> int:
        return self.num

    @classmethod
    def int_from_str(cls, s: str) -> Optional[int]:
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
