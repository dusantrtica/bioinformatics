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


if __name__ == "__main__":
    unittest.main()
