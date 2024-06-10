class GenomeGraph:
    def __init__(self, edges):
        self.edges = edges
        self.adjacency_list = {}
        for u, v in edges:
            if u not in self.adjacency_list:
                self.adjacency_list[u] = []
            if v not in self.adjacency_list:
                self.adjacency_list[v] = []

            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)

    def __str__(self) -> str:
        return f"{self.adjacency_list}"

    def get_cycles(self):
        unvisited = set(self.adjacency_list.keys())
        cycles = []

        while len(unvisited) > 0:
            v = min(unvisited)
            current_cycle = [v]
            unvisited.remove(v)
            w = sorted(self.adjacency_list[v])[0]
            while w != v and w != None:
                unvisited.remove(w)
                current_cycle.append(w)
                first_unvisted = None
                for u in sorted(self.adjacency_list[w]):
                    if u in unvisited:
                        first_unvisted = u
                        break
                w = first_unvisted

            cycles.append(current_cycle)

        return cycles

    def add_edge(self, i, j):
        self.adjacency_list[i].append(j)
        self.adjacency_list[j].append(i)

    def remove_edge(self, i, j):
        self.adjacency_list[i].remove(j)
        self.adjacency_list[j].remove(i)

    def two_break_on_genome_graph(self, i, i_p, j, j_p):
        self.remove_edge(i, i_p)
        self.remove_edge(j, j_p)

        self.add_edge(i, j)
        self.add_edge(i_p, j_p)

        return self


