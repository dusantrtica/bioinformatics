class TrieNode:
    def __init__(self, character):
        self.character = character
        self.children = {}
        self.is_leaf = True

    def add_child(self, character):
        new_node = TrieNode(character)
        self.is_leaf = False
        self.children[character] = new_node

    def get_child(self, character):
        if character not in self.children:
            return None

        return self.children[character]

    def __str__(self):
        return f"{self.character}: {list(self.children.keys())}"


class Trie:
    def __init__(self, patterns) -> None:
        self.trie_construction(patterns)

    def trie_construction(self, patterns):
        self.root = TrieNode(None)

        for pattern in patterns:
            current_node = self.root
            for current_symbol in pattern:
                if current_symbol not in current_node.children:
                    current_node.add_child(current_symbol)
                current_node = current_node.get_child(current_symbol)

        return self.root

    def __str__(self):
        return f"{self.root}"

    def dfs(self, node, path=""):
        for character, child in node.children.items():
            if child.is_leaf:
                print(f"{path}{character}")
            else:
                self.dfs(child, path=f"{path}{character}")

    def prefix_trie_matching(self, text):
        current_node = self.root
        path = ""
        for character in text:
            if current_node.is_leaf:
                return path

            if character in current_node.children:
                path += character
                current_node = current_node.get_child(character)
            else:
                return None

        return path

    def trie_matching(self, text):
        found_patterns = []
        n = len(text)
        for i in range(n):
            result = self.prefix_trie_matching(text[i:])
            if result != None:
                found_patterns.append((result, i))

        return found_patterns


class SuffixArray:
    def __init__(self, text):
        self.arr = self.generate_suffix_array(text)

    def generate_suffix_array(self, text):
        terminated_text = f"{text}$"

        arr = [(terminated_text[i:], i) for i in range(len(terminated_text))]

        return sorted(arr)

    def compare(self, pattern, suffix):
        n = len(pattern)
        m = len(suffix)

        if n > m:
            return 1

        suffix_pref = suffix[:n]
        if suffix_pref == pattern:
            return 0

        if suffix_pref < pattern:
            return 1
        else:
            return -1

    def pattern_matching_with_suffix_array(self, pattern):
        n = len(self.arr)

        min_index = 0
        max_index = n

        while min_index <= max_index:
            mid_index = (min_index + max_index) // 2

            current_suffix = self.arr[mid_index][0]
            compare_res = self.compare(pattern, current_suffix)
            if compare_res == 0:
                i = mid_index
                while i >= 0 and self.compare(pattern, self.arr[i][0]) == 0:
                    i -= 1

                i += 1

                j = mid_index
                while j < n and self.compare(pattern, self.arr[j][0]) == 0:
                    j += 1

                return [self.arr[k][1] for k in range(i, j)]

            elif compare_res < 0:
                max_index = mid_index
            else:
                min_index = mid_index

        return []


class BWT:
    def __init__(self, text):
        self.bwt_text = self.construct_bwt(text + "$")

    def construct_bwt(self, text):
        # matrica ciklicnih permutacija i da izvucemo poslednju kolonu
        n = len(text)
        permutations = [text[i:n] + text[:i] for i in range(n)]
        return "".join([x[-1] for x in sorted(permutations)])

    def inverse_bwt(self):
        last_column = list(self.bwt_text)
        columns = sorted(last_column[:])
        orignal_row = last_column.index("$")
        n = len(last_column)
        for _ in range(n - 1):
            for j in range(n):
                columns[j] = last_column[j] + columns[j]
            columns.sort()

        return columns[orignal_row][:-1]

    def last_to_first(self, last_col_index):
        last_column = list(self.bwt_text)
        first_column = sorted(last_column[:])

        last_col_char = last_column[last_col_index]
        n = len(last_column)
        rank = 0
        for i in range(last_col_index + 1):
            if last_column[i] == last_col_char:
                rank += 1

        count = 0
        for i in range(n):
            if first_column[i] == last_col_char:
                count += 1
            if count == rank:
                return i

    def bw_matching(self, pattern):
        n = len(self.bwt_text)
        last_column = list(self.bwt_text)

        top = 0
        bottom = n - 1

        j = len(pattern) - 1
        while top <= bottom:
            if j < 0:
                return bottom - top + 1
            symbol = pattern[j]
            j -= 1
            if symbol in last_column[top : bottom + 1]:
                first_index = None
                last_index = None

                for i in range(top, bottom + 1):
                    if symbol == last_column[i]:
                        if first_index == None:
                            first_index = i
                        last_index = i
                top = self.last_to_first(first_index)
                bottom = self.last_to_first(last_index)

            else:
                return 0


import unittest


class TestBWT(unittest.TestCase):
    def test_bw_matching(self):
        bwt = BWT("panamabananas")
        self.assertEqual(3, bwt.bw_matching("ana"))
        self.assertEqual(1, bwt.bw_matching("ban"))

    def test_last_to_first(self):
        bwt = BWT("panamabananas")
        print("".join(bwt.bwt_text))
        print("".join(bwt.inverse_bwt()))
        self.assertEqual(11, bwt.last_to_first(6))

    def test_construct_bwt(self):
        bwt = BWT("panamabananas")
        self.assertEqual("smnpbnnaaaaa$a", bwt.bwt_text)

    def test_inverse_bwt(self):
        text = "panamabananas"
        bwt = BWT(text)
        self.assertEqual(text, bwt.inverse_bwt())


class TestTrie(unittest.TestCase):
    def test_trie_construction(self):
        patterns = [
            "ananas",
            "and",
            "antenna",
            "banana",
            "bandana",
            "nab",
            "nana",
            "pan",
        ]

        trie = Trie(patterns)
        trie.dfs(trie.root)

    def test_prefix_trie_matching(self):
        patterns = [
            "ananas",
            "and",
            "antenna",
            "banana",
            "bandana",
            "nab",
            "nana",
            "pan",
        ]

        trie = Trie(patterns)

        self.assertEqual("banana", trie.prefix_trie_matching("banana"))
        self.assertEqual("pan", trie.prefix_trie_matching("panabanananas"))

    def test_trie_matching(self):
        patterns = [
            "ananas",
            "and",
            "antenna",
            "banana",
            "bandana",
            "nab",
            "nana",
            "pan",
        ]

        trie = Trie(patterns)
        self.assertEqual(
            [("pan", 0), ("banana", 6), ("ananas", 7), ("nana", 8)],
            trie.trie_matching("panamabananas"),
        )

    def test_patterns_(self):
        patterns = ["GAATTC", "AACGT", "GGTGC"]
        dna = "GAGATCGAATTCTCGGAGATAACGTCAGTTTGCAGGTGCTGC"
        trie = Trie(patterns)
        print(trie.trie_matching(dna))


class TestSuffixArray(unittest.TestCase):
    def test_generate_suffix_array(self):
        text = "PANANABANANAS"
        sa = SuffixArray(text)
        print(sa.arr)

    def test_compare(self):
        sa = SuffixArray([])
        self.assertEqual(0, sa.compare("aaa", "aaa"))
        self.assertEqual(0, sa.compare("aaa", "aaaa"))
        self.assertEqual(1, sa.compare("aab", "aaab"))

    def test_pattern_matching_with_suffix_array(self):
        suff_arr = SuffixArray("panamabananas")
        self.assertEqual([6], suff_arr.pattern_matching_with_suffix_array("banana"))


if __name__ == "__main__":
    unittest.main()
