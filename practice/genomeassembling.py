import unittest
from copy import deepcopy
from random import random


class Graph:
    def __init__(self, adjacency_list={}):
        self.adjacency_list = deepcopy(adjacency_list)

    def __str__(self):
        return f"{self.adjacency_list}"

    """Returns list of neighbors for a given node"""

    def get_neighbors(self, node):
        return self.adjacency_list[node]

    def num_neighbors(self, node):
        return len(self.get_neighbors(node))

    def add_node(self, node):
        self.adjacency_list[node] = []

    def remove_node(self, node):
        del self.adjacency_list[node]

        for key, items in self.adjacency_list.items():
            self.adjacency_list[key] = [neigh for neigh in items if neigh != node]

    def in_degree(self, node):
        degree = 0
        for _, items in self.adjacency_list.items():
            for item in items:
                if item == node:
                    degree += 1

        return degree

    def out_degree(self, node):
        return self.num_neighbors(node)

    def outbound_edges(self, node):
        edges = [(node, neighbor) for neighbor in self.get_neighbors(node)]
        return edges

    def inbound_edges(self, node):
        edges = []
        for key, items in self.adjacency_list.items():
            for item in items:
                if item == node:
                    edges.append((item, node))

        return edges

    def get_all_edges(self):
        edges = set([])
        for key, items in self.adjacency_list.items():
            for item in items:
                edges.add((key, item))

        return edges

    def get_unvisited_edges(self, node, unvisited_edges):
        node_edges = self.outbound_edges(node)
        return list(set(node_edges).intersection(set(unvisited_edges)))

    def eulerian_cycle(self):
        current_node = list(self.adjacency_list.keys())[0]
        unvisited_edges = self.get_all_edges()

        unvisited_edges_for_node = self.get_unvisited_edges(
            current_node, unvisited_edges
        )
        cycle = [current_node]

        while len(unvisited_edges) > 0:

            while len(unvisited_edges_for_node) > 0:
                edge = unvisited_edges_for_node[0]
                unvisited_edges.remove(edge)

                current_node = edge[1]
                cycle.append(current_node)
                unvisited_edges_for_node = self.get_unvisited_edges(
                    current_node, unvisited_edges
                )

            for i in range(len(cycle)):
                node = cycle[i]
                unvisited_edges_for_node = self.get_unvisited_edges(
                    node, unvisited_edges
                )
                if len(unvisited_edges_for_node) > 0:
                    cycle = cycle[i:] + cycle[1 : i + 1]
        return cycle

    def add_neighbor(self, node, neighbor):
        self.adjacency_list[node].append(neighbor)

    def is_simple(self):
        for key in self.adjacency_list.keys():
            if len(self.inbound_edges(key)) > 1:
                return False
        return True

    def bypass(self, u, v, w):
        x = f"{v}_{random()}"

        self.adjacency_list[u].remove(v)
        self.adjacency_list[v].remove(w)

        self.add_node(x)
        self.add_neighbor(u, x)
        self.add_neighbor(x, w)

    def is_connected(self):
        for key in self.adjacency_list.keys():
            visited = set([])
            stack = [key]

            while len(stack) > 0:
                node = stack.pop()
                visited.add(node)
                for neighbor in self.get_neighbors(node):
                    if neighbor not in visited:
                        stack.append(neighbor)

            if len(visited) != len(self.adjacency_list.keys()):
                return False

        return True

    def all_eulerian_cycles(self):
        graphs = [self]
        cycles = []

        while True:
            non_simple_graph = None
            for graph in graphs:
                if not graph.is_simple():
                    non_simple_graph = graph
                    break

            if non_simple_graph is None:
                break

            non_simple_node = None
            for node in non_simple_graph.adjacency_list.keys():
                if len(non_simple_graph.inbound_edges(node)) > 1:
                    non_simple_node = node

            outbound_edges = non_simple_graph.outbound_edges(non_simple_node)
            inbound_edges = non_simple_graph.inbound_edges(non_simple_node)

            for u, v in inbound_edges:
                for v, w in outbound_edges:
                    if u == v and v == w:
                        continue
                    new_graph = Graph(deepcopy(non_simple_graph.adjacency_list))
                    new_graph.bypass(u, v, w)
                    if new_graph.is_connected():
                        graphs.append(new_graph)

            graphs.remove(non_simple_graph)

        for graph in graphs:
            cycles.append(graph.eulerian_cycle())

        return cycles