class Reversals:
    def k_sorting_reversal(self, P, k):
        n = len(P)
        for i in range(k, n):
            if abs(P[i]) == k:
                P[k:i] = [-x for x in P[k:i][::-1]]
        return P

    def greedy_sorting(self, P):
        approx_reversal_distance = 0
        n = len(P)

        for k in range(n):
            if P[k] != (k + 1):
                P = self.k_sorting_reversal(P, k)
                approx_reversal_distance += 1

                if P[k] == -(k + 1):
                    P[k] *= -1
                    approx_reversal_distance += 1

        return approx_reversal_distance

    def chromosome_to_cycle(self, chromosome):
        n = len(chromosome)
        nodes = [0] * (2 * n)
        for j in range(n):
            i = chromosome[j]

            if i > 0:
                nodes[2 * j] = 2 * i - 1
                nodes[2 * j + 1] = 2 * i
            else:
                nodes[2 * j] = -2 * i
                nodes[2 * j + 1] = -2 * i - 1
        return nodes

    def cycle_to_chromosome(self, cycle):
        m = len(cycle)

        chromosome = [0] * (m // 2)
        for j in range(0, m, 2):
            if cycle[j] < cycle[j + 1]:
                chromosome[j // 2] = cycle[j + 1] // 2
            else:
                chromosome[j // 2] = -cycle[j] // 2

        return chromosome

    def colored_edges(self, P):
        edges = []
        for chromosome in P:
            nodes = self.chromosome_to_cycle(chromosome)
            m = len(nodes)

            for j in range(1, m - 1, 2):  # da bismo poslednji spojli sa prvim
                edges.append((nodes[j], nodes[j + 1]))
            edges.append((nodes[-1], nodes[0]))

        return edges

    def black_edges(self, P):
        edges = []
        for chromosome in P:
            nodes = self.chromosome_to_cycle(chromosome)
            m = len(nodes)

            for j in range(0, m, 2):  # da bismo poslednji spojli sa prvim
                edges.append((nodes[j], nodes[j + 1]))

        return edges

    def graph_to_genome(self, genome_graph):
        P = []
        cycles = genome_graph.get_cycles()
        for cycle in cycles:
            chromosome = self.cycle_to_chromosome(cycle)
            P.append(chromosome)

        return P

    def two_break_on_genome(self, P, i, i_p, j, j_p):
        genome_graph = GenomeGraph(self.black_edges(P) + self.colored_edges(P))
        genome_graph.two_break_on_genome_graph(i, i_p, j, j_p)
        return self.graph_to_genome(genome_graph)

    def shortest_rearrangement_scenario(self, P, Q):
        red_edges = self.colored_edges(P)
        blue_edges = self.colored_edges(Q)

        breakpoint_graph = GenomeGraph(red_edges + blue_edges)

        while True:
            cycles = breakpoint_graph.get_cycles()
            non_trivial_cycle = None
            for cycle in cycles:
                if len(cycle) > 2:
                    non_trivial_cycle = cycle
            if non_trivial_cycle == None:
                break

            n = len(non_trivial_cycle)
            cycle_edges = [
                (non_trivial_cycle[i], non_trivial_cycle[i + 1]) for i in range(n - 1)
            ] + [(non_trivial_cycle[-1], non_trivial_cycle[0])]

            for k in range(n):
                edge = cycle_edges[k]
                (j_blue, i_p_blue) = edge
                if (j_blue, i_p_blue) in blue_edges or (i_p_blue, j_blue) in blue_edges:
                    previous_red_edge = cycle_edges[(k - 1) % n]
                    next_red_edge = cycle_edges[(k + 1) % n]
                    break

            (i, j) = previous_red_edge

            (i_p, j_p) = next_red_edge

            breakpoint_graph.remove_edge(i, j)
            breakpoint_graph.remove_edge(i_p, j_p)

            breakpoint_graph.add_edge(j, i_p)
            breakpoint_graph.add_edge(j_p, i)

            P = self.two_break_on_genome(P, j, i, i_p, j_p)
        return P


import unittest


class TestGenomeGraph(unittest.TestCase):
    def test_get_cycles(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        edges = revs.colored_edges(P) + revs.black_edges(P)
        genome_graph = GenomeGraph(edges)

        self.assertEqual([[1, 2, 4, 3, 6, 5, 7, 8]], genome_graph.get_cycles())

    def test_two_break_on_genome_graph(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        edges = revs.colored_edges(P) + revs.black_edges(P)
        genome_graph = GenomeGraph(edges)
        genome_graph.two_break_on_genome_graph(1, 8, 3, 6)
        self.assertEqual([[1, 2, 4, 3], [5, 6, 8, 7]], genome_graph.get_cycles())


class TestReversals(unittest.TestCase):
    def test_shortest_rearrangement_scenario(self):
        P = [[1, -2, -3, 4]]
        Q = [[1, 2, 3, 4]]
        rev = Reversals()
        P_p = rev.shortest_rearrangement_scenario(P, Q)
        self.assertEqual(Q, P_p)

    def test_two_break_on_genome(self):
        P = [[1, -2, -3, 4]]
        revs = Reversals()

        chromosome = revs.two_break_on_genome(P, 1, 8, 3, 6)
        self.assertEqual([[1, -2], [3, -4]], chromosome)

    def test_graph_to_genome(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]

        edges = revs.colored_edges(P) + revs.black_edges(P)

        self.assertEqual([chromosome], revs.graph_to_genome(GenomeGraph(edges)))

    def test_black_edges(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]

        self.assertEqual([(1, 2), (4, 3), (6, 5), (7, 8)], revs.black_edges(P))

    def test_colored_edges(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]

        self.assertEqual([(2, 4), (3, 6), (5, 7), (8, 1)], revs.colored_edges(P))

    def test_cycle_to_chromosome(self):
        revs = Reversals()
        cycle = [1, 2, 4, 3, 6, 5, 7, 8]
        self.assertEqual([1, -2, -3, 4], revs.cycle_to_chromosome(cycle))

    def test_chromosome_to_cycle(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]

        self.assertEqual([1, 2, 4, 3, 6, 5, 7, 8], revs.chromosome_to_cycle(chromosome))

    def test_greedy_sorting(self):
        rev = Reversals()
        input = [1, -7, 6, -10, 9, -8, 2, -11, -3, 5, 4]

        self.assertEqual(11, rev.greedy_sorting(input))


if __name__ == "__main__":
    unittest.main()
