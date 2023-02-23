from hexgame.src.board import Board
from hexgame.src.conncomp import ConnComp, ConnCompSet
# from hexgame.src.cell import Cell
# from hexgame.src.color import Color
import pytest


class TestConnComp:

    def test_zero_comp(self):

        cc_set = ConnCompSet({})

        node_target = (0, 1)
        neighbours = {}

        assert len(cc_set) == 0
        cc_set.update_conn_comp(node_target, neighbours)
        assert len(cc_set) == 1
        assert len(cc_set._conn_comp_dict) == 1
        assert node_target in cc_set._conn_comp_dict.keys()
        assert cc_set._conn_comp_dict[node_target].id == 0
        assert len(cc_set._conn_comp_dict[node_target].members) == 1

    def test_one_node_is_neighbour_comp(self):
        n = (0, 0)
        cc = ConnComp(1, {n})
        cc_set = ConnCompSet({n: cc})

        node_target = (0, 1)
        neighbours = {}
        cc_set.update_conn_comp(node_target, neighbours)
        assert len(cc_set._conn_comp_dict) == 2
        assert len(cc_set) == 2
        assert node_target in cc_set._conn_comp_dict.keys()
        assert n in cc_set._conn_comp_dict.keys()
        assert len(cc_set._conn_comp_dict[n].members) == 1
        assert len(cc_set._conn_comp_dict[node_target].members) == 1

    def test_one_node_is_not_neighbour_comp(self):
        n = (0, 0)
        cc = ConnComp(1, {n})
        cc_set = ConnCompSet({n: cc})

        node_target = (0, 1)
        neighbours = {n}
        cc_set.update_conn_comp(node_target, neighbours)
        assert len(cc_set._conn_comp_dict) == 2

        assert len(cc_set) == 1
        assert node_target in cc_set._conn_comp_dict.keys()
        assert n in cc_set._conn_comp_dict.keys()
        assert len(cc_set._conn_comp_dict[n].members) == 2
        assert len(cc_set._conn_comp_dict[node_target].members) == 2

    def test_basic_comp(self):
        n_1 = (0, 0)
        n_2 = (1, 0)
        n_3 = (2, 0)
        n_4 = (3, 0)
        n_5 = (4, 0)

        cc_1 = ConnComp(1, {n_1, n_2, n_3})
        cc_2 = ConnComp(2, {n_4, n_5})

        cc_set = ConnCompSet({n_1: cc_1,
                              n_2: cc_1,
                              n_3: cc_1,
                              n_4: cc_2,
                              n_5: cc_2})

        node_target = (0, 1)
        neighbours = {n_1, n_5}

        assert len(cc_set) == 2
        cc_set.update_conn_comp(node_target, neighbours)
        for x in cc_set._conn_comp_dict[n_1].members:
            print(x)
        print("\n")
        for x in cc_set._conn_comp_dict[n_2].members:
            print(x)
        print("\n")
        for x in cc_set._conn_comp_dict[n_3].members:
            print(x)
        print("\n")
        for x in cc_set._conn_comp_dict[n_4].members:
            print(x)
        print("\n")
        for x in cc_set._conn_comp_dict[n_5].members:
            print(x)
        print("\n")
        for x in cc_set._conn_comp_dict[node_target].members:
            print(x)

        assert len(cc_set) == 1
