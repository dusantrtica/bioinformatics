import unittest
from copy import deepcopy

mapping = {"A": 0, "T": 1, "C": 2, "G": 3}
inv_map = {v: k for k, v in mapping.items()}


def hamming_distance(s1, s2):
    n = len(s1)
    different_characters = 0
    for i in range(n):
        if s1[i] != s2[i]:
            different_characters += 1

    return different_characters


def number_to_symbol(number):
    return inv_map.get(number)


def symbol_to_number(symbol):
    return mapping.get(symbol)


def number_to_pattern(number, k):
    if number == 0:
        return "A" * k
    (div, mod) = divmod(number, 4)

    return number_to_pattern(div, k - 1) + number_to_symbol(mod)


def median_string(dna, k):
    best_pattern = ""
    min_distance = float("inf")

    for i in range(4**k):
        pattern = number_to_pattern(i, k)
        distance = d(pattern, dna)
        if distance < min_distance:
            min_distance = distance
            best_pattern = pattern

    return best_pattern


def d(pattern, dna):
    total_distance = 0

    k = len(pattern)
    for sequence in dna:
        n = len(sequence)
        sequence_min_distance = float("inf")
        for i in range(n - k + 1):
            distance = hamming_distance(pattern, sequence[i : i + k].upper())
            if distance < sequence_min_distance:
                sequence_min_distance = distance

        total_distance += sequence_min_distance

    return total_distance


def score(motifs, k):
    counts = [[0 for _ in range(4)] for _ in range(k)]

    t = len(motifs)

    total_sum_of_different = 0

    for i in range(k):
        for c in range(t):
            char = motifs[c][i]
            j = symbol_to_number(char.upper())
            counts[i][j] += 1

    for i in range(k):
        index_with_max_elem = counts[i].index(max(counts[i]))
        for j in range(4):
            if j != index_with_max_elem:
                total_sum_of_different += counts[i][j]

    return total_sum_of_different


def profile(motifs, k):
    t = len(motifs)

    counts = [[0 for _ in range(4)] for _ in range(k)]
    for i in range(k):
        for c in range(t):
            char = motifs[c][i]
            j = symbol_to_number(char.upper())
            counts[i][j] += 1

    profile = [[0 for _ in range(4)] for _ in range(k)]
    for i in range(k):
        for j in range(4):
            profile[i][j] = counts[i][j] / (t)

    return profile


def probability(motif_profile, pattern, k):
    prob = 1
    for i in range(k):
        prob = prob * motif_profile[i][symbol_to_number(pattern[i].upper())]

    return prob


def most_probable_k_mer(motif_profile, sequence, k):
    k_mer = sequence[0:k]
    k_mer_probability = float(0)
    n = len(sequence)
    for i in range(n - k + 1):
        pattern = sequence[i : i + k]
        prob = probability(motif_profile, pattern, k)
        if prob > k_mer_probability:
            k_mer = pattern
            k_mer_probability = prob

    return k_mer


def greedy_motif_search(dna, k, t):
    best_motifs = [sequence[:k] for sequence in dna]
    best_motifs_score = score(best_motifs, k)

    first_sequence = dna[0]

    for i in range(len(first_sequence) - k + 1):
        motif_1 = first_sequence[i : i + k]
        motifs = [motif_1]

        for j in range(1, t):
            motif_profile = profile(motifs, k)
            motif = most_probable_k_mer(motif_profile, dna[j], k)
            motifs.append(motif)

        current_score = score(motifs, k)
        if current_score < best_motifs_score:
            best_motifs_score = current_score
            best_motifs = deepcopy(motifs)

    return best_motifs


def randomized_motif_search(dna, k, t):
    pass


def gibbs_sampler(dna, k, t, N):
    pass


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

    def test_score(self):
        motifs = ["ATGCAA", "CTCCAA", "AGCCAA"]
        self.assertEqual(3, score(motifs, 6))

    def test_profile(self):
        motifs = ["ATGCAA", "CTCCAA", "AGCCAA"]
        profile(motifs, 6)

    def test_most_probable_k_mer(self):
        motifs = ["ATGCAAATGCAAATGCAA", "CTCCAACTCCAACTCCAA", "AGCCAAAGCCAAAGCCAA"]
        k = len(motifs[0])
        motif_profile = profile(motifs, k)

        self.assertEqual(
            "CTCCAACTCCAACTCCAA",
            most_probable_k_mer(
                motif_profile, "CTCCAATGTGTGCTCCAACTCCAACTCCAACTCCAA", k
            ),
        )

    def test_greedy_motif_search(self):
        dna = ["ttACCTtaac", "gATGTctgtc", "acgGCGTtag", "ccctaACGAg", "cgtcagAGGT"]

        self.assertEqual(
            ["ACCT", "ATGT", "acgG", "ACGA", "AGGT"],
            greedy_motif_search(dna, 4, len(dna)),
        )

    def test_randomized_motif_search(self):
        dna = ["ttACCTtaac", "gATGTctgtc", "acgGCGTtag", "ccctaACGAg", "cgtcagAGGT"]

        print(randomized_motif_search(dna, 4, len(dna)))

    def test_gibbs_sampler(self):
        dna = ["ttACCTtaac", "gATGTctgtc", "acgGCGTtag", "ccctaACGAg", "cgtcagAGGT"]
        N = 10

        self.assertEqual(
            ["ACCT", "ATGT", "acgG", "ACGA", "AGGT"],
            gibbs_sampler(dna, 4, len(dna), N),
        )


if __name__ == "__main__":
    unittest.main()
