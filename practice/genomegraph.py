class GenomeGraph:
    def __init__(self, edges) -> None:
        self.edges = edges
        self.adjacency_list = {}
        for u, v in edges:
            if u not in self.adjacency_list:
                self.adjacency_list[u] = []
            if v not in self.adjacency_list:
                self.adjacency_list[v] = []

            self.adjacency_list[u].append(v)
            self.adjacency_list[v].append(u)

    def get_cycles(self):
        unvisited = set(self.adjacency_list.keys())
        cycles = []
        while len(unvisited) > 0:
            v = min(unvisited)
            unvisited.remove(v)
            current_cycle = [v]
            w = sorted(self.adjacency_list[v])[0]

            while w != v and w != None:
                current_cycle.append(w)
                unvisited.remove(w)
                first_unvisited = None
                for u in sorted(self.adjacency_list[w]):
                    if u in unvisited:
                        first_unvisited = u
                        break

                w = first_unvisited

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


class Reversals:
    def chromosome_to_cycle(self, chromosome):
        cycle = []
        n = len(chromosome)
        for j in range(n):
            i = chromosome[j]
            if i > 0:
                cycle.append(2 * i - 1)
                cycle.append(2 * i)
            else:
                cycle.append(-2 * i)
                cycle.append(-2 * i - 1)
        return cycle

    def cycle_to_chromosome(self, cycle):
        chromosome = []
        for i in range(0, len(cycle), 2):
            if cycle[i] < cycle[i + 1]:
                chromosome.append(cycle[i + 1] // 2)
            else:
                chromosome.append(-cycle[i] // 2)

        return chromosome

    def colored_edges(self, P):
        edges = []
        for chromosome in P:
            nodes = self.chromosome_to_cycle(chromosome)
            m = len(nodes)
            for j in range(1, m - 1, 2):
                edges.append((nodes[j], nodes[j + 1]))

        edges.append((nodes[-1], nodes[0]))

        return edges

    def black_edges(self, P):
        edges = []
        for chromosome in P:
            nodes = self.chromosome_to_cycle(chromosome)
            m = len(nodes)
            for j in range(0, m - 1, 2):
                edges.append((nodes[j], nodes[j + 1]))

        return edges

    def graph_to_genome(self, genome_graph):
        P = []
        cycles = genome_graph.get_cycles()

        for nodes in cycles:
            chromosome = self.cycle_to_chromosome(nodes)
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

        conversions = []

        while True:
            cycles = breakpoint_graph.get_cycles()
            non_trivial_cycle = None
            for cycle in cycles:
                if len(cycle) > 2:
                    non_trivial_cycle = cycle
                    break
            if non_trivial_cycle == None:
                break

            n = len(non_trivial_cycle)
            cycle_edges = [
                (non_trivial_cycle[i], non_trivial_cycle[i - 1]) for i in range(n - 1)
            ] + [(non_trivial_cycle[-1], non_trivial_cycle[0])]

            print(cycle_edges)

            for k in range(n):
                edge = cycle_edges[k]
                (j_blue, i_p_blue) = edge
                if (j_blue, i_p_blue) in blue_edges or (i_p_blue, j_blue) in blue_edges:
                    previous_red_edge = cycle_edges[(k - 1) % n]
                    next_red_edge = cycle_edges[(k + 1) % n]

            (i, j) = previous_red_edge
            (i_p, j_p) = next_red_edge

            breakpoint_graph.remove_edge(i, j)
            breakpoint_graph.remove_edge(i_p, j_p)

            breakpoint_graph.add_edge(j, i_p)
            breakpoint_graph.add_edge(j_p, i)

            P = self.two_break_on_genome(P, j, i, i_p, j_p)
            conversions.append(P)

        return conversions


import unittest


class TestGenomeGraph(unittest.TestCase):
    def test_shortest_rearrangement_scenario(self):
        P = [[1, -2, -3, 4]]
        Q = [[1, 2, 3, 4]]
        revs = Reversals()

        conversions = revs.shortest_rearrangement_scenario(P, Q)

        self.assertEqual(2, len(conversions))

        self.assertEqual(Q, conversions[-1])

    def test_two_break_on_genome(self):
        revs = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]

        self.assertEqual([[1, -2], [3, -4]], revs.two_break_on_genome(P, 1, 8, 3, 6))

    def test_chromosome_to_cycle(self):
        gg = Reversals()

        self.assertEqual(
            [1, 2, 4, 3, 6, 5, 7, 8], gg.chromosome_to_cycle([1, -2, -3, 4])
        )

    def test_cycle_to_chromosome(self):
        gg = Reversals()
        self.assertEqual(
            [1, -2, -3, 4], gg.cycle_to_chromosome([1, 2, 4, 3, 6, 5, 7, 8])
        )

    def test_colored_edges(self):
        gg = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        self.assertEqual([(2, 4), (3, 6), (5, 7), (8, 1)], gg.colored_edges(P))

    def test_black_edges(self):
        gg = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        self.assertEqual([(1, 2), (4, 3), (6, 5), (7, 8)], gg.black_edges(P))

    def test_get_cycles(self):
        rev = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        edges = rev.colored_edges(P) + rev.black_edges(P)

        gg = GenomeGraph(edges)
        self.assertEqual([[1, 2, 4, 3, 6, 5, 7, 8]], gg.get_cycles())

    def test_graph_to_genome(self):
        rev = Reversals()
        chromosome = [1, -2, -3, 4]
        P = [chromosome]
        edges = rev.colored_edges(P) + rev.black_edges(P)

        gg = GenomeGraph(edges)
        self.assertEqual([[1, -2, -3, 4]], rev.graph_to_genome(gg))


if __name__ == "__main__":
    unittest.main()
