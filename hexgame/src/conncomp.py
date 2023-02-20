"""
conncomp.py set of utility function to store 
and compute conected components of a graph
"""

from hexgame.src.cell import Cell

__author__ = "Gianpiero Cea"


class ConnectedComponentSet:
    def __init__(self, conn_comp: set[set[Cell]]) -> 'ConnectedComponentSet':
        self._conn_comp = conn_comp

    def _update_connected_components(self, new_placed_cell: Cell) -> 'ConnectedComponentSet':
        """
        Given a new placed cell it recomputes the relevant connected components
        data structure (either the Red or Blue one)

        The idea behind the algorithm is simple, and can be generalised
        for any graph that is updated with a new node and edges
        from that node to the previous nodes

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
        # TODO: maybe create a class for connected component as this
        # seems a complex enough idea

        color = new_placed_cell.color

        # 1.a find the neihgbours of the new placed cell
        #   of the same color

        # 1.b For each of those neighours, find the connected component in
        # which they lie, if it exists

        same_color_nbrs = {self._get_connected_comp(cell) for cell in self.find_neighbours(
            (new_placed_cell.x, new_placed_cell.y)) if cell.color == color}

    def _get_connected_comp(self, cell: Cell) -> set[Cell]:
        """
        Returns as a set of Cells the current connected
        component in which the cell lies

        """
        color = cell.color
        connected_components = self._connected_components[color]
        conn_comps_for_cell = [
            comp for comp in connected_components if cell in comp]

        # There should be exactly a single conn component
        if len(conn_comps_for_cell) != 1:
            raise ValueError(
                "Attempted to find a connected component for not found cell")

        return conn_comps_for_cell[0]
