from trie import Trie

class WordBank():
    def __init__(self) -> None:
        self.trie = Trie()
        
    def addWord(self, word: str) -> None:
        self.trie.insert(word)
        
    def readWords(self, path: str) -> None:
        with open(path, 'r') as f:
            for line in f:
                self.addWord(line.strip())

if __name__ == "__main__":
    wb = WordBank()
    wb.readWords("wordle-words.txt")
    
    # wb.trie.printRoot()
    
    print(wb.trie.atPositions("_o_a_", {"r":[0,2],"o":[3], "a":[]}, set([i for i in "thwge"])))