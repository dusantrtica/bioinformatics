import unittest
from patterncount import number_to_pattern, hamming_distance, symbol_to_number


def score(motifs, k):
    counts = [[0] * 4 for _ in range(k)]

    for motif in motifs:
        for i in range(k):
            current_nuc = motif[i]
            j = symbol_to_number(current_nuc)
            counts[i][j] += 1


def d(pattern, dna):
    total_distance = 0
    k = len(pattern)
    for sequence in dna:
        n = len(sequence)
        min_distance = float("inf")
        for i in range(0, n - k + 1):
            current_pattern = sequence[i : i + k]
            current_distance = hamming_distance(pattern, current_pattern.upper())
            if current_distance < min_distance:
                min_distance = current_distance
        total_distance += min_distance

    return total_distance


def median_string(dna, k):
    distance = float("inf")
    median_pattern = None

    for i in range(4**k):
        pattern = number_to_pattern(i, k)
        current_distance = d(pattern, dna)
        if current_distance < distance:
            distance = current_distance
            median_pattern = pattern

    return median_pattern


class TestMedianStringSearch(unittest.TestCase):
    def test_d(self):
        dna_sequence = [
            "ttaccttAAC",
            "gATAtctgtc",
            "ACGgcgttcg",
            "ccctAAAgag",
            "cgtcAGAggt",
        ]

        pattern = "AAA"

        self.assertEqual(5, d(pattern, dna_sequence))

    def test_median_string(self):
        dna_sequence = [
            "ttaccttAAC",
            "gATAtctgtc",
            "ACGgcgttcg",
            "ccctAAAgag",
            "cgtcAGAggt",
        ]

        self.assertEqual("CCT", median_string(dna_sequence, 3))


if __name__ == "__main__":
    unittest.main()
