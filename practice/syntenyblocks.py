class Reversals:

    def k_sorting_reversal(self, P, k):
        n = len(P)
        for i in range(k, n):
            if abs(P[i]) == k:
                P[k:i] = [-x for x in P[k:i][::-1]]

        return P

    def greedy_sorting(self, P):
        approximate_reversal_distance = 0

        n = len(P)
        for k in range(n):
            if P[k] != (k + 1):
                P = self.k_sorting_reversal(P, k)
                approximate_reversal_distance += 1
                if P[k] == -(k + 1):
                    P[k] = -P[k]
                    approximate_reversal_distance += 1

        return approximate_reversal_distance


import unittest


class TestSyntenyBlocks(unittest.TestCase):
    def test_greedy_sorting(self):
        reversals = Reversals()
        P = [1, -7, 6, -10, 9, -8, 2, -11, -3, 5, 4]
        self.assertEqual(11, reversals.greedy_sorting(P))


if __name__ == "__main__":
    unittest.main()
