import unittest
from copy import deepcopy
import random
from patterncount import number_to_pattern, hamming_distance, symbol_to_number


def make_counts(motifs, k, pseudo_count=0):
    counts = [[pseudo_count] * 4 for _ in range(k)]
    for motif in motifs:
        for i in range(k):
            current_nuc = motif[i]
            j = symbol_to_number(current_nuc.upper())
            counts[i][j] += 1
    return counts


def profile(motifs, k):
    t = len(motifs)
    pseudo_count = 1
    counts = make_counts(motifs, k, pseudo_count=pseudo_count)
    profile = [[0] * 4 for _ in range(k)]
    for i in range(k):
        for j in range(4):
            profile[i][j] = counts[i][j] / (t + 4 * pseudo_count)

    return profile


def score(motifs, k):

    total_score = 0

    counts = make_counts(motifs, k)

    for i in range(k):
        most_frequent = counts[i].index(max(counts[i]))
        for j in range(4):
            if j != most_frequent:
                total_score += counts[i][j]

    return total_score


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


def probability(motif_profile, pattern, k):
    prob = 1
    for i in range(k):
        symbol = pattern[i]
        j = symbol_to_number(symbol.upper())
        symbol_probability = motif_profile[i][j]
        prob *= symbol_probability
    return prob


def most_probable_k_mer(motif_profile, sequence, k):
    n = len(sequence)
    max_prob = float("-inf")
    max_pattern = None
    for i in range(n - k + 1):
        pattern = sequence[i : i + k]
        prob = probability(motif_profile, pattern, k)
        if prob > max_prob:
            max_prob = prob
            max_pattern = pattern
    return max_pattern


def greedy_motif_search(dna, k, t):
    best_motifes = [sequence[:k] for sequence in dna]
    best_score = score(best_motifes, k)

    first_sequence = dna[0]
    for i in range(len(first_sequence) - k + 1):
        motif_1 = first_sequence[i : i + k]
        motifs = [motif_1]
        for j in range(1, t):
            motif_profile = profile(motifs, k)
            motif_i = most_probable_k_mer(motif_profile, dna[j], k)
            motifs.append(motif_i)

        current_score = score(motifs, k)
        if current_score < best_score:
            best_score = current_score
            best_motifes = deepcopy(motifs)

    return best_motifes


def motifs_from_profile(motif_profile, dna, k):
    motifs = []
    for sequence in dna:
        motif_i = most_probable_k_mer(motif_profile, sequence, k)
        motifs.append(motif_i)
    return motifs


def randomized_motif_search(dna, k, t):
    motifs = []
    for sequence in dna:
        n = len(sequence)
        i = random.randrange(0, n - k + 1)
        motifs.append(sequence[i : i + k])

    best_motifs = deepcopy(motifs)
    best_score = score(best_motifs, k)

    while True:
        motif_profile = profile(motifs, k)
        motifs = motifs_from_profile(motif_profile, dna, k)

        current_score = score(motifs, k)
        if current_score < best_score:
            best_score = current_score
            best_motifs = deepcopy(motifs)
        else:
            return best_motifs


def most_probable_gibbs_k_mer(motif_profile, sequence, k):
    probabilities = []
    patterns = []
    kmers = []
    prob_sum = 0

    n = len(sequence)
    for i in range(n - k + 1):
        pattern = sequence[i : i + k]
        prob = probability(motif_profile, pattern, k)
        prob_sum += prob
        patterns.append(pattern)
        probabilities.append(prob)

    random_pos = random.random() * prob_sum

    current_sum = 0
    for i in range(n - k + 1):
        prob = probabilities[i]
        current_sum += prob
        if current_sum >= random_pos:
            return patterns[i]


def gibbs_sampler(dna, k, t, N):
    motifs = []
    for sequence in dna:
        n = len(sequence)
        i = random.randrange(0, n - k + 1)
        motifs.append(sequence[i : i + k])

    best_motifs = deepcopy(motifs)
    best_score = score(best_motifs, k)

    for _ in range(N):
        i = random.randrange(0, t)
        del motifs[i]

        motifs_profile = profile(motifs, k)
        motifs_i = most_probable_gibbs_k_mer(motifs_profile, dna[i], k)
        motifs.insert(i, motifs_i)

        current_score = score(motifs, k)
        if current_score < best_score:
            best_score = current_score
            best_motifes = deepcopy(motifs)

    return best_motifs


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
