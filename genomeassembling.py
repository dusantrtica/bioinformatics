from copy import deepcopy
from random import random


class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = deepcopy(adjacency_list)

    def __str__(self):
        return f"{self.adjacency_list}"

    """Returns list of neighbors for a given node"""

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
        for key, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                if neighbor == node:
                    edges.append((key, node))

        return edges

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

    def add_neighbor(self, node, neighbor):
        self.adjacency_list[node].append(neighbor)

    def bypass(self, u, v, w):
        x = f"{v}-{random()}"

        self.adjacency_list[u].remove(v)
        self.adjacency_list[v].remove(w)
        self.add_node(x)

        self.add_neighbor(u, x)
        self.add_neighbor(x, w)

    """Checks whether the graph is simple - is simple there is no node
    which has more than one inbound edge"""

    def is_simple(self):
        for key in self.adjacency_list.keys():
            if self.in_degree(key) > 1:
                return False
        return True

    """Does DFS for every single node and checks if all nodes are accessible from that one"""

    def is_connected(self):
        total_num_nodes = len(self.adjacency_list)
        for key in self.adjacency_list:
            stack = [key]
            visited = set([])

            while len(stack) > 0:
                node = stack[-1]
                visited.add(node)
                has_unvisited_neighbor = False
                for neighbor in self.get_neighbors(node):
                    if neighbor not in visited:
                        has_unvisited_neighbor = True
                        stack.append(neighbor)

                if not has_unvisited_neighbor:
                    stack.pop()

            if len(visited) != total_num_nodes:
                return False

        return True

    def get_unbalanced(self):
        unbalanced = []
        for key in self.adjacency_list:
            if self.in_degree(key) != self.out_degree(key):
                unbalanced.append(key)

        return unbalanced

    def close_to_cycle(self):
        [u, v] = self.get_unbalanced()
        if self.in_degree(u) > self.out_degree(u):
            self.add_neighbor(u, v)
        else:
            self.add_neighbor(v, u)

    def all_eulerian_cycles(self):
        all_graphs = [self]
        while True:
            non_simple_g = None
            for g in all_graphs:
                if not g.is_simple():
                    non_simple_g = g
                    break
            if non_simple_g == None:
                break

            non_simple_node = None
            # trazimo ulazni cvor koji ima stepen veci od jedan
            # sad ga bajpasujemo, tj. izravnavamo ga
            for key in non_simple_g.adjacency_list.keys():
                if non_simple_g.in_degree(key) > 1:
                    non_simple_node = key

            inbound_e = non_simple_g.inbound_edges(non_simple_node)
            outbound_e = non_simple_g.outbound_edges(non_simple_node)

            for u, v in inbound_e:
                for v, w in outbound_e:
                    if u == v and u == w:
                        continue  # grana koja ide u isti cvor, preskacemo.
                    new_graph = Graph(deepcopy(non_simple_g.adjacency_list))
                    new_graph.bypass(u, v, w)

                    if new_graph.is_connected():
                        all_graphs.append(new_graph)

            all_graphs.remove(non_simple_g)

        cycles = []
        for g in all_graphs:
            cycle = g.eulerian_cycle()
            cycles.append(tuple([node.split("-")[0] for node in cycle]))

        deduplicated_cycles = set(cycles)

        return [list(cycle) for cycle in deduplicated_cycles]

    def maximal_non_branching_paths(self):
        paths = []
        visited = set([])
        for v in self.adjacency_list:
            # 1 in, 1 out
            v_in_deg = self.in_degree(v)
            v_out_deg = self.out_degree(v)
            if not (v_in_deg == 1 and v_out_deg) == 1:
                # konstruisemo putanju od ovog cvora, koji nije 1-1
                if v_out_deg > 0:
                    for v, w in self.outbound_edges(v):
                        non_branching_path = [v, w]
                        visited.add(v)
                        w_in_deg = self.in_degree(w)
                        w_out_deg = self.out_degree(w)

                        while w_in_deg == 1 and w_out_deg == 1:
                            [(w, u)] = self.outbound_edges(w)
                            non_branching_path.append(u)

                            visited.add(w)
                            w = u
                            w_in_deg = self.in_degree(w)
                            w_out_deg = self.out_degree(w)

                        paths.append(non_branching_path)

        for v in self.adjacency_list:
            if v not in visited:
                visited.add(v)

                non_branching_path = [v]
                neighbor = self.outbound_edges(v)
                while neighbor != None and neighbor[1] not in visited:
                    w = neighbor[1]
                    non_branching_path.append(w)
                    visited.add(w)
                    neighbor = self.outbound_edges(w)

                paths.append(non_branching_path)

        return paths


class DeBruijn(Graph):
    def __init__(self, reads, k):
        kmers = self.get_kmers(reads, k)  # array of triples
        adjacency_list = {}

        for kmer in kmers:
            u = kmer[:-1]
            v = kmer[1:]
            if u not in adjacency_list:
                adjacency_list[u] = []

            if v not in adjacency_list:
                adjacency_list[v] = []

            adjacency_list[u].append(v)

        super().__init__(adjacency_list)

    def get_kmers(self, reads, k):
        kmers = []
        for read in reads:
            n = len(read)
            for i in range(n - k + 1):
                kmer = read[i : i + k]
                kmers.append(kmer)
        return kmers


import unittest


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

    def test_de_bruijn_cycles(self):
        reads = ["TAATGCCATGGGATGTT"]
        dg = DeBruijn(reads, k=3)
        dg.close_to_cycle()
        # print(dg.all_eulerian_cycles())
        print("Maximal Non Branching Paths: ")
        print(dg.maximal_non_branching_paths())

    def test_all_eulerian_cycles(self):
        g = Graph(self.make_graph())
        # print(g.all_eulerian_cycles())

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
