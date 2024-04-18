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
        raise "Invalid Symbol"
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


import unittest


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


if __name__ == "__main__":
    unittest.main()
