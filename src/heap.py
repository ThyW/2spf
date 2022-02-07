# TODO: This needs to be implemented...
from typing import Generic, TypeVar, List

T = TypeVar("T")

class Heap(Generic[T]):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_list(cls, input: List[T]) -> "Heap":
        return Heap()
