class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def add_neighbor(self, v, w, distance):
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[v].append((w, distance))
        self.adjacency_list[w] = [(v, distance)]

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def __str__(self) -> str:
        return f"{self.adjacency_list}"

    def add_node(self, v):
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []

    def find_path(self, source, destination):
        stack = [source]
        visited = set([source])

        while len(stack) > 0:
            v = stack[-1]
            if v == destination:
                return stack

            has_neighbor = False

            for w, _ in self.adjacency_list[v]:
                if w not in visited:
                    visited.add(w)
                    stack.append(w)
                    has_neighbor = True
                    break
            if not has_neighbor:
                stack.pop()

    def distance_between(self, v_i, v_j):
        for w, dist in self.adjacency_list[v_i]:
            if w == v_j:
                return dist

    def remove_edge(self, v_i, v_j):
        self.adjacency_list[v_i] = [
            neighbor for neighbor in self.adjacency_list[v_i] if neighbor[0] != v_j
        ]
        self.adjacency_list[v_j] = [
            neighbor for neighbor in self.adjacency_list[v_j] if neighbor[0] != v_i
        ]

    def add_vertex_on_edge(self, v_i, v_j, distance_i, distance_j):
        new_vertex = f"X{v_i},{v_j}"

        self.remove_edge(v_i, v_j)
        self.add_neighbor(v_i, new_vertex, distance_i)
        self.add_neighbor(new_vertex, v_j, distance_j)

        return new_vertex

    def add_vertex_on_path(self, u, v, distance):
        path = self.find_path(u, v)
        i = 0
        j = 1

        v_i = path[i]
        v_j = path[j]
        current_distance = self.distance_between(v_i, v_j)
        while current_distance < distance:
            i += 1
            j += 1
            v_i = path[i]
            v_j = path[j]
            current_distance += self.distance_between(v_i, v_j)

        if current_distance == distance:
            return v_j
        else:
            local_distance_j = current_distance - distance
            local_distance_i = self.distance_between(v_i, v_j) - local_distance_j
            return self.add_vertex_on_edge(v_i, v_j, local_distance_i, local_distance_j)


class Cluster:
    def __init__(self, elements=[], age=0):
        self.age = age
        self.elements = elements

    def __str__(self):
        return f"{self.elements}"

    def merge(self, other_cluster):
        c_new = Cluster(elements=self.elements + other_cluster.elements)
        return c_new

    def distance(self, other_cluster, D):
        total_distance = 0
        for e_i in self.elements:
            for e_j in other_cluster.elements:
                d_ij = D[e_i][e_j]
                total_distance += d_ij

        return total_distance / (len(self.elements) + len(other_cluster.elements))


class Phylogeny:
    def limb(self, D, n):
        # To find nodes i and k, such that dik + dnk = din
        # n is size of matrix and the node itself
        min_length = float("inf")
        min_i = None
        min_k = None
        v = n - 1
        for i in range(n):
            for k in range(n):
                if i != v and k != v:
                    limb_length = (D[v][k] + D[i][v] - D[i][k]) / 2
                    if limb_length < min_length:
                        min_length = limb_length
                        min_i = i
                        min_k = k

        return (min_i, min_k, min_length)

    def additive_phylogeny(self, D, n):
        if n == 2:
            return Graph({0: [(1, D[0][1])], 1: [(0, D[0][1])]})

        (i, k, limb_length) = self.limb(D, n)  # limb length for nth node

        for j in range(n - 1):
            D[j][n - 1] = D[j][n - 1] - limb_length
            D[n - 1][j] = D[j][n - 1]

        x = D[i][n - 1]

        T = self.additive_phylogeny(D, n - 1)

        v = T.add_vertex_on_path(i, k, x)
        T.add_neighbor(v, n - 1, limb_length)
        return T

    def two_closest_clusters(self, clusters, D):
        min_ci = None
        min_cj = None
        min_distance = float("inf")

        for c_i in clusters:
            for c_j in clusters:
                if c_i != c_j:
                    current_disance = c_i.distance(c_j, D)
                    if current_disance < min_distance:
                        min_distance = current_disance
                        min_ci = c_i
                        min_cj = c_j

        return min_ci, min_cj, min_distance

    def UPGMA(self, D, n):
        clusters = [Cluster([i], 0) for i in range(n)]
        adjacency_list = dict([(i, []) for i in range(n)])
        T = Graph(adjacency_list)

        while len(clusters) > 1:
            c_i, c_j, dist = self.two_closest_clusters(clusters, D)
            c_new = c_i.merge(c_j)
            c_new.age = dist / 2
            T.add_node(str(c_new))
            T.add_neighbor(str(c_new), str(c_i), c_new.age - c_i.age)
            T.add_neighbor(str(c_new), str(c_j), c_new.age - c_j.age)

            clusters = [
                cluster for cluster in clusters if cluster != c_i and cluster != c_j
            ]
            clusters.append(c_new)

        root = str(clusters[0])

        return T, root


import unittest


class TestPhylogeny(unittest.TestCase):
    def test_add_vertex_on_path(self):
        G = {"A": [("B", 2), ("C", 1)], "B": [], "C": [("D", 3)], "D": []}
        g = Graph(G)
        g.add_vertex_on_path("A", "D", 2)
        self.assertEqual(["A", "C", "XC,D", "D"], g.find_path("A", "D"))

    def test_find_path(self):
        G = {"A": [("B", 2), ("C", 1)], "B": [], "C": [("D", 3)], "D": []}
        g = Graph(G)
        self.assertEqual(["A", "C", "D"], g.find_path("A", "D"))

    def test_limb_length(self):
        ph = Phylogeny()
        D = [[0, 13, 21, 22], [13, 0, 12, 13], [21, 12, 0, 13], [22, 13, 13, 0]]
        n = len(D)
        self.assertEqual((0, 2, 7), ph.limb(D, n))

    def test_additive_phylogeny(self):
        ph = Phylogeny()
        D = [[0, 13, 21, 22], [13, 0, 12, 13], [21, 12, 0, 13], [22, 13, 13, 0]]
        n = len(D)
        t = ph.additive_phylogeny(D, n)
        print(t)

    def test_UPGMA(self):
        D = [[0, 3, 4, 3], [3, 0, 4, 5], [4, 4, 0, 2], [3, 5, 2, 0]]
        n = len(D)
        ph = Phylogeny()
        T, root = ph.UPGMA(D, n)
        print(T, root)


if __name__ == "__main__":
    unittest.main()
