# TODO: This needs to be implemented...
from typing import Generic, Optional, TypeVar, List


LTE = TypeVar("LTE")

class HeapNode(Generic[LTE]):
    def __init__(self, data: LTE) -> None:
        self._data = data

    def __le__(self, other: "HeapNode") -> bool:
        return self._data <= other._data


class Heap(Generic[LTE]):
    def __init__(self) -> None:
        self._data: List[HeapNode[LTE]] = list()
        self._index: int = -1

    def push(self, element: LTE) -> None:
        # 1. Add the element to the bottom level of the heap at the leftmost
        # open space.
        node = HeapNode(element)
        self._data.append(node)
        self._index += 1

        # 2. Compare the added element with its parent; if they are in the
        # correct order, stop.
        index = self._index
        parent_index = (index - 1) // 2
        while not self._data[parent_index] <= self._data[index]:
            # 3. If not, swap the element with its parent and return to the
            # previous step.
            self._swap(index, parent_index)
            index = parent_index
            parent_index = (index) // 2

    def pop(self) -> Optional[LTE]:
        if not self._data:
            return
        # 1. Replace the root of the heap with the last element on the last 
        # level.
        temp = self._data[0]
        self._data[0] = self._data[-1]
        self._data[-1] = temp
        del self._data[-1]
        self._index -=  1

        if len(self) < 2:
            x = self._data.pop(0)
            self._index -= 1
            return x._data 

        root = 0
        c1 = (2 * root) + 1
        c2 = (2 * root) + 2
        # 2. Compare the new root with its children; if they are in the correct
        # order, stop.
        if c1 > len(self) - 1:
            return temp._data
        if c2 > len(self) - 1:
            c2 = c1
        while self._data[c1] <= self._data[root]\
            or self._data[c2] <= self._data[root]:
                # 3. If not, swap the element with one of its children and
                # return to the previous step. (Swap with its smaller child in 
                # a min-heap and its larger child in a max-heap.)
                if self._data[c1] <= self._data[root]:
                    self._swap(root, c1)
                    root = c1
                    c1 = (2 * root) + 1
                    c2 = (2 * root) + 2
                    if c1 > len(self) - 1:
                        break
                    if c2 > len(self) - 1:
                        c2 = c1
                if self._data[c2] <= self._data[root]:
                    self._swap(root, c2)
                    root = c2
                    c1 = (2 * root) + 1
                    c2 = (2 * root) + 2
                    if c1 > len(self) - 1:
                        break
                    if c2 > len(self) - 1:
                        c2 = c1
        return temp._data

    def peek(self) -> Optional[LTE]:
        if self._data:
            return self._data[0]._data
        return None

    def get_data(self) -> List[LTE]:
        return [x._data for x in self._data]

    def is_empty(self) -> bool:
        if len(self) == 0:
            return True
        return False

    def _swap(self, n1: int, n2: int) -> None:
        # FIXME: maybe make this look a bit better?
        temp = self._data[n1]
        self._data[n1] = self._data[n2]
        self._data[n2] = temp

    def __len__(self) -> int:
        return len(self._data)

    @classmethod
    def from_list(cls, input: List[LTE]) -> "Heap":
        heap = Heap()
        [heap.push(n) for n in input]
        return heap


def tests():
    print("[TESTING] src/heap.py")
    t_push()
    t_pop()


def t_push():
    # part 1
    h = Heap.from_list([1, 2, 3, 4, 5])
    res = [1, 2, 3, 4, 5]
    print(f"[ASSERT] {h.get_data()} == {res}")
    assert h.get_data() == res

    # part 2
    h = Heap.from_list([51, 100, 1, 23, 200])
    res = [1, 23, 51, 100, 200]
    print(f"[ASSERT] {h.get_data()} == {res}")
    assert h.get_data() == res

    print("[PASSED] test: t_push")


def t_pop():
    h = Heap.from_list([51, 100, 1, 23, 200])
    res = h.pop()
    print(f"[ASSERT] {1} == {res}")
    assert res == 1

    res = [23, 100, 51, 200]
    print(f"[ASSERT] {h.get_data()} == {res}")
    assert h.get_data() == res

    print("[PASSED] test: t_pop")
