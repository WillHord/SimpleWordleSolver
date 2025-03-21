from typing import Dict, List, Set


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.isEnd = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self.excluded_at_index = {}

    def strToIndex(self, c: str) -> int:
        return ord(c) - ord("a")

    def insert(self, word: str) -> None:
        root = self.root
        for c in word:
            if c not in root.children:
                root.children[c] = TrieNode()
            root = root.children[c]
        root.isEnd = True

    def included(self, word: str) -> bool:
        root = self.root
        for c in word:
            if c not in root.children:
                return False
            root = root.children[c]
        return root.isEnd

    def search(self, word: str) -> str:
        # Search for a word in the trie and return the word if it exists
        root = self.root
        for c in word:
            if c not in root.children:
                return ""
            root = root.children[c]
        if root.isEnd:
            return word

    def getWordsWithLetter(self, letter: str) -> List[str]:
        # Return all words that contain the letter
        def dfs(node: TrieNode, letter: str, word: List[str]) -> None:
            if node.isEnd and letter in word:
                words.append("".join(word))
            for ch, child in node.children.items():
                dfs(child, letter, word + [ch])

        words = []
        for c in self.root.children:
            dfs(self.root.children[c], letter, [c])
        return words

    def atPositions(
        self, word: str, included: Dict[str, List[int]], excluded: Set[str]
    ) -> List[str]:
        """
        Function that takes a word with underscores and returns a list of all possible words that fit the pattern.
        Underscores are used to represent unknown letters.
        """

        def helperSearch(word: str, node: TrieNode, index: int) -> List[str]:
            if not word:
                return [""] if node.isEnd else []

            if word[0] == "_":
                res = []
                for ch in node.children:
                    if ch in excluded:
                        continue
                    if ch in included and index in included[ch]:
                        continue
                    for w in helperSearch(word[1:], node.children[ch], index + 1):
                        res.append(ch + w)
                return res

            if word[0] in node.children:
                return [
                    word[0] + w
                    for w in helperSearch(word[1:], node.children[word[0]], index + 1)
                ]
            else:
                return []

        words = helperSearch(word, self.root, 0)
        # Filter out all words that don't contain the included letters
        res = []
        for w in words:
            if all(c in w for c in included.keys()):
                res.append(w)

        return res
