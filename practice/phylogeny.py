class Graph:
    def __init__(self, adjacency_list) -> None:
        self.adjacency_list = adjacency_list

    def add_node(self, v):
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []

    def add_neighbor(self, v, w, distance):
        self.adjacency_list[v].append((w, distance))
        self.adjacency_list[w] = [((v, distance))]

    def remove_edge(self, v_i, v_j):
        self.adjacency_list[v_i] = [
            neigh for neigh in self.adjacency_list[v_i] if neigh[0] != v_j
        ]
        self.adjacency_list[v_j] = [
            neigh for neigh in self.adjacency_list[v_j] if neigh[0] != v_i
        ]

    def get_neighbor(self, v):
        return self.adjacency_list[v]

    def __str__(self) -> str:
        return f"{self.adjacency_list}"

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

        local_distance_j = current_distance - distance  # local distance between i and j
        local_distance_i = self.distance_between(v_i, v_j) - local_distance_j
        return self.add_vertex_on_edge(v_i, v_j, local_distance_i, local_distance_j)


class Cluster:
    def __init__(self, elements=[], age=0) -> None:
        self.age = age
        self.elements = elements

    def __str__(self) -> str:
        return f"{self.elements}"

    def distance(self, other_cluster, D):
        total_distance = 0
        for e_i in self.elements:
            for e_j in other_cluster.elements:
                d_ij = D[e_i][e_j]
                total_distance += d_ij

        return total_distance / (len(self.elements) + len(other_cluster.elements))

    def merge(self, other_cluster):
        return Cluster(elements=self.elements + other_cluster.elements)


class Phylogeny:
    def limb(self, D, n):
        # naci i, k cvorove: Dnk + D = Dik + Din
        min_length = float("inf")
        min_i = None
        min_k = None
        for i in range(n):
            for k in range(n):
                if i != n - 1 and k != n - 1:
                    limb_length = (D[n - 1][k] + D[i][n - 1] - D[i][k]) / 2
                    if limb_length < min_length:
                        min_length = limb_length
                        min_i = i
                        min_k = k

        return (min_i, min_k, min_length)

    def additive_phylogeny(self, D, n):
        if n == 2:
            return Graph({0: [(1, D[0][1])], 1: [(0, D[0][1])]})

        (i, k, limb_length) = self.limb(D, n)
        for j in range(n - 1):
            D[j][n - 1] -= limb_length
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
                    current_distance = c_i.distance(c_j, D)
                    if current_distance < min_distance:
                        min_ci = c_i
                        min_cj = c_j
                        min_distance = current_distance

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
            T.add_neighbor(
                str(c_new),
                str(c_i),
            )
            T.add_neighbor(str(c_new), str(c_j))

            clusters = [
                cluster for cluster in clusters if cluster != c_i and cluster != c_j
            ]
            clusters.append(c_new)

        root = str(clusters[0])
        return T, root


import unittest


class TestGraph(unittest.TestCase):
    def test_find_path(self):
        G = {"A": [("B", 2), ("C", 1)], "B": [], "C": [("D", 3)], "D": []}
        graph = Graph(G)
        self.assertEqual(["A", "C", "D"], graph.find_path("A", "D"))


class TestPhylogeny(unittest.TestCase):
    def test_limb(self):
        D = [[0, 13, 21, 22], [13, 0, 12, 13], [21, 12, 0, 13], [22, 13, 13, 0]]
        n = len(D)

        ph = Phylogeny()
        self.assertEqual((0, 2, 7), ph.limb(D, n))

    def test_additive_philogeny(self):
        D = [[0, 13, 21, 22], [13, 0, 12, 13], [21, 12, 0, 13], [22, 13, 13, 0]]
        n = len(D)

        ph = Phylogeny()
        print(ph.additive_phylogeny(D, n))


if __name__ == "__main__":
    unittest.main()
