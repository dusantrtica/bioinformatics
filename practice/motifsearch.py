import unittest


def median_string(sequence, k):
    pass


def d(pattern, sequence):
    pass


def score(motifs, k):
    pass


def profile(motifs, k):
    pass


def most_probable_k_mer(motif_profile, sequence, k):
    pass


def greedy_motif_search(dna, k, t):
    pass


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
