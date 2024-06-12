import unittest


def pattern_count(text, pattern):
    n = len(text)
    k = len(pattern)
    count = 0

    for i in range(n - k + 1):
        if pattern == text[i : i + k]:
            count += 1

    return count


def frequent_words(text, k):
    n = len(text)
    frequences = [0 for _ in range(n - k + 1)]
    for i in range(n - k + 1):
        frequences[i] = pattern_count(text, text[i : i + k])

    max_count = max(frequences)
    most_frequent_words = set([])

    for i in range(n - k + 1):
        if frequences[i] == max_count:
            most_frequent_words.add(text[i : i + k])

    return most_frequent_words


mapping = {"A": 0, "T": 1, "C": 2, "G": 3}
inv_map = {value: key for (key, value) in mapping.items()}


def symbol_to_number(char):

    return mapping.get(char)


def number_to_symbol(number):
    if number not in inv_map:
        raise "Invalid Number"

    return inv_map[number]


def pattern_to_number(pattern):
    k = len(pattern)
    if k == 1:
        return symbol_to_number(pattern)

    return 4 * pattern_to_number(pattern[: k - 1]) + symbol_to_number(pattern[-1])


def number_to_pattern(value, k):
    if value == 0:
        return "".join("A" for _ in range(k))
    (div, mod) = divmod(value, 4)

    return number_to_pattern(div, k - 1) + number_to_symbol(mod)


def faster_frequent_words(text, k):
    pattern_counts = [0 for _ in range(4**k)]
    frequent_words = []
    n = len(text)
    for i in range(n - k + 1):
        pattern = text[i : i + k]
        num_pattern = pattern_to_number(pattern)
        pattern_counts[num_pattern] += 1

    max_count = max(pattern_counts)
    for i in range(4**k):
        if pattern_counts[i] == max_count:
            frequent_words.append(number_to_pattern(i, k))

    return frequent_words


def hamming_distance(s1, s2):
    mismatch_count = 0
    n = len(s1)
    for i in range(n):
        if s1[i] != s2[i]:
            mismatch_count += 1

    return mismatch_count


def immediate_neighbors(pattern):
    pattern_neighbors = set([])

    for i, char in enumerate(pattern):
        for neighbor_char in ["A", "T", "G", "C"]:
            if neighbor_char != char:
                pattern_neighbors.add(f"{pattern[:i]}{neighbor_char}{pattern[i+1:]}")

    return pattern_neighbors


def iterative_neighbors(pattern, d):
    neighbors = set([pattern])

    for _ in range(d):
        for neighbor in neighbors:
            new_neighbors = immediate_neighbors(neighbor)
            neighbors = set(list(new_neighbors) + list(neighbors))

    return neighbors


def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {"A", "T", "G", "C"}

    neighborhood = set([])

    suffix = pattern[1:]
    neighbors_for_suffix = neighbors(suffix, d)

    for text in neighbors_for_suffix:
        if hamming_distance(text, suffix) < d:
            for char in ["A", "G", "C", "T"]:
                neighborhood.add(char + text)
        else:
            neighborhood.add(pattern[0] + text)
    return neighborhood


def frequent_words_with_mismatches(text, k, d):
    return []


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

    def test_neighbors_with_bigger_distance(self):
        self.assertEqual(
            set(
                [
                    "AA",
                    "AT",
                    "AG",
                    "GA",
                    "TA",
                    "CA",
                    "TT",
                    "CC",
                    "GC",
                    "CG",
                    "TG",
                    "CT",
                    "GG",
                    "AC",
                    "GT",
                    "TC",
                ]
            ),
            set(neighbors("AA", 2)),
        )

    def test_frequent_words_with_mismatches(self):
        text = "ACGTTGCACGTTACACACACAGGTTCGGATGCATGCCGTAAGCTACGT"
        self.assertEqual(
            ["CACA", "ACGT", "ACAC"], frequent_words_with_mismatches(text, 4, 0)
        )


if __name__ == "__main__":
    unittest.main()
