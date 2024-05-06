import unittest


def pattern_count(text, pattern):
    count = 0
    k = len(pattern)
    n = len(text)
    for i in range(0, n - k + 1):
        curr_pattern = text[i : i + k]
        if curr_pattern == pattern:
            count += 1
    return count


def frequent_words(text, k):
    frequent_words = set([])
    n = len(text)
    counts = [0 for i in range(n - k + 1)]

    for i in range(n - k + 1):
        pattern = text[i : i + k]
        counts[i] = pattern_count(text, pattern)

    max_count = max(counts)
    for i in range(n - k + 1):
        if counts[i] == max_count:
            pattern = text[i : i + k]
            frequent_words.add(pattern)

    return frequent_words


mapping = {"A": 0, "T": 1, "C": 2, "G": 3}
inv_map = {v: k for k, v in mapping.items()}


def symbol_to_number(symbol=""):
    if symbol not in mapping:
        raise Exception("Invalid Symbol: " + symbol)
    return mapping[symbol.upper()]


def pattern_to_number(pattern):
    if len(pattern) == 1:
        return symbol_to_number(pattern)

    prefix = pattern[:-1]
    last_symbol = pattern[-1]

    return pattern_to_number(prefix) * 4 + symbol_to_number(last_symbol)


def number_to_symbol(number):
    if number not in inv_map:
        raise "Invalid Number"

    return inv_map[number]


def number_to_pattern(number, k):
    if k == 1:
        return number_to_symbol(number)

    prefix = number // 4
    remainder = number % 4

    return number_to_pattern(prefix, k - 1) + number_to_symbol(remainder)


def compute_frequencies(text, k):
    frequency_array = [0 for _ in range(4**k)]
    n = len(text)
    for i in range(0, n - k + 1):
        pattern = text[i : i + k]
        j = pattern_to_number(pattern)
        frequency_array[j] += 1

    return frequency_array


def faster_frequent_words(text, k):
    frequent_patterns = set([])
    frequency_array = compute_frequencies(text, k)

    max_count = max(frequency_array)
    for i in range(0, 4**k):
        if frequency_array[i] == max_count:
            pattern = number_to_pattern(i, k)
            frequent_patterns.add(pattern)

    return frequent_patterns


def hamming_distance(seq_1, seq_2):
    n = len(seq_1)

    dist = 0
    for i in range(n):
        if seq_1[i] != seq_2[i]:
            dist += 1
    return dist


def immediate_neighbors(pattern):
    neighborhood = set([])
    n = len(pattern)
    for i in range(n):
        curr_nucleotide = pattern[i]

        for nucleotide in ["A", "T", "C", "G"]:
            if nucleotide != curr_nucleotide:
                new_pattern_list = list(pattern)
                new_pattern_list[i] = nucleotide

                new_pattern = "".join(new_pattern_list)
                neighborhood.add(new_pattern)
    return list(neighborhood)


def iterative_neighbors(pattern, d):
    neighborhood = set([pattern])

    for _ in range(d):
        for neighbor in neighborhood:
            new_neighbors = immediate_neighbors(neighbor)
            neighborhood = set(list(neighborhood) + new_neighbors)

    return neighborhood


# Recursive implementation
def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {"A", "C", "G", "T"}

    neighborhood = set([])
    suffix = pattern[1:]
    suffix_neighbors = neighbors(suffix, d)
    for text in suffix_neighbors:
        new_neighbor = None
        if hamming_distance(text, suffix) < d:
            for x in ["A", "T", "C", "G"]:
                new_neighbor = x + text
                neighborhood.add(new_neighbor)

        else:
            new_neighbor = pattern[0] + text
            neighborhood.add(new_neighbor)

    return list(neighborhood)


def approximate_pattern_count(text, pattern, d):
    n = len(text)
    k = len(pattern)

    count = 0

    for i in range(0, n - k + 1):
        if hamming_distance(pattern, text[i : i + k]) <= d:
            count += 1

    return count


def frequent_words_with_mismatches(text, k, d):
    frequent_patterns = set([])
    frequency_array = [0 for _ in range(4**k)]

    close = [0 for _ in range(4**k)]

    n = len(text)
    for i in range(n - k + 1):
        pattern = text[i : i + k]
        neighborhood = neighbors(pattern, d)
        for neighbor in neighborhood:
            j = pattern_to_number(neighbor)
            close[j] = 1

    for i in range(4**k):
        if close[i] == 1:
            pattern = number_to_pattern(i, k)
            frequency_array[i] = approximate_pattern_count(text, pattern, d)

    max_count = max(frequency_array)
    for i in range(4**k):
        if frequency_array[i] == max_count:
            frequent_patterns.add(number_to_pattern(i, k))

    return list(frequent_patterns)


def compute_gc(dna):
    skew = [0 for _ in dna]
    curr_sum = 0
    n = len(dna)
    for i in range(n):
        if dna[i] == "G":
            curr_sum += 1
        elif dna[i] == "C":
            curr_sum -= 1

        skew[i] = curr_sum

    return skew


class PatternCount(unittest.TestCase):
    def test_pattern_count(self):
        text = "AAATTTGCTAAATTTGTGAGAT"
        pattern = "AAATTT"

        self.assertEqual(2, pattern_count(text, pattern))

    def test_frequent_words(self):
        text = "ATCGCGGC"
        k = 2
        self.assertEqual(set(["GC", "CG"]), frequent_words(text, k))

    def test_symbol_mapping(self):
        self.assertEqual(symbol_to_number("A"), 0)

    def test_pattern_to_number(self):
        self.assertEqual(6, pattern_to_number("ATC"))

    def test_number_to_pattern(self):
        self.assertEqual("ATC", number_to_pattern(6, 3))

    def test_faster_frequent_words(self):
        text = "ATCGCGGC"
        k = 2
        self.assertEqual(set(["GC", "CG"]), set(faster_frequent_words(text, k)))

    def test_hamming_distance(self):
        self.assertEqual(2, hamming_distance("ABCD", "ABDC"))

    def test_immediate_neighbors(self):
        self.assertEqual(
            set(["TA", "AT", "GA", "AC", "CA", "AG"]), set(immediate_neighbors("AA"))
        )

    def test_iterative_neighbors(self):
        self.assertEqual(
            set(["AC", "AT", "AG", "GA", "TA", "CA", "AA"]),
            set(iterative_neighbors("AA", 1)),
        )

    def test_neighbors(self):
        self.assertEqual(
            set(["AC", "AT", "AG", "GA", "TA", "CA", "AA"]),
            set(neighbors("AA", 1)),
        )

    def test_frequent_words_with_mismatches(self):
        text = "ACGTTGCACGTTACACACACAGGTTCGGATGCATGCCGTAAGCTACGT"
        self.assertAlmostEqual(
            ["CACA", "ACGT", "ACAC"], frequent_words_with_mismatches(text, 4, 0)
        )

    def test_compute_gc(self):
        self.assertEqual(
            [-1, -2, -2, -2, -1, -1, -1, 0, -1, 0, 0, 1, 1, 2, 2, 2, 1, 0, -1, -2, -3],
            compute_gc("CCATGTAGCGAGTGATCCCCC"),
        )


if __name__ == "__main__":
    unittest.main()
