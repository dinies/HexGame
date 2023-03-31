"""graph.py Represents a graph """
from typing import TypeVar, Generic, Optional
from hexgame.unionfind import UnionFind
T = TypeVar('T')
__author__ = "Gianpiero Cea"


class Graph(Generic[T]):
    def __init__(
            self, adjency: dict[T, list[T]] = {},
            conn_comps: Optional[UnionFind[T]] = None) -> None:
        self._adjency = adjency
        self._conn_comps = conn_comps if conn_comps else self.get_conn_comps()

    def __repr__(self) -> str:
        return str(self._adjency)

    def get_conn_comps(self) -> UnionFind[T]:
        """
        @returns: The connected components of this graph

        @implementation: goes through each new edge and
        updates the connected components by unioning nodes
        of the edge
        """
        # TODO: probably can be optimised further
        # with better traversal of graph
        conn_comps = UnionFind(list(self._adjency.keys()))
        edges: frozenset[frozenset[T]] = frozenset()
        for v, nbrs in self._adjency.items():
            for nbr in nbrs:
                new_edge = frozenset((v, nbr))
                if new_edge not in edges:
                    edges.union(frozenset((nbr, v)))

                    conn_comps.union(v, nbr)

        return conn_comps

    def add_edge(self, node1: T, node2: T) -> None:
        """
        Add an edge to current graph and incrementally
        updates its connected components
        """
        if node1 in self._adjency:
            self._adjency[node1].append(node2)
        else:
            self._adjency[node1] = [node2]
        if node2 in self._adjency:
            self._adjency[node1].append(node1)
        else:
            self._adjency[node2] = [node1]

        # TODO:rework unionfind to make it work incrementally
        self._conn_comps = self.get_conn_comps()

    def update_graph(self, node: T, nbrs: list[T]) -> None:
        if node in self._adjency:
            # TODO: this is horrible!!rewrite
            self._adjency[node] = list({el for el in self._adjency[node]+nbrs})
            self._conn_comps = self.get_conn_comps()
        else:
            pass
        raise NotImplementedError


if __name__ == "__main__":
    gph = Graph({'a': ['b', 'c'], 'b': ['a', 'd'],
                'c': ['a'], 'd': ['b'], 'e': [], 'f': []})
    print(gph)

    print(gph.get_conn_comps())
