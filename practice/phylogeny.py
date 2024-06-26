class Graph:
    def __init__(self, adjacency_list) -> None:
        self.adjacency_list = adjacency_list

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
