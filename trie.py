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


import unittest


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


if __name__ == "__main__":
    unittest.main()
