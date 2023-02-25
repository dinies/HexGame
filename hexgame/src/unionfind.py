"""unionfind.py implements a union find data structure"""
from typing import TypeVar, Generic
T = TypeVar('T')
__author__ = "Gianpiero Cea"


class UnionFind(Generic[T]):
    """
    A union find is a data strcutre to store a partition
    of a set into disjoint sets.

    This is what normally arises as the induced equivalence
    clases partition of an equivalence relation on a set, such
    as with the connected components of graph

    |METHODS

    | Union: merges two disjoint sets into a single one
    | Find: tells which of the disjoint sets a nonde belongs to
    |        by giving the name of its representative


    see: shorturl.at/flCN9
    """

    def __init__(self, nodes: list[T]) -> None:
        """
        |input
        nodes: the nods of the graph
        """
        # map each node to its parent
        # initialise to be itself
        self._parents: dict[T, T] = {node: node for node in nodes}
        # the size of node is the numner of descendants,including itself
        # only valid for a "root" node
        self._size: dict[T, int] = {node: 1 for node in nodes}
        self._counts: int = len(nodes)

    def __len__(self):
        return self._counts

    def __str__(self) -> str:
        return str(self._parents)

    def find(self, a: T) -> T:
        """
        Returns the  root of the component tree,
        which is taken to be as the representative of the
        disjoint set
        """
        parent = self._parents[a]
        # father is a father of itself iff is root
        # so while not reached root
        while parent != self._parents[parent]:
            # chase ancestors
            parent = self._parents[parent]
        # amortized code:
        # this is for speed
        while a != parent:
            newp = self._parents[a]
            self._parents[a] == parent
            a = newp

        return parent

    def union(self, a: T, b: T) -> None:
        """
        Given two nodes,it combines
        their connected components

        """
        root_a = self.find(a)
        root_b = self.find(b)

        # Weighted union:
        # for performance we make sure the deepest tree components
        # is always above

        if (root_a == root_b):
            return

        if (self._size[root_a] < self._size[root_b]):
            self._parents[root_a] = root_b
            self._size[root_b] += self._size[root_a]
        else:
            self._parents[root_b] = root_a
            self._size[root_a] += self._size[root_b]

        # we one component less
        self._counts -= 1


if __name__ == "__main__":
    uf = UnionFind([(0, 0), (1, 1), (1, 0), (2, 1)])
    print(len(uf))
    uf.union((1, 0), (2, 1))
    print(len(uf))
    uf.union((1, 1), (2, 1))
    print(len(uf))
    print(uf._parents)
