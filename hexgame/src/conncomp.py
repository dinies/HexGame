from typing import TypeVar, Generic
T = TypeVar('T')

""" conncomp.py Contains classes that implement the connected com
ponent set data structure needed to implement the function that cheks
if Hex game is finished"""


class ConnComp(Generic[T]):
    """
    A connected component is a set of element of type T
    enriched with a id
    """

    def __init__(self, id: int, members: set[T]) -> None:
        self.id = id
        self.members = members

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.members == other.members

    def __hash__(self):
        return self.id.__hash__()

    def __repr__(self) -> str:
        return str(self.id)


class ConnCompSet(Generic[T]):
    """
    A Connected Component Set is a data structure that can hold
    the set of connected components of a graph and can efficiently
    be updated when a new node is added together with its edges to
    existing nodes in the graph


    | Implementation

    The data structure at its heart stores the connected components
    in a dictionary that maps nodes of type T to connected component 
    obects


    """

    def __init__(self, _conn_comp_dict: dict[T, ConnComp[T]] = {}):
        self._conn_comp_dict: dict[T, ConnComp[T]] = _conn_comp_dict

    def __getitem__(self, key: T) -> ConnComp[T]:
        return self._conn_comp_dict[key]

    def __setitem__(self, key: T, value: ConnComp[T]) -> None:
        self._conn_comp_dict[key] = value

    def __repr__(self) -> str:
        return repr(self._conn_comp_dict)

    def update_conn_comp(self, node: T, nbrs: set[T]) -> None:
        """                
            The idea behind the algorithm is simple, and can be generalised
            for any graph that is updated with a new node and its neighbours
            in the existing graph

            For example, let's say we have 5 red cells on board, let's call them:

            A,B,C,D,E

            Let's say that , because of their edges, they can be separated in
            connected components as:

            { {A,C,E} , {B} , {D} }

            Now, when we add a new node F, and F has the following connections:
            F - B ; F - E

            Then the updated components set will be updated by unioning all the
            single connected compontes that F is connected to plus F itself,
            thus we will end up with :

            { {A,C,E,F,B} , {D} }

        """
        # 1. first create a new conn component witht he singleton set
        # containing the new node and with id to the current number of
        # components plus one, and add this to the conn comp dict

        new_conn_comp = ConnComp(id=len(self) + 1, members={node})
        self[node] = new_conn_comp
        for nbr in nbrs:
            # 2. Then replace for each neighbour of the node
            # the existing conn component to the newly created one
            # and set the new members of this conn component to be the
            # current members union the nbr itself
            olc_nbr_comp = self[nbr]
            self[nbr] = new_conn_comp
            self[nbr].members = olc_nbr_comp.members.union(
                new_conn_comp.members)
            # TODO:use a Union-Find datasctructur
            # very sub-optimal but want to get something working
            for mem in self[nbr].members:
                self[mem] = new_conn_comp
        self.reorder_ids()

    @property
    def conn_comp_set(self) -> set[ConnComp[T]]:
        """
        The underlying data structure for a conn comp set is
        a dict i.e.:

        """
        return set(self._conn_comp_dict.values())

    def __len__(self):
        return len(self.conn_comp_set)

    def reorder_ids(self) -> None:
        no_comps = len(self)
        conn_comp_set = self.conn_comp_set
        conn_comp_set_ids = {comp.id for comp in conn_comp_set}
        mapping = dict(zip(conn_comp_set_ids, range(no_comps)))
        self._conn_comp_dict = {k: ConnComp(
            mapping[v.id], v.members) for k, v in self._conn_comp_dict.items()}


if __name__ == "__main__":
    conncompset = ConnCompSet()
    print(conncompset._conn_comp_dict)
    conncompset.update_conn_comp(node=(0, 0), nbrs=set())
    print(conncompset._conn_comp_dict[(0, 0)].members)
    print(conncompset._conn_comp_dict)
    print(len(conncompset))

    conncompset.update_conn_comp((1, 0), nbrs=set([(0, 0)]))
    print(conncompset._conn_comp_dict)
    print(conncompset._conn_comp_dict[(0, 0)].members)
    print(len(no_comps))

    conncompset.update_conn_comp((1, 1), set(''))
    print(conncompset._conn_comp_dict)
    print(conncompset.conn_comp_set)
    print(conncompset._conn_comp_dict[(1, 1)].members)
    print(len(no_comps))