class DeBruijn(Graph):
    def __init__(self, reads, k):
        pass


class TestDeBruijn(unittest.TestCase):

    def make_graph(self):
        G = {
            "A": ["B"],
            "B": ["C", "E"],
            "C": ["D"],
            "D": ["B", "A"],
            "E": ["G", "F"],
            "F": ["G"],
            "G": ["D", "E"],
        }
        return G

    def test_eulerian_cycle(self):
        g = Graph(self.make_graph())

        self.assertEqual(
            ["E", "G", "D", "A", "B", "C", "D", "B", "E", "F", "G", "E"],
            g.eulerian_cycle(),
        )

    def test_simple_eulerian_cycle(self):
        adjacency_list = {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]}
        g = Graph(adjacency_list)

        self.assertEqual(["A", "B", "C", "D"], g.eulerian_cycle())

    def test_is_connected_for_connected_graph(self):
        adjacency_list = {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]}
        g = Graph(adjacency_list)

        self.assertTrue(g.is_connected())

    def test_is_connected_for_disconnected_graph(self):
        adjacency_list = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
        g = Graph(adjacency_list)

        self.assertFalse(g.is_connected())

    def test_de_bruijn_cycles(self):
        reads = ["TAATGCCATGGGATGTT"]
        dg = DeBruijn(reads, k=3)
        dg.close_to_cycle()
        # print(dg.all_eulerian_cycles())
        print("Maximal Non Branching Paths: ")
        print(dg.maximal_non_branching_paths())

    def test_all_eulerian_cycles(self):
        g = Graph(self.make_graph())
        print("all Eulerian cycles: ")
        print(g.all_eulerian_cycles())

    def test_out_degree(self):
        g = Graph(self.make_graph())
        self.assertEqual(2, g.out_degree("G"))

    def test_inbound_edge(self):
        g = Graph(self.make_graph())

    def test_outbound_edge(self):
        g = Graph(self.make_graph())
        self.assertEqual([("D", "B"), ("D", "A")], g.outbound_edges("D"))

    def test_all_edges(self):
        print(Graph(self.make_graph()).get_all_edges())

    def test_in_degree(self):
        g = Graph(self.make_graph())
        self.assertEqual(2, g.in_degree("B"))

    def test_debrujin(self):
        reads = ["AATT"]
        dg = DeBruijn(reads=reads, k=3)
        self.assertEqual("{'AA': ['AT'], 'AT': ['TT']}", str(dg))

    def test_get_neighbors(self):
        g = Graph(self.make_graph())
        self.assertEqual(["B", "A"], g.get_neighbors("D"))

    def test_num_neighbors(self):
        g = Graph(self.make_graph())
        self.assertEqual(2, g.num_neighbors("D"))

    def test_add_node(self):
        g = Graph(self.make_graph())
        g.add_node("X")
        self.assertEqual([], g.get_neighbors("X"))

    def test_remove_node(self):
        g = Graph(self.make_graph())
        g.remove_node("A")
        self.assertEqual(
            str(
                {
                    "B": ["C", "E"],
                    "C": ["D"],
                    "D": ["B"],
                    "E": ["G", "F"],
                    "F": ["G"],
                    "G": ["D", "E"],
                }
            ),
            str(g),
        )

    def test_out_degree(self):
        g = Graph(self.make_graph())


if __name__ == "__main__":
    unittest.main()
