from copy import deepcopy


class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def __str__(self):
        return f"{self.adjacency_list}"

    def get_neighbors(self, node):
        return self.adjacency_list[node]

    def num_neighbors(self, node):
        return len(self.get_neighbors(node))

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]

        for key, neighbors in self.adjacency_list.items():
            self.adjacency_list[key] = [n for n in neighbors if n != node]

    def in_degree(self, node):
        counter = 0
        for _, nghs in self.adjacency_list.items():
            for ng in nghs:
                if ng == node:
                    counter += 1

        return counter

    def out_degree(self, node):
        return self.num_neighbors(node)

    def outbound_edges(self, node):
        neighbors = self.get_neighbors(node)
        edges = [(node, neighbor) for neighbor in neighbors]
        return edges

    def inbound_edges(self, node):
        edges = []
        for key, neighbors in self.adjacency_list:
            for neighbor in neighbors:
                if neighbor == node:
                    edges.append((key, node))

    def get_all_edges(self):
        all_edges = []
        for key in self.adjacency_list.keys():
            all_edges += self.outbound_edges(key)

        return all_edges

    def get_unvisited_edges(self, node, unvisited_edges):
        node_unvisited_edges = []
        node_edges = self.outbound_edges(node)
        for node_edge in node_edges:
            for unvisited_edge in unvisited_edges:
                if unvisited_edge == node_edge:
                    node_unvisited_edges.append(unvisited_edge)

        return node_unvisited_edges

    def eulerian_cycle(self):
        current_node = list(self.adjacency_list.keys())[0]
        unvisited_edges = self.get_all_edges()
        unvisited_edges_from_current_node = self.get_unvisited_edges(
            current_node, unvisited_edges
        )
        cycle = [current_node]

        while len(unvisited_edges) > 0:
            while len(unvisited_edges_from_current_node) > 0:
                current_edge = unvisited_edges_from_current_node[0]
                (from_node, to_node) = current_edge

                unvisited_edges.remove(current_edge)

                cycle.append(to_node)

                current_node = to_node
                unvisited_edges_from_current_node = self.get_unvisited_edges(
                    current_node, unvisited_edges
                )

            for i in range(len(cycle)):
                current_node = cycle[i]
                unvisited_edges_from_current_node = self.get_unvisited_edges(
                    current_node, unvisited_edges
                )
                if len(unvisited_edges_from_current_node) > 0:
                    cycle = cycle[i:] + cycle[1 : i + 1]

        return cycle


class DeBrujin(Graph):
    def __init__(self, reads, k):
        kmers = self.get_kmers(reads, k)  # array of triples
        adjacency_list = {}

        for kmer in kmers:
            u = kmer[:-1]
            v = kmer[1:]
            if u not in adjacency_list:
                adjacency_list[u] = []

            if v not in adjacency_list:
                adjacency_list[u] = []

            adjacency_list[u].append(v)

        super().__init__(adjacency_list=adjacency_list)

    def get_kmers(self, reads, k):
        kmers = []
        for read in reads:
            n = len(read)
            for i in range(n - k + 1):
                kmer = read[i : i + k]
                kmers.append(kmer)
        return kmers


import unittest


class TestDebrujin(unittest.TestCase):

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
        dg = DeBrujin(reads=reads, k=3)
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
